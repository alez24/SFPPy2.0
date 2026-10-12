import weakref
import inspect
from jinja2.environment import Environment
from jinja2.utils import LRUCache

orig_get = LRUCache.__getitem__

def wrapped_get(self, key):
    print('LRUCache.__getitem__ key type:', type(key), 'repr:', repr(key))
    try:
        print('hashable?', hash(key))
    except Exception as e:
        print('hash failed:', type(e), e)
        raise
    return orig_get(self, key)

LRUCache.__getitem__ = wrapped_get

from starlette.requests import Request
from survey.app.main import app, templates, current_family

scope = {
    'type': 'http', 'method': 'GET', 'path': '/', 'headers': [],
    'query_string': b'', 'scheme': 'http', 'server': ('testserver', 80),
    'client': ('testclient', 50000), 'root_path': '', 'http_version': '1.1', 'app': app,
}
req = Request(scope)
print('loader:', templates.env.loader)
print('cache before:', templates.env.cache)
key = (weakref.ref(templates.env.loader), 'index.html')
print('key hash', hash(key))
try:
    response = templates.TemplateResponse('index.html', {'request': req, 'family': current_family})
    print('OK', response)
except Exception:
    import traceback
    traceback.print_exc()
finally:
    LRUCache.__getitem__ = orig_get
