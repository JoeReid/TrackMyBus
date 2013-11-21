PROJECT=server

PATH_ASSETS=${PROJECT}/static/ext

INI_DEV  = development.ini
INI_PROD = production.ini


help:
	# TrackMyBus
	#	Bus bus bus busbusbusbusbus

env:
	if dpkg -s python-virtualenv ; then \
		echo virtualenv already installed; \
	else \
		echo installing virtualenv; \
		sudo apt-get install python-virtualenv -y ; \
	fi
	if dpkg -s python3-setuptools ; then \
		echo python 3 already installed; \
	else \
		echo installing python 3; \
		sudo apt-get install python3-setuptools -y ; \
	fi
	virtualenv --no-site-packages -p python3 env
	env/bin/easy_install pyramid

externals:
	env/bin/python $(PROJECT)/scripts/dependency_downloader.py --destination $(PATH_ASSETS)

setup: env
	env/bin/python setup.py develop

install: env setup externals init_db

run: externals
	env/bin/pserve --reload $(INI_DEV)

run_production:
	env/bin/pserve $(INI_PROD)

init_db:
	env/bin/python -mserver.model.setup --config_uri $(INI_DEV) --init_func server.model.init_data:init_data

import_stops:
	env/bin/python -m$(PROJECT).model.setup --config_uri $(INI_DEV) --init_func $(PROJECT).model.init_data:init_data
	env/bin/python -m$(PROJECT).scripts.import_busstops --config=$(INI_DEV)

start_webapp_daemon: ini_vagrant
	start-stop-daemon --start --pidfile webapp.pid --name $(PROJECT) --make-pidfile --background --exec /bin/bash -- -c "$(CURDIR)/env/bin/pserve $(CURDIR)/$(INI_VAGRANT)"
stop_webapp_daemon:
	start-stop-daemon --stop  --pidfile webapp.pid && rm webapp.pid

clean:
	rm -rf webapp.pid
	rm -rf env
	rm -rf $(PATH_ASSETS)
	rm -rf *.egg-info
	rm -rf dependencys_installed.json
	find . -name '*.pyc' -delete
