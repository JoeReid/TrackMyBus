import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'pyramid',
    #'pyramid_chameleon',
    'waitress',
    'pyramid_mako',
    'pyramid_tm',
    'pyramid_beaker', # Session/Cache framework - Deprecated by pyramid because it is unmaintained
    'decorator',
    'beautifulsoup4',
    'python-dateutil',
    'dogpile.cache',
    'mock',
    'SQLAlchemy',
    'py-postgresql',
    'transaction',
    'zope.sqlalchemy',
    'py-postgresql',
]
test_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
    #'pudb',  # Won't import, needs compiled stuff
]


setup(name='Server',
      version='0.0',
      description='Server',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires+test_requires,
      tests_require=install_requires+test_requires,
      test_suite="server",
      entry_points="""\
      [paste.app_factory]
      main = server:main
      """,
      )
