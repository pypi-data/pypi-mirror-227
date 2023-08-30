import logging
from werkzeug.wrappers import Response

class CORS:
    def __init__(
        self,
        allowed_origins='*',
        allowed_methods=None,
        max_age=3600,
        allowed_headers=None,
        expose_headers=None,
        allow_credentials=False,
        cors_profile='default',
        validate_request_origin=None,
        log_cors_requests=False,
        cors_logger_name='cors',
    ):
        self.allowed_origins = allowed_origins
        self.allowed_methods = allowed_methods
        self.max_age = max_age
        self.allowed_headers = allowed_headers
        self.expose_headers = expose_headers
        self.allow_credentials = allow_credentials
        self.cors_profile = cors_profile
        self._validate_request_origin = validate_request_origin
        self.log_cors_requests = log_cors_requests
        self.cors_logger_name = cors_logger_name
        self.cors_logger = logging.getLogger(cors_logger_name)

    def handle_preflight(self, request):
        response = Response('', status=204)
        response.headers.update(self._build_cors_headers())
        return response

    def enable(self):
        def decorator(handler):
            def wrapper(request, **values):
                if not self.validate_request_origin(request):
                    self.cors_logger.warning('Request origin not allowed: %s', request.headers.get('Origin'))
                    return self._handle_error('Forbidden', status_code=403)

                if self.log_cors_requests:
                    self.log_cors_request(request.headers.get('Origin'))

                response = handler(request, **values)

                if request.method == 'OPTIONS':
                    return self.preflight_response()

                if isinstance(response, Response):
                    response.headers.update(self._build_cors_headers())
                    return response

                response = Response(response, content_type='text/plain')
                response.headers.update(self._build_cors_headers())
                return response

            return wrapper

        return decorator

    def _build_cors_headers(self):
        cors_headers = {
            'Access-Control-Allow-Origin': self.allowed_origins,
            'Access-Control-Allow-Methods': ', '.join(self.allowed_methods or []),
            'Access-Control-Max-Age': str(self.max_age)
        }
        if self.allowed_headers:
            cors_headers['Access-Control-Allow-Headers'] = ', '.join(self.allowed_headers)
        if self.expose_headers:
            cors_headers['Access-Control-Expose-Headers'] = ', '.join(self.expose_headers)
        if self.allow_credentials:
            cors_headers['Access-Control-Allow-Credentials'] = 'true'
        return cors_headers

    def _handle_error(self, error_message, status_code=400):
        response = Response(error_message, status=status_code)
        response.headers.update(self._build_cors_headers())
        return response

    def handle_error(self, error_message, status_code=400):
        return self._handle_error(error_message, status_code)

    def set_allowed_origins(self, origins):
        self.allowed_origins = origins

    def set_allowed_methods(self, methods):
        self.allowed_methods = methods

    def set_allowed_headers(self, headers):
        self.allowed_headers = headers

    def set_expose_headers(self, headers):
        self.expose_headers = headers

    def set_allow_credentials(self, allow):
        self.allow_credentials = allow

    def set_max_age(self, age):
        self.max_age = age

    def set_cors_logger_name(self, logger_name):
        self.cors_logger_name = logger_name
        self.cors_logger = logging.getLogger(logger_name)

    def validate_request_origin(self, request):
        if callable(self._validate_request_origin):
            return self._validate_request_origin(request)
        elif self._validate_request_origin is None or self._validate_request_origin == '*':
            return True
        elif isinstance(self._validate_request_origin, (list, tuple)):
            return request.headers.get('Origin') in self._validate_request_origin
        return False

    def log_cors_request(self, origin):
        self.cors_logger.info('CORS request from origin: %s', origin)

    def preflight_response(self):
        response = Response('', status=204)
        response.headers.update(self._build_cors_headers())
        return response

    def custom_response(self, content, content_type='text/plain', status_code=200):
        response = Response(content, content_type=content_type, status=status_code)
        response.headers.update(self._build_cors_headers())
        return response
    
    def set_validate_request_origin(self, validation_function):
        self.validate_request_origin = validation_function

    def add_allowed_origin(self, origin):
        if self.allowed_origins == '*':
            self.allowed_origins = []
        if origin not in self.allowed_origins:
            self.allowed_origins.append(origin)

    def remove_allowed_origin(self, origin):
        if origin in self.allowed_origins:
            self.allowed_origins.remove(origin)

    def add_allowed_method(self, method):
        if self.allowed_methods is None:
            self.allowed_methods = []
        if method not in self.allowed_methods:
            self.allowed_methods.append(method)

    def remove_allowed_method(self, method):
        if self.allowed_methods is not None and method in self.allowed_methods:
            self.allowed_methods.remove(method)

    def add_allowed_header(self, header):
        if self.allowed_headers is None:
            self.allowed_headers = []
        if header not in self.allowed_headers:
            self.allowed_headers.append(header)

    def remove_allowed_header(self, header):
        if self.allowed_headers is not None and header in self.allowed_headers:
            self.allowed_headers.remove(header)
            
    def add_exposed_header(self, header):
        if self.expose_headers is None:
            self.expose_headers = []
        if header not in self.expose_headers:
            self.expose_headers.append(header)

    def remove_exposed_header(self, header):
        if self.expose_headers is not None and header in self.expose_headers:
            self.expose_headers.remove(header)
            
    def set_cors_profile(self, profile):
        self.cors_profile = profile

    def enable_logging(self, logger_name='cors'):
        self.log_cors_requests = True
        self.cors_logger_name = logger_name
        self.cors_logger = logging.getLogger(logger_name)

    def disable_logging(self):
        self.log_cors_requests = False
        self.cors_logger_name = ''
        self.cors_logger = None
        
    def set_logger_level(self, level):
        if self.cors_logger:
            self.cors_logger.setLevel(level)

    def enable_all_methods(self):
        self.allowed_methods = ['OPTIONS', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def enable_all_headers(self):
        self.allowed_headers = None  # Allows all headers
        self.expose_headers = None  # Exposes all headers

    def disable_credentials(self):
        self.allow_credentials = False

    def disable_preflight_cache(self):
        self.max_age = 0
        
    def set_max_age_minutes(self, minutes):
        self.max_age = minutes * 60

    def add_custom_header(self, key, value):
        if self.custom_headers is None:
            self.custom_headers = {}
        self.custom_headers[key] = value

    def remove_custom_header(self, key):
        if self.custom_headers is not None and key in self.custom_headers:
            del self.custom_headers[key]
    
    def set_cors_origin_validator(self, origin_validator):
        self.cors_origin_validator = origin_validator

    def set_expose_all_headers(self, expose_all=True):
        if expose_all:
            self.expose_headers = None  # Expose all headers
        else:
            self.expose_headers = []

    def set_response_headers(self, headers):
        self.response_headers = headers

    def clear_response_headers(self):
        self.response_headers = {}
        
    def enable_same_site_cookies(self, same_site_policy='Lax'):
        self.same_site_cookies = same_site_policy

    def set_cors_max_age(self, max_age_seconds):
        self.max_age = max_age_seconds

    def set_cors_allowed_origins(self, origins):
        self.allowed_origins = origins

    def set_cors_allowed_methods(self, methods):
        self.allowed_methods = methods
