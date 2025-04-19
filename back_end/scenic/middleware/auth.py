from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def precess_request(self, request):
        if request.path_info in ["/api/login", "/api/image_code"] :
            return
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect("/api/login")