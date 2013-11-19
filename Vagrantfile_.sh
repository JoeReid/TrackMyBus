#!/usr/bin/env bash
set -e

# Variables --------------------------------------------------------------------

HOME="/home/vagrant"
SHARE="/vagrant"
GIT_REPO="https://github.com/joe.reid/TrackMyBus.git"
GIT_PROJECT_NAME="TrackMyBus"
INSTALLED_FILE="$HOME/.installed"
# Check if installation required

if [ -e "$INSTALLED_FILE" ]
then
	echo "Install previously completed"
else

# Root Setup -------------------------------------------------------------------

# TODO: FIX THIS
#if dpkg -s git ; then
#    echo "Packages already installed"
#else
    echo "Installing packages"
    apt-get update
    apt-get install -y git make
#fi


# User Setup -------------------------------------------------------------------

sudo -u vagrant sh << EOF
set -e

# Vagrant does not update the HOME env when switching to normal 'vagrant' user
HOME=$HOME
cd $HOME

if [ -e "$GIT_PROJECT_NAME" ]
then
	echo "Codebase already checked out"
else
	git clone $GIT_REPO
fi

# Setup Website Python Project
cd $HOME/$GIT_PROJECT_NAME/server
make install


echo 'Installation complete'
touch $INSTALLED_FILE

EOF

fi


# VM Startup -------------------------------------------------------------------
sudo -u vagrant sh << EOF
set +e
cd $HOME/$GIT_PROJECT_NAME/server
echo 'Updating repo'
git pull
make externals
echo 'Start server daemon'
make start_webapp_daemon
EOF