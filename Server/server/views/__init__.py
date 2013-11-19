from decorator import decorator
from ..lib.misc            import random_string
from ..lib.pyramid_helpers import request_from_args, etag, etag_decorator, _generate_cache_key_default
from ..lib.auto_format     import auto_format_output

__all__ = [
    'base','auto_format_output','web',
    'etag','etag_decorator', #'etag_generate'
    'method_delete_router', 'method_put_router',
    'cache','cache_none',
]


#-------------------------------------------------------------------------------
# Global Variables
#-------------------------------------------------------------------------------

from dogpile.cache import make_region
from dogpile.cache.api import NO_VALUE as cache_none

cache = make_region().configure(
    'dogpile.cache.memory'
)



#-------------------------------------------------------------------------------
# Base - executed on all calls
#-------------------------------------------------------------------------------
@decorator
def base(target, *args, **kwargs):
    """
    The base instructions to be executed for most calls
    """
    request = request_from_args(args)
    
    # Abort if internal call
    if 'internal_request' in request.matchdict:
        return target(*args, **kwargs)

    # The session id is abstracted from the framework. Keep a count/track id's as session values
    if 'id' not in request.session:
        request.session['id'] = random_string()
    
    #request.session.flash('Hello World %d' % request.session['id'])

    # Enable Pyramid GZip on all responses - NOTE! In a production this should be handled by nginx for performance!
    if request.registry.settings.get('server.gzip'):
        request.response.encode_content(encoding='gzip', lazy=False)
    
    result = target(*args, **kwargs)
    
    return result


#-------------------------------------------------------------------------------
# Web - the decorators merged
#-------------------------------------------------------------------------------
# Reference - http://stackoverflow.com/questions/2182858/how-can-i-pack-serveral-decorators-into-one

def chained(*dec_funs):
    def _inner_chain(f):
        for dec in reversed(dec_funs):
            f = dec(f)
        return f
    return _inner_chain

web  = chained(base, auto_format_output)


#-------------------------------------------------------------------------------
# Predicates
#-------------------------------------------------------------------------------

def method_delete_router(info, request):
    if request.method == 'DELETE' or request.params.get('method','GET').upper() == 'DELETE':
        return True

def method_put_router(info, request):
    if request.method == 'PUT' or request.params.get('method','GET').upper() == 'PUT':
        return True


#-------------------------------------------------------------------------------
# eTag
#-------------------------------------------------------------------------------
def generate_cache_key(request):
    if request.session.peek_flash():
        raise LookupError  # Response is not cacheable/indexable if there is a custom flash message
    return '-'.join([_generate_cache_key_default(request)])

