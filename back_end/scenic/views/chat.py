import json
import logging
from openai import OpenAI
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import User, Scenic, Attraction, ChatSession, ChatMessage, ChatIntent
from ..serializers import ChatMessageSerializer, ChatSessionSerializer
import requests
import re, ast
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://api.sambanova.ai/v1",
    api_key="c0200d40-6bfe-4787-9a93-1afe0ef739c3"
)

class ChatSessionView(APIView):
    """Chat session management view"""
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all user sessions"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "Missing user ID parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        sessions = ChatSession.objects.filter(user=user, active=True).order_by('-last_message_time')
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """创建新会话"""
        user_id = request.data.get('user_id')
        scenic_id = request.data.get('scenic_id')
        # 添加这一行来获取初始意图类型
        initial_intent = request.data.get('initial_intent')

        print(f"Initial intent: {initial_intent}")
        
        if not user_id:
            return Response({"error": "no user_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        scenic = None
        if scenic_id:
            scenic = get_object_or_404(Scenic, scenic_id=scenic_id)
        
        # 创建会话时设置初始意图
        session = ChatSession.objects.create(
            user=user,
            scenic=scenic,
            current_intent=initial_intent  # 设置初始意图类型
        )
        
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, session_id):
        """Close the session (set to inactive)"""
        session = get_object_or_404(ChatSession, session_id=session_id)
        session.active = False
        session.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatMessageView(APIView):
    """Chat message management view"""
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        """Get the history messages of the session"""
        session = get_object_or_404(ChatSession, session_id=session_id)
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request, session_id):
        """发送新消息并获取AI回复"""
        session = get_object_or_404(ChatSession, session_id=session_id)
        user_message = request.data.get('message')
        intent_type = request.data.get('intent_type')  # 接收前端传递的意图类型
        is_prompt = request.data.get('is_prompt', False)  # 判断是否为提示消息
        print(f"Send new message after click button, Intent type: {intent_type}")
        if not user_message:
            return Response({"error": "The message content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 保存用户消息
        user_chat_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # 如果前端指定了意图类型，直接使用
        if intent_type and intent_type in ['route', 'real_time', 'attraction_info', 'ticket_info']:
            intent = ChatIntent.objects.create(
                message=user_chat_message,
                intent_type=intent_type,
                confidence=0.9,  # 高置信度
                parameters={}
            )
            # 更新会话状态
            session.current_intent = intent_type
            session.save()
        else:
            # 正常处理用户意图
            intent = self._process_intent(user_chat_message)
        
        # 如果是prompt消息，直接返回该消息而不生成新回复
        if is_prompt and intent_type is not 'real_time':
            ai_chat_message = ChatMessage.objects.create(
                session=session,
                message_type='ai',
                content=user_message  # 使用传入的提示文本
            )
        else:
            # 根据用户意图生成回复
            if intent_type == 'real_time':
                ai_response = self._generate_real_time_info(session.scenic)
            else:
                ai_response = self._generate_response(intent, session)
            ai_chat_message = ChatMessage.objects.create(
                session=session,
                message_type='ai',
                content=ai_response
            )
        
        # 更新会话时间
        session.save()
        
        # 返回消息
        result = {
            'user_message': ChatMessageSerializer(user_chat_message).data,
            'ai_message': ChatMessageSerializer(ai_chat_message).data
        }
        
        return Response(result, status=status.HTTP_201_CREATED)
    
    def extract_first_json_block(self, s: str) -> str:
        """返回 s 中第一个成对平衡的 {…} 子串，否则抛 ValueError"""
        start = s.find('{')
        if start < 0:
            raise ValueError("No JSON-like block found")
        count = 0
        for idx, ch in enumerate(s[start:], start):
            if ch == '{':
                count += 1
            elif ch == '}':
                count -= 1
            # 当计数归零，说明找到了完整的一个 JSON 对象
            if count == 0:
                return s[start:idx+1]
        raise ValueError("Braces never balanced")

    def _call_llm_api(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """
        Use the OpenAI client to call the model
        """
        try:
            response = client.completions.create(
                model="Llama-4-Scout-17B-16E-Instruct",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            # Parse the returned text
            # print(f"LLM Response: {response.choices[0].text.strip()}")
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return "Sorry, I'm unable to process this request right now. Please try again later."
    
    def _process_intent(self, message):
        """Process the user intent"""
        session = message.session
        previous_intent = session.current_intent  # 获取上一次的意图

        print(f"Previous intent: {previous_intent}")
    
        prompt = (
            "You are a scenic AI assistant. Your goal is to analyze and determine the intent and other information based on the context information."
            "Important context information:\n"
            f"- The previous intent type: {previous_intent}\n"
            f"The user new massage is: \"{message.content}\"\n"
            "Instructions:\n"
            "1. Read the user's new message, determine the current intent type.\n"
            "2. Identify the parameters: location, preference, time constraint.\n"
            "3. Provide a confidence score for the intent detection (0-1).\n"
            "4. The intent type can be one of the following: route, real_time, ticket_info, attraction_info, general.\n"
            "5. If the user's message is unclear or related to multiple intents, but related to the previous intent, keep the previous intent type and increase the confidence.\n"
            "6. If user only send a location such as the scenic name or attraction name, keep the previous intent type and increase the confidence.\n"
            "7. If it is determined that the user's intent has been clearly changed, update to the new intent and give a higher confidence.\n"
            "8. Only output the result with highest confidence in JSON format, DO NOT include your thinking process and any other content.\n"
            "- Example output: {\"intent_type\": \"route\", \"parameters\": {\"location\": \"Hong Kong\", \"time_constraint\": \"one day\", \"preference\": \"natural scenery\"}, \"confidence\": 0.8}\n"
            
        )
        response = self._call_llm_api(prompt)
        print(f"Process intent response: {response}")
        try:
            # 1. 匹配第一个 {...} 块
            block = self.extract_first_json_block(response)
            print("Got JSON block:", block)

            # 2. 优先尝试 JSON 解析（双引号）
            try:
                intent_data = json.loads(block)
                print("intent_data: ", intent_data)
            except json.JSONDecodeError:
                # 3. 再尝试 ast.literal_eval（支持单引号、Python 字典字面量）
                intent_data = ast.literal_eval(block)

            # 4. 最终提取字段
            intent_type = intent_data.get('intent_type', 'general')
            parameters  = intent_data.get('parameters', {}) or {}
            confidence  = float(intent_data.get('confidence', 0.5))

        except Exception as e:
            print(f"解析JSON失败: {e}")
            intent_type, parameters, confidence = 'general', {}, 0.5
        # intent_type = intent_data.get('intent_type', 'general')
        # parameters  = intent_data.get('parameters', {}) or {}
        # confidence  = float(intent_data.get('confidence', 0.5))
        print(f"Intent type: {intent_type}, Parameters: {parameters}, Confidence: {confidence}")

        if previous_intent != 'general' and (intent_type == 'general' or confidence < 0.6):
            # 如果上一个意图是路线推荐，而当前意图不明确或置信度低
            # 则假定用户仍在讨论路线
            intent_type = 'route'
            confidence = max(confidence, 0.7)  # 提高置信度
            # 从用户消息中提取可能的参数
            if 'preference' not in parameters and re.search(r'like|enjoy|prefer|love', message.content, re.I):
                # 尝试提取用户偏好
                parameters['preference'] = message.content
                
            if 'time_constraint' not in parameters and re.search(r'day|hour|time|week|month', message.content, re.I):
                # 尝试提取时间约束
                parameters['time_constraint'] = message.content
        
        # 更新会话状态
        session.current_intent = intent_type
        session.save()
        # Create an intent record
        intent = ChatIntent.objects.create(
            message=message,
            intent_type=intent_type,
            confidence=confidence,
            parameters=parameters
        )
        
        return intent

    def _generate_general_response(self, intent: ChatIntent) -> str:
        """
        General reply generated using LLM
        """
        prompt = (
            f"You are a scenic AI assistant, the user said:\"{intent.message.content}\"，"
            "Please reply briefly and effectively, do not include any programming code or other non-related content."
        )
        return self._call_llm_api(prompt, max_tokens=256, temperature=0.7)
    
    """
        TODO: 
        Need modify after the database information is confirmed
    """
    def _extract_attraction(self, content):
        """Extract the attraction name from the user message"""
        # The actual implementation may need to use NER or more complex algorithms
        # Here is a simple implementation, matching the existing attraction names in the database
        attractions = Attraction.objects.all()
        for attraction in attractions:
            if attraction.attraction_name in content:
                return attraction.attraction_name
        return None
    
    def _generate_response(self, intent, session):
        """Generate a reply based on the intent"""
        intent_type = intent.intent_type
        parameters = intent.parameters
        scenic = session.scenic
        print(f"Scenic: {scenic}")
        attractions = Attraction.objects.filter(scenic_id=scenic.scenic_id)

        if intent_type == 'route':
            return self._generate_route_recommendation(parameters, attractions, scenic)
        elif intent_type == 'real_time':
            return self._generate_real_time_info(scenic)
        elif intent_type == 'attraction_info':
            return self._generate_attraction_info(parameters, scenic)
        elif intent_type == 'ticket_info':
            return self._generate_ticket_info(parameters)
        else:
            return self._generate_general_response(intent)

    """
        TODO: 
        Need modify after the all prompt is confirmed
    """ 
    def _extract_response(self, response: str, response_type: str = "general") -> str:
        patterns = {
            "route":       r'(Ok, I have recommended a tour route for you:[\s\S]*?)(?=\s*\*/|$)',
            "ticket_info": r'(Ok, the ticket information of the attraction is as follows:[\s\S]*?)(?=\s*\*/|$)',
            "general":     r'([\s\S]+?)(?=\s*\*/|$)'
        }

        # 1. 根据 response_type 提取目标片段，fallback 到 entire response
        pattern = patterns.get(response_type, patterns["general"])
        m = re.search(pattern, response, flags=re.DOTALL)
        text = m.group(1) if m else response

        # 2. 清理 Markdown/``` 代码块
        text = re.sub(r'```[\s\S]*?```', '', text)

        # 3. 清理注释 /*...*/, //..., <!--...-->
        text = re.sub(r'/\*[\s\S]*?\*/', '', text)
        text = re.sub(r'//.*?(?=\n|$)', '', text)
        text = re.sub(r'<!--[\s\S]*?-->', '', text)

        # 4. 清理常见编程残留片段（可根据需要删减）
        text = re.sub(
            r'\b(return\s+0;|int\s+main\(\)|public\s+class\b|#include\b)[\s\S]*',
            '',
            text
        )

        # 5. 合并多余空白，保留 HTML 标签
        text = re.sub(r'\s+', ' ', text).strip()

        return text

        
    def _generate_route_recommendation(self, parameters: Dict[str, Any], attractions: List[Dict[str, Any]], scenic=None) -> str:
        """Generate route recommendation reply"""
        # Create a formatted string of scenic attractions information as the knowledge base of LLM
        attractions_info = ""
        for attraction in attractions:
            status_text = "Opening" if attraction.status == 1 else "Closed" if attraction.status == 0 else "Crowded"
            attractions_info += f"Attraction ID: {attraction.attraction_id}, Name: {attraction.attraction_name}, Description: {attraction.description}, " \
                            f"Category: {attraction.category}, Status: {status_text}, " \
                            f"Opens: {attraction.open_time}to{attraction.close_time}, " \
                            f"Current number of visitors: {attraction.count}, Maximum capacity: {attraction.flow_limit}\n"
        print(f"Attractions info: {attractions_info}")
        
        # When location is empty, use scenic.scenic_name as the user's location
        location = parameters.get("location", "")
        if not location and scenic:
            location = scenic.scenic_name
        
        preference = parameters.get("preference", "no preference")
        time_constraint = parameters.get("time_constraint", "no time constraint")
        print(f"Location: {location}, Preference: {preference}, Time constraint: {time_constraint}")
        prompt = f"""
            You are a scenic AI assistant. Please recommend a tour route for the user based on the following information:
            User's requirements:
            - Location: {location}
            - Preference: {preference}
            - Time constraint: {time_constraint}
            
            Available attractions information:
            {attractions_info}

            Please note the following rules:
            1. Only recommend attractions that are in the database and match the user's location.
            2. Do not recommend attractions that are not in the database.
            3. Do not recommend attractions that are closed.
            4. For attractions that are crowded, you can recommend them but need to add a special prompt.
            5. According to the user's time constraint, plan an appropriate number of attractions.
            6. Try to meet the user's keyword preferences.
            7. Provide a reasonable itinerary and recommend a visit time for each attraction.
            8. Give a brief reason for the route.
            9. Answer in html format, you can use <br> to break the line and other html tags to beautify the text.

            Please start your answer with "Ok, I have recommended a tour route for you:"
        """
        response = self._call_llm_api(prompt, max_tokens=1024, temperature=0.7)
        print(f"Route recommendation response: {response}")
        route_recommendation = self._extract_response(response, "route")

        if route_recommendation:
            return route_recommendation
        else:
            return "Sorry, I couldn't generate a tour route for you. Please try again later."

    """
        TODO: 
        Need to improve, haven't tested yet
    """
    def _generate_real_time_info(self, scenic):
        """Generate real-time information reply"""
        if not scenic:
            return "Please select a scenic first, I can provide you with real-time information."
            
        # Get the real-time visitor flow data of the attractions in the scenic
        attractions = Attraction.objects.filter(scenic_id=scenic.scenic_id).order_by('-count')
        
        if not attractions:
            return f"Sorry, I couldn't get the real-time data of {scenic.scenic_name}."
            
        most_crowded = attractions.first()
        least_crowded = attractions.last()
        
        response = f"🗺️ {scenic.scenic_name} current real-time situation:<br>"
        response += f"- The most crowded attraction: {most_crowded.attraction_name}, about {most_crowded.count} people<br>"
        response += f"- The least crowded attraction: {least_crowded.attraction_name}, about {least_crowded.count} people<br>"
        
        # Add a warning for crowded attractions
        alert_attractions = attractions.filter(status=2)
        if alert_attractions:
            response += "⚠️ The following attractions are currently crowded, you can visit them during off-peak hours:<br>"
            for attraction in alert_attractions:
                response += f"- {attraction.attraction_name}<br>"
                
        return response
    
    def _generate_attraction_info(self, parameters, scenic):
        """Generate attraction information reply"""
        attraction_name = parameters.get('location')
        
        if attraction_name:
            # Query specific attractions
            try:
                attraction = Attraction.objects.get(attraction_name=attraction_name)
                response = f"📍 {attraction.attraction_name}<br>"
                response += f"{attraction.description}<br>"
                response += f"🏡 Address: {attraction.address}<br>"
                response += f"⏰ Open time: {attraction.open_time.strftime('%H:%M')} - {attraction.close_time.strftime('%H:%M')}<br>"
                if attraction.fee:
                    response += f"🎫 Ticket price: ${attraction.fee}<br>"
                if attraction.phone:
                    response += f"📞 Phone: {attraction.phone}<br>"
                return response
            except Attraction.DoesNotExist:
                return f"Sorry, I couldn't find information about {attraction_name}."
        elif scenic:
            # If no specific attraction is specified but there is a scenic, introduce the scenic
            attractions = Attraction.objects.filter(scenic_id=scenic.scenic_id)[:5]
            response = f"{scenic.scenic_name} main attractions:\n\n"
            for i, attraction in enumerate(attractions, 1):
                response += f"{i}. {attraction.attraction_name}\n"
            response += f"\nTo learn more about specific attractions, please ask for the attraction name directly."
            return response
        else:
            return "What specific attraction or scenic information would you like to know?"
    
    def _generate_ticket_info(self, parameters: Dict[str, Any]):
        """Generate ticket information reply"""
        prompt = f"""
            You are a scenic AI assistant. Please provide ticket information based on the following information:

            The attraction the user asked for: {parameters.get('location', '')}
            
            If the attraction needs to buy tickets, please start your answer with "Ok, the ticket information of the attraction is as follows:" and provide the following information:
            1. Ticket price
            2. Discounts
            3. Purchase methods
            4. Other related information

            If the attraction does not need to buy tickets, please say that the attraction is free and visitors do not need to buy tickets to enter.

            Only return the ticket information in beautified html format (do not use <li>), do not include any programming code or other non-related content.
        """
        response = self._call_llm_api(prompt, max_tokens=512, temperature=0.7)

        ticket_info = self._extract_response(response, "ticket_info")

        if ticket_info:
            return ticket_info
        else:
            return "Sorry, I couldn't generate ticket information for you. Please try again later."
    
    def _generate_general_response(self, intent):
        """Generate a general reply"""
        user_message = intent.message.content

        prompt = f"""
            You are a scenic AI assistant. Please generate a brief reply based on the user's message.
            User's message: {user_message}
            Please avoid using programming code or other non-related content.
        """
        response = self._call_llm_api(prompt, max_tokens=512, temperature=0.7)

        general_response = self._extract_response(response)

        if general_response:
            return general_response
        else:
            return "Sorry, I didn't fully understand your message. You can try asking about attraction recommendations, real-time visitor flow, or ticket information."