from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import send_from_directory, safe_join
from ..core.branch import Emonic, Response, json, SharedDataMiddleware, Environment, FileSystemLoader, url_encode, Map, base64, os
from ..globals import csrf
from urllib.parse import urljoin, urlencode

app = Emonic(__name__)

def render(template_name, **kwargs):
    template = app.template_env.get_template(template_name)
    kwargs['url_for'] = url_for
    kwargs['csrf_token'] = csrf.generate_csrf_token()
    response = Response(template.render(**kwargs), mimetype='text/html')
    csrf.set_csrf_token_cookie(response, kwargs['csrf_token'])
    return response

# JSON response function
def JsonResponse(data):
    json_data = json.dumps(data)
    return Response(json_data, mimetype='application/json')

# Redirect function
def redirect(location, code=302) -> Response:
    return Response('', status=code, headers={'Location': location})

# URL building function
def url_for(endpoint, **values) -> str:
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            return f'/{app.static_folder}/{filename}'
        else:
            raise ValueError("Static filename not provided")

    elif endpoint == 'redirect':
        location = values.get('location', None)
        if location:
            args = values.get('args', {})
            if args:
                location = urljoin(location, f'?{urlencode(args)}')
            return location
        else:
            raise ValueError("Redirect location not provided")

    elif endpoint == 'user_profile':
        username = values.get('username', None)
        if username:
            return f'/users/{username}'
        else:
            raise ValueError("Username not provided")

    elif endpoint == 'article':
        article_id = values.get('article_id', None)
        if article_id:
            return f'/articles/{article_id}'
        else:
            raise ValueError("Article ID not provided")
    
    elif endpoint == 'category':
        category_name = values.get('category_name', None)
        if category_name:
            return f'/categories/{category_name}'
        else:
            raise ValueError("Category name not provided")
    
    elif endpoint == 'search':
        query = values.get('query', None)
        if query:
            return f'/search?q={urlencode(query)}'
        else:
            raise ValueError("Search query not provided")

    else:
        raise ValueError("Unknown endpoint")

# Send file with headers function
def send_file(filename, mimetype):
    with open(filename, 'rb') as f:
        content = f.read()
    headers = {'Content-Type': mimetype, 'Content-Disposition': f'attachment; filename={os.path.basename(filename)}'}
    return Response(content, headers=headers)

# Middleware for serving static files
def static_engine(static_folder):
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/static': static_folder})

# Set template loader
def template_engine(template_folder):
    app.template_env = Environment(loader=FileSystemLoader(template_folder))

# Save JSON content to a file
def SaveJsonContent(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Redirect with query parameters function
def redirect_args(location, **kwargs):
    query_params = url_encode(kwargs)
    url = f'{location}?{query_params}' if kwargs else location
    return Response(status=302, headers={'Location': url})

# Map routes using rules
def url_map(rules):
    return Map(rules)

# Stream with context function
def stream_with_context(generator_or_function):
    def generate():
        for item in generator_or_function():
            yield item
    return Response(generate())

# Generate a unique key
def make_unique_key():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')

# Encode URLs safely
def url_quote(url, safe='/', encoding=None, errors=None):
    return url_quote(url, safe=safe, encoding=encoding, errors=errors)

def url_quote_plus(url, safe='/', encoding=None, errors=None):
    return url_quote_plus(url, safe=safe, encoding=encoding, errors=errors)

# Join directory paths safely
def safe_join(directory, *pathnames):
    return safe_join(directory, *pathnames)

# Set context processor
def context_processor(f):
    app.template_env.globals.update(f())

# Open resource file
def open_resource(resource):
    return open(resource, 'rb')

# Define template filters
def template_filter(name=None):
    def decorator(f):
        app.template_env.filters[name or f.__name__] = f
        return f
    return decorator

# Set URL defaults for view functions
def url_defaults(f):
    app.url_map.url_defaults(f)

# Get attribute from a template
def get_template_attribute(template_name, attribute):
    return getattr(app.template_env.get_template(template_name), attribute)

# Abort request with HTTPException
def abort(code):
    raise HTTPException(code)

# Make response with appropriate content type
def make_response(response, status=200, headers=None):
    if isinstance(response, (str, bytes)):
        return Response(response, status=status, headers=headers)
    return response