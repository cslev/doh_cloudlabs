#!/bin/bash
#COLORIZING
none='\033[0m'
bold='\033[01m'
disable='\033[02m'
underline='\033[04m'
reverse='\033[07m'
strikethrough='\033[09m'
invisible='\033[08m'

black='\033[30m'
red='\033[31m'
green='\033[32m'
orange='\033[33m'
blue='\033[34m'
purple='\033[35m'
cyan='\033[36m'
lightgrey='\033[37m'
darkgrey='\033[90m'
lightred='\033[91m'
lightgreen='\033[92m'
yellow='\033[93m'
lightblue='\033[94m'
pink='\033[95m'
lightcyan='\033[96m'



DEPS="tshark tcpdump nano tar bzip2 wget lsb-release screen procps apt-transport-https ca-certificates curl gnupg-agent software-properties-common"

PYTHON_DEPS="python3 libpython3-dev"

sudo echo -e "\n\n${reverse}${red}Installing is still in progess...!${disable}${none}" | sudo tee /etc/motd

echo -e "Installing requirements..."
# sudo add-apt-repository ppa:wireshark-dev/stable -y
# sudo apt-get update
# ========== ARM64 ========
#upgrade to focal ubuntu 20.04
#remove any docker container-related installations
#sudo apt-get remove docker docker-engine docker.io containerd runc

sudo dpkg-reconfigure debconf --frontend=noninteractive

sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $DEPS
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $PYTHON_DEPS
# sudo cd /local/repository/
#sudo dpkg -i /local/repository/source/selenium/python3-urllib3_1.24.1.deb
#sudo dpkg -i /local/repository/source/selenium/python3-selenium_3.14.1.deb
#sudo apt-get autoremove --purge -y
#x86_64
#sudo wget -q https://ftp.mozilla.org/pub/firefox/releases/74.0/linux-x86_64/en-US/firefox-74.0.tar.bz2
#sudo tar -xjf firefox-74.0.tar.bz2 -C /local/repository
#sudo tar -xzf /local/repository/source/geckodriver-v0.26.0-linux64.tar.gz -C /local/repository

#ARM64
#sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
#sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
#sudo sed -i 's/bionic/focal/g' /etc/apt/sources.list
#sudo apt-get update

#sudo apt-get dist-upgrade -y --no-install-recommends

#installing docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io

#installing docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

#get doh_docker image
sudo docker pull cslev/doh_docker:latest

#firefox
#sudo wget -q http://launchpadlibrarian.net/468415450/firefox_74.0+build3-0ubuntu0.18.04.1_arm64.deb
#sudo wget -q http://launchpadlibrarian.net/468415270/firefox-geckodriver_74.0+build3-0ubuntu0.18.04.1_arm64.deb
#sudo dpkg -i firefox_74.0+build3-0ubuntu0.18.04.1_arm64.deb
#sudo dpkg -i firefox-geckodriver_74.0+build3-0ubuntu0.18.04.1_arm64.deb
#sudo ln -s `which geckodriver` /local/repository/geckodriver

#========== ARM64 END =================

#sudo rm -rf /var/lib/apt/lists/*
# sudo rm -rf selenium/
# sudo rm -rf firefox-74.0.tar.bz2
# sudo rm -rf geckodriver-v0.26.0-linux64.tar.gz
#sudo chmod +x /local/repository/geckodriver
#sudo chmod +x /local/repository/source/doh_capture.py
#sudo chmod +x /local/repository/source/start_doh_capture.sh
#sudo cp /local/repository/geckodriver /usr/bin
# sudo rm -rf /usr/lib/firefox
#sudo mkdir -p /usr/lib/firefox
# sudo ln -s /local/repository/firefox/firefox /usr/lib/firefox/firefox
#sudo mv /local/repository/source/*.py /local/repository/
#sudo mkdir -p /local/repository/pcap
#sudo mkdir -p /local/repository/csv
#sudo mv /local/repository/source/*.sh /local/repository/
#sudo mv /local/repository/source/*.csv /local/repository/
#sudo mv /local/repository/source/r_config.json /local/repository/
#sudo touch /etc/motd
#sudo cp /local/repository/source/others/bashrc_template /root/.bashrc
sudo source /root/.bashrc
sudo cp /local/repository/source/others/bashrc_template /users/cslev/.bashrc
sudo echo "cslev   ALL= NOPASSWD:/usr/sbin/tcpdump" >> /etc/sudoers
sudo apt-get install -f -y
sudo apt-get autoremove -y

# sudo echo -e "\n\n${reverse}${red}Install tshark manually!${disable}${none}" | sudo tee  /etc/motd
# sudo echo -e "\n\n${reverse}${red}apt-get install tshark -y --no-install-recommends!${disable}${none}" | sudo tee  /etc/motd
# sudo echo -e "\n\n${reverse}${red}mv /local/repository/others/bashrc_template /root/.bashrc!${disable}${none}" | sudo tee  /etc/motd
# sudo echo -e "\n\n${reverse}${red}. /root/.bashrc!${disable}${none}" | sudo tee -a /etc/motd
sudo echo -e "\n\n${reverse}${green}Installation finished\n\$PATH=${PATH}!${disable}${none}" | sudo tee /etc/motd
