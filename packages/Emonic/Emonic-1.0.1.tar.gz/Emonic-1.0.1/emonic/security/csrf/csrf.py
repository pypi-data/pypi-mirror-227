import os
import secrets
import time
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import Forbidden
from itsdangerous import URLSafeSerializer
from functools import wraps

class CSRF:
    def __init__(self, app):
        self.app = app
        self.csrf_secret_key = os.urandom(32)
        self.cookie_secret_key = os.urandom(32)
        self.token_name = 'csrf_token'
        self.csrf_serializer = URLSafeSerializer(self.csrf_secret_key)
        self.cookie_serializer = URLSafeSerializer(self.cookie_secret_key)
        self.rate_limit_period = 60  # 1 minute
        self.rate_limit_max_requests = 5
        self.rate_limit_storage = {}

    def generate_csrf_token(self):
        return secrets.token_hex(32)

    def protect(self, handler):
        @wraps(handler)
        def wrapper(request, **values):
            self._apply_rate_limit(request.remote_addr)
            
            if request.method in ('POST', 'PUT', 'DELETE'):
                submitted_token = request.form.get(self.token_name)
                session_token = request.cookies.get(self.token_name)

                if not submitted_token or submitted_token != session_token:
                    raise Forbidden("CSRF token validation failed.")
            return handler(request, **values)
        return wrapper

    def set_csrf_token_cookie(self, response, token):
        response.set_cookie(self.token_name, token, httponly=True, secure=True, samesite='strict', max_age=3600)

    def _apply_rate_limit(self, ip_address):
        now = int(time.time())
        if ip_address not in self.rate_limit_storage:
            self.rate_limit_storage[ip_address] = [(now, 1)]
            return
        
        requests = self.rate_limit_storage[ip_address]
        requests = [r for r in requests if now - r[0] <= self.rate_limit_period]
        requests.append((now, len(requests) + 1))
        
        if len(requests) > self.rate_limit_max_requests:
            raise Forbidden("Rate limit exceeded.")
        
        self.rate_limit_storage[ip_address] = requests
    
    def get_csrf_token(self, request):
        return request.cookies.get(self.token_name)

    def generate_csrf_token_and_set_cookie(self, response):
        token = self.generate_csrf_token()
        self.set_csrf_token_cookie(response, token)
        return token

    def require_csrf_token(self, request):
        token = self.get_csrf_token(request)
        if not token:
            raise Forbidden("CSRF token missing.")
        return token

    def validate_csrf_token(self, request):
        submitted_token = request.form.get(self.token_name)
        session_token = self.get_csrf_token(request)
        return submitted_token and submitted_token == session_token

    def csrf_exempt(self, handler):
        return handler

    def is_csrf_request(self, request):
        return request.method in ('POST', 'PUT', 'DELETE')

    def is_same_origin(self, request):
        return True  # Add your same-origin check logic here

    def _get_request_ip(self, request):
        return request.remote_addr

    def _get_session_token(self, request):
        return request.cookies.get(self.token_name)

    def _set_session_token(self, response, token):
        self.set_csrf_token_cookie(response, token)

    def _generate_token(self):
        return self.generate_csrf_token()

    def _clear_session_token(self, response):
        response.delete_cookie(self.token_name)

    def _should_set_cookie(self, request):
        return self.is_same_origin(request) and self.is_csrf_request(request)

    def __call__(self, environ, start_response):
        request = Request(environ)
        environ['csrf'] = self
        return self.app(environ, start_response)