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
import re
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
        """Create new session"""
        user_id = request.data.get('user_id')
        scenic_id = request.data.get('scenic_id')
        # Add this line to get the initial intent type
        initial_intent = request.data.get('initial_intent')

        print(f"Initial intent: {initial_intent}")
        
        if not user_id:
            return Response({"error": "no user_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        scenic = None
        if scenic_id:
            scenic = get_object_or_404(Scenic, scenic_id=scenic_id)
        
        # Set initial intent when creating session
        session = ChatSession.objects.create(
            user=user,
            scenic=scenic,
            current_intent=initial_intent  # Set initial intent type
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
        """Send new message and get AI reply"""
        session = get_object_or_404(ChatSession, session_id=session_id)
        user_message = request.data.get('message')
        intent_type = request.data.get('intent_type')  # Receive intent type passed from frontend
        is_prompt = request.data.get('is_prompt', False)  # Check if it's a prompt message
        print(f"Send new message after click button, Intent type: {intent_type}")
        if not user_message:
            return Response({"error": "The message content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save user message
        user_chat_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # If intent type is specified by frontend, use it directly
        if intent_type and intent_type in ['route', 'real_time', 'attraction_info', 'ticket_info']:
            intent = ChatIntent.objects.create(
                message=user_chat_message,
                intent_type=intent_type,
                confidence=0.9,  # High confidence
                parameters={}
            )
            # Update session state
            session.current_intent = intent_type
            session.save()
        else:
            # Normal user intent processing
            intent = self._process_intent(user_chat_message)
        
        # If it's a prompt message, return this message directly without generating new reply
        if is_prompt:
            ai_chat_message = ChatMessage.objects.create(
                session=session,
                message_type='ai',
                content=user_message  # Use the provided prompt text
            )
        else:
            # Generate reply based on user intent
            ai_response = self._generate_response(intent, session)
            ai_chat_message = ChatMessage.objects.create(
                session=session,
                message_type='ai',
                content=ai_response
            )
        
        # Update session time
        session.save()
        
        # Return message
        result = {
            'user_message': ChatMessageSerializer(user_chat_message).data,
            'ai_message': ChatMessageSerializer(ai_chat_message).data
        }
        
        return Response(result, status=status.HTTP_201_CREATED)
    
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
        previous_intent = session.current_intent  # Get previous intent

        print(f"Previous intent: {previous_intent}")
    
        prompt = (
            "You are a scenic AI assistant. Your goal is to analyze and determine the intent and other information based on the user's message and the previous intent."
            "Important context information:\n"
            f"- The previous intent type: {previous_intent}\n"
            "Instructions:\n"
            "1. Read the user's message and determine the intent type.\n"
            "2. Identify the parameters such as location, preference, time constraint, etc.\n"
            "3. Provide a confidence score for the intent detection (0-1).\n"
            "4. The intent type can be one of the following: route, real_time, ticket_info, attraction_info, general.\n"
            "5. If the user's message is unclear or related to multiple intents, but related to the previous intent, keep the previous intent type and increase the confidence.\n"
            "6. If user only send a location such as the scenic name or attraction name, keep the previous intent type and increase the confidence.\n"
            "6. If it is determined that the user's intent has been clearly changed, update to the new intent and give a higher confidence.\n"
            "7. Only output the result in JSON format, do not include any other content.\n"
            "- Example output: {'intent_type': 'route', 'parameters': {'location': 'West Lake', 'time_constraint': 'one day', 'preference': 'natural scenery'}, 'confidence': 0.8}\n"
            f"The user new massage is: \"{message.content}\"\n"
        )
        response = self._call_llm_api(prompt)
        print(f"Process intent response: {response}")
        try:
            json_match = re.search(r'\{[\s\n]*"intent_type"[\s\S]*?\}(?=\s*$|\n|\.)', response)
            if json_match:
                # Found the standard JSON format (double quotes)
                json_str = json_match.group(0)
                intent_data = json.loads(json_str)
            else:
                # Try to handle the JSON format using single quotes
                json_match = re.search(r'\{[\s\n]*\'intent_type\'[\s\S]*?\}(?=\s*$|\n|\.)', response)
                if json_match:
                    json_str = json_match.group(0).replace("'", '"')
                    intent_data = json.loads(json_str)
                else:
                    # Try to get any JSON data block
                    json_blocks = re.findall(r'\{[\s\S]*?\}', response)
                    for block in json_blocks:
                        try:
                            # Try to clean and parse each block
                            cleaned_block = block.replace("'", '"')
                            intent_data = json.loads(cleaned_block)
                            if 'intent_type' in intent_data:
                                break
                        except json.JSONDecodeError:
                            continue
                    else:
                        # If no valid JSON block is found, use a default intent
                        print("No valid JSON intent data found, using default.")
                        intent_data = {
                            'intent_type': 'general',
                            'parameters': {},
                            'confidence': 0.5
                        }
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Raw JSON data: {json_str}")
            # Fallback to general intent
            intent_data = {
                'intent_type': 'general',
                'parameters': {},
                'confidence': 0.5
            }
            
        # Create or update intent record
        intent_type = intent_data.get('intent_type', 'general')
        parameters = intent_data.get('parameters', {})
        confidence = float(intent_data.get('confidence', 0.5))
        
        # Update session with current intent type
        session.current_intent = intent_type
        session.save()
        
        # Create intent record
        intent = ChatIntent.objects.create(
            message=message,
            intent_type=intent_type,
            confidence=confidence,
            parameters=parameters
        )
        
        return intent
    
    def _extract_attraction(self, content):
        """Extract attraction information from content"""
        attractions = Attraction.objects.all()
        found_attractions = []
        
        for attraction in attractions:
            if attraction.attraction_name in content:
                found_attractions.append({
                    'id': attraction.attraction_id,
                    'name': attraction.attraction_name,
                    'scenic_id': attraction.scenic_id
                })
                
        return found_attractions
    
    def _generate_response(self, intent, session):
        """Generate response based on intent"""
        intent_type = intent.intent_type
        parameters = intent.parameters
        scenic = session.scenic
        
        if intent_type == 'route':
            attractions = []
            if scenic:
                attractions = Attraction.objects.filter(scenic=scenic).values(
                    'attraction_id', 'attraction_name', 'address', 'description', 'category',
                    'fee', 'open_time', 'close_time', 'status', 'count'
                )
            return self._generate_route_recommendation(parameters, attractions, scenic)
            
        elif intent_type == 'real_time':
            return self._generate_real_time_info(scenic)
            
        elif intent_type == 'attraction_info':
            return self._generate_attraction_info(parameters, scenic)
            
        elif intent_type == 'ticket_info':
            return self._generate_ticket_info(parameters)
            
        else:  # general intent or fallback
            return self._generate_general_response(intent)
    
    def _extract_response(self, response: str, response_type: str = "general") -> str:
        """Extract response from LLM output"""
        # If the response is already clean, return it directly
        if not response.strip().startswith('```') and '```' not in response:
            return response.strip()
        
        # Try to extract content from markdown code blocks
        code_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        matches = re.findall(code_pattern, response)
        
        if matches:
            # Extract the content from the first code block
            extracted = matches[0].strip()
            
            # For JSON responses, parse and format nicely
            if response_type == "json":
                try:
                    data = json.loads(extracted)
                    return json.dumps(data, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    # If it's not valid JSON, return as is
                    return extracted
            
            return extracted
        
        # If no code blocks found, return the original response with markdown removed
        return re.sub(r'```.*?```', '', response, flags=re.DOTALL).strip()
    
    def _generate_route_recommendation(self, parameters: Dict[str, Any], attractions: List[Dict[str, Any]], scenic=None) -> str:
        """Generate route recommendation based on parameters"""
        if not attractions:
            return "I don't have information about attractions in this area. Could you specify which scenic area you're interested in?"
        
        prompt = (
            "You are a tour guide AI assistant. Generate a personalized route recommendation based on the attractions and user preferences.\n\n"
            "Instructions:\n"
            "1. Analyze the available attractions and user preferences.\n"
            "2. Create a route that makes geographical sense (nearby attractions grouped together).\n"
            "3. Consider time constraints, visitor count, and attraction categories.\n"
            "4. Output a route with 3-5 attractions (unless user specified otherwise).\n"
            "5. For each attraction, include:\n"
            "   - Name\n"
            "   - Brief description (if available)\n"
            "   - Recommended visit duration\n"
            "6. Add a brief introduction at the beginning and conclusion at the end.\n"
            "7. Keep the format clear and easy to read.\n\n"
        )
        
        # Add user preferences if available
        if parameters:
            prompt += "User preferences:\n"
            for key, value in parameters.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        # Add attractions information
        prompt += "Available attractions:\n"
        for idx, attraction in enumerate(attractions, 1):
            prompt += f"{idx}. {attraction['attraction_name']}\n"
            if 'category' in attraction:
                category_map = {1: "Natural Scenery", 2: "Historical Sites", 3: "Cultural Heritage", 4: "Entertainment Experience"}
                category = category_map.get(attraction['category'], "Other")
                prompt += f"   - Category: {category}\n"
            if 'count' in attraction:
                prompt += f"   - Current visitors: {attraction['count']}\n"
            if 'fee' in attraction and attraction['fee']:
                prompt += f"   - Entrance fee: {attraction['fee']} HKD\n"
            if 'open_time' in attraction and 'close_time' in attraction:
                prompt += f"   - Hours: {attraction['open_time']} - {attraction['close_time']}\n"
            if 'description' in attraction and attraction['description']:
                desc = attraction['description']
                if len(desc) > 100:
                    desc = desc[:100] + "..."
                prompt += f"   - Description: {desc}\n"
        
        response = self._call_llm_api(prompt, max_tokens=800)
        return self._extract_response(response)
    
    def _generate_real_time_info(self, scenic):
        """Generate real-time information about the scenic area"""
        if not scenic:
            return "I need to know which scenic area you're asking about to provide real-time information. Could you please specify?"
        
        # Get real-time attraction data
        attractions = Attraction.objects.filter(scenic=scenic)
        
        prompt = (
            "You are a tour guide AI assistant. Provide real-time information about the scenic area and its attractions.\n\n"
            f"Scenic Area: {scenic.scenic_name}\n\n"
            "Attraction status:\n"
        )
        
        for attraction in attractions:
            status_text = "Not Open"
            if attraction.status == 1:
                status_text = "Open"
            elif attraction.status == 2:
                status_text = "Crowd Warning"
            
            prompt += f"- {attraction.attraction_name}:\n"
            prompt += f"  * Status: {status_text}\n"
            prompt += f"  * Current visitors: {attraction.count}\n"
            prompt += f"  * Visitor limit: {attraction.flow_limit}\n"
            prompt += f"  * Hours: {attraction.open_time} - {attraction.close_time}\n"
        
        prompt += "\nBased on this information, provide a helpful summary of the current situation in the scenic area. Mention which attractions are crowded, which are good to visit now, and any other relevant information to help the visitor plan their day."
        
        response = self._call_llm_api(prompt, max_tokens=600)
        return self._extract_response(response)
    
    def _generate_attraction_info(self, parameters, scenic):
        """Generate information about specific attractions"""
        # Try to extract attraction name from parameters
        attraction_name = None
        if parameters and 'attraction' in parameters:
            attraction_name = parameters['attraction']
        elif parameters and 'location' in parameters:
            attraction_name = parameters['location']
        
        if attraction_name:
            # Look for matching attractions
            attractions = Attraction.objects.filter(attraction_name__icontains=attraction_name)
            if not attractions.exists() and scenic:
                # If no direct match, try to find within the current scenic area
                attractions = Attraction.objects.filter(scenic=scenic)
        elif scenic:
            # If no specific attraction mentioned, return info about all attractions in the scenic area
            attractions = Attraction.objects.filter(scenic=scenic)
        else:
            return "I need more information about which attraction you're interested in. Could you specify a name or ask about a specific category of attractions?"
        
        prompt = "You are a tour guide AI assistant. Provide helpful information about the following attraction(s):\n\n"
        
        for attraction in attractions:
            prompt += f"Attraction: {attraction.attraction_name}\n"
            prompt += f"Address: {attraction.address}\n"
            if attraction.description:
                prompt += f"Description: {attraction.description}\n"
            prompt += f"Category: {attraction.get_category_display()}\n"
            if attraction.fee:
                prompt += f"Entrance Fee: {attraction.fee} HKD\n"
            prompt += f"Opening Hours: {attraction.open_time} - {attraction.close_time}\n"
            prompt += f"Current Status: {attraction.get_status_display()}\n"
            prompt += f"Current Visitors: {attraction.count} / {attraction.flow_limit}\n\n"
        
        prompt += "Provide a helpful and informative response about these attractions. Include practical information that would be useful for visitors."
        
        response = self._call_llm_api(prompt, max_tokens=700)
        return self._extract_response(response)
    
    def _generate_ticket_info(self, parameters: Dict[str, Any]):
        """Generate information about tickets"""
        # Try to extract attraction name from parameters
        attraction_name = None
        if parameters and 'attraction' in parameters:
            attraction_name = parameters['attraction']
        
        if attraction_name:
            # Look for matching attractions with ticket prices
            attractions = Attraction.objects.filter(
                attraction_name__icontains=attraction_name,
                fee__isnull=False
            )
        else:
            # If no specific attraction mentioned, return general ticket info
            attractions = Attraction.objects.filter(fee__isnull=False).exclude(fee=0)[:5]
        
        if not attractions.exists():
            return "I couldn't find ticket information for the specified attraction. Most attractions in Hong Kong are free to visit, but some may require admission fees. Could you specify which attraction you're interested in?"
        
        prompt = "You are a tour guide AI assistant. Provide helpful information about tickets for the following attraction(s):\n\n"
        
        for attraction in attractions:
            prompt += f"Attraction: {attraction.attraction_name}\n"
            prompt += f"Entrance Fee: {attraction.fee} HKD\n"
            prompt += f"Opening Hours: {attraction.open_time} - {attraction.close_time}\n"
            prompt += f"Current Status: {attraction.get_status_display()}\n\n"
        
        prompt += "Additional Information:\n"
        prompt += "- Tickets can be purchased through our app by visiting the 'Book Tickets' section.\n"
        prompt += "- Some attractions may offer discounts for children, students, and seniors.\n"
        prompt += "- It's recommended to book tickets in advance during peak season or holidays.\n\n"
        
        prompt += "Provide a helpful response about ticket information for these attractions. Include practical booking advice."
        
        response = self._call_llm_api(prompt, max_tokens=600)
        return self._extract_response(response)
    
    def _generate_general_response(self, intent):
        """Generate a general response when no specific intent is identified"""
        message = intent.message.content
        
        prompt = (
            "You are a helpful tour guide AI assistant for Hong Kong. Respond to the following user query in a friendly and helpful manner:\n\n"
            f"User: {message}\n\n"
            "Instructions:\n"
            "1. If the query is about Hong Kong tourism, provide helpful information.\n"
            "2. If you're unsure, suggest topics the user might be interested in such as attractions, routes, or tickets.\n"
            "3. Keep your response concise and informative.\n"
            "4. If appropriate, suggest that the user can ask about specific attractions, real-time information, route recommendations, or tickets.\n"
        )
        
        response = self._call_llm_api(prompt, max_tokens=400)
        return self._extract_response(response)