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
  echo -e "\t\t-s <START>: [INT] First website from Alexa's top 1M - Default: 1"
  echo -e "\t\t-e <END>:   [INT] Last website from Alexa's top 1M - Default: 5000"
  echo -e "\t\t-b <BATCH_SIZE>: [INT] Websites/batch - Default:200"
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
 s)
   START=$OPTARG
   ;;
 e)
   END=$OPTARG
   ;;
 b)
   BATCH=$OPTARG
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

DEPS="tshark tcpdump nano tar bzip2 wget gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libxt6 screen procps"

PYTHON_DEPS="python3 python3-six python3-pandas python3-simplejson libpython3-dev"

sudo echo -e "\n\n${reverse}${red}Installing is still in progess...!${disable}${none}" | sudo tee /etc/motd

echo -e "Installing requirements..."
sudo add-apt-repository ppa:wireshark-dev/stable -y
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $DEPS
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $PYTHON_DEPS
# sudo cd /local/repository/
sudo dpkg -i /local/repository/source/selenium/python3-urllib3_1.24.1.deb
sudo dpkg -i /local/repository/source/selenium/python3-selenium_3.14.1.deb
#sudo apt-get autoremove --purge -y
sudo wget -q https://ftp.mozilla.org/pub/firefox/releases/74.0/linux-x86_64/en-US/firefox-74.0.tar.bz2
sudo tar -xjf firefox-74.0.tar.bz2 -C /local/repository
sudo tar -xzf /local/repository/source/geckodriver-v0.26.0-linux64.tar.gz -C /local/repository
#sudo apt-get clean
#sudo rm -rf /var/lib/apt/lists/*
# sudo rm -rf selenium/
# sudo rm -rf firefox-74.0.tar.bz2
# sudo rm -rf geckodriver-v0.26.0-linux64.tar.gz
sudo chmod +x /local/repository/geckodriver
sudo chmod +x /local/repository/source/doh_capture.py
sudo chmod +x /local/repository/source/start_doh_capture.sh
sudo cp /local/repository/geckodriver /usr/bin
sudo rm -rf /usr/lib/firefox
sudo mkdir -p /usr/lib/firefox
sudo ln -s /local/repository/firefox/firefox /usr/lib/firefox/firefox
sudo mv /local/repository/source/*.py /local/repository/
sudo mkdir -p /local/repository/pcap
sudo mv /local/repository/source/*.sh /local/repository/
sudo mv /local/repository/source/*.csv /local/repository/
sudo touch /etc/motd
sudo cp /local/repository/source/others/bashrc_template /root/.bashrc
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
