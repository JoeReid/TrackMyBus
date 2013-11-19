import re

from pyramid.config import Configurator

from .lib.auto_format import registered_formats


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    
    # Beaker Session Manager
    import pyramid_beaker
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # Routes
    def append_format_pattern(route):
        return re.sub(r'{(.*)}', r'{\1:[^/\.]+}', route) + r'{spacer:[.]?}{format:(%s)?}' % '|'.join(registered_formats())
    
    config.add_route('home'          , append_format_pattern('/')              )
    
    config.scan()
    return config.make_wsgi_app()
