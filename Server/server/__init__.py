import re

from pyramid.config import Configurator

# SQLAlchemy imports
from .model import init_DBSession

from .lib.auto_format import registered_formats
from .lib.misc import convert_str_with_type


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    init_DBSession(settings)
    
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    
    # Beaker Session Manager
    import pyramid_beaker
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    
    # Parse/Convert setting keys that have specifyed datatypes
    for key in config.registry.settings.keys():
        config.registry.settings[key] = convert_str_with_type(config.registry.settings[key])

    
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # Routes
    def append_format_pattern(route):
        return re.sub(r'{(.*)}', r'{\1:[^/\.]+}', route) + r'{spacer:[.]?}{format:(%s)?}' % '|'.join(registered_formats())
    
    config.add_route('home'           , append_format_pattern('/')               )
    config.add_route('position_update', append_format_pattern('/position_update'))
    config.add_route('position_get'   , append_format_pattern('/position_get')   )
    config.add_route('last_checkin'   , append_format_pattern('/last_checkin')   )
    
    config.scan()
    return config.make_wsgi_app()
