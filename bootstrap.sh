#!/usr/bin/env bash

sudo add-apt-repository ppa:saiarcot895/myppa
sudo apt-get update
sudo apt-get -y install apt-fast

sudo apt-add-repository ppa:brightbox/ruby-ng
sudo chown -R `whoami` /etc/apt/sources.list.d/
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-fast update
sudo apt-fast install -y ruby2.2 ruby2.2-dev git python-pip
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
pip install virtualenv
