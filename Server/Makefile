run:
	env/bin/pserve --reload development.ini

setup:
	echo 'setup'
	virtualenv --no-site-packages -p python3 env
	env/bin/pip install pyramid
	env/bin/python3 setup.py develop
