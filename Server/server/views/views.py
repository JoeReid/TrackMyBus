from pyramid.view import view_config

from . import web
from ..lib.auto_format    import action_ok


@view_config(route_name='home')
@web
def my_view(request):
    return action_ok(data={})
