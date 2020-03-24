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


function show_help
{
  echo -e "${green}Example:./cloudlas_start.sh -r <RESOLER> ${none}"
  echo -e "\t\t-r <RESOLVER>: [INT] DoH resolver to use - Options: 1 (Cloudflare), 2 (Google), 3 (CleanBrowsing), 4 (Quad4) - Default: 1"
  exit
}

while getopts "h?s:e:b:r:" opt
do
 case "$opt" in
 h|\?)
   show_help
   ;;
 r)
   RESOLVER=$OPTARG
   ;;
 *)
   show_help
  ;;
 esac
done

if [ -z "$RESOLVER" ]
then
  show_help
fi

DEPS="tshark tcpdump nano tar bzip2 wget gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libxt6"

PYTHON_DEP="python3 python3-six python3-pandas libpython3-dev"


echo -e "Installing requirements..."
apt-get update
apt-get install -y --no-install-recommends $DEPS
apt-get install -y --no-install-recommends $PYTHON_DEPS
dpkg -i source/selenium/python3-urllib3_1.24.1.deb
dpkg -i source/selenium/python3-selenium_3.14.1.deb
apt-get autoremove --purge -y
wget -q https://ftp.mozilla.org/pub/firefox/releases/74.0/linux-x86_64/en-US/firefox-74.0.tar.bz2
tar -xjf firefox-74.0.tar.bz2
tar -xzf source/geckodriver-v0.26.0-linux64.tar.gz
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf selenium/
rm -rf firefox-74.0.tar.bz2
rm -rf geckodriver-v0.26.0-linux64.tar.gz
chmod +x source/geckodriver
chmod +x source/doh_capture.py
chmod +x source/start_doh_capture.sh
cp source/geckodriver /usr/bin
mkdir -p /usr/lib/firefox
ln -s $PWD/firefox/firefox /usr/lib/firefox/firefox
mv source/others/bashrc_template /root/.bashrc
source /root/.bashrc
mkdir -p pcap
