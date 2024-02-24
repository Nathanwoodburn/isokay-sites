#!/bin/bash

# Make sure script is running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Install nginx
sudo apt update
sudo apt install nginx python3-pip -y

cd /root
git clone https://git.woodburn.au/nathanwoodburn/hns-links.git
cd hns-links
mkdir avatars
mkdir sites
cp example/example.json sites/example.json
cp example/example.jpg avatars/example.jpg
chmod +x *.sh
python3 -m pip install -r requirements.txt

# Install python script as a service
sudo cp ./hns-links.service /etc/systemd/system/hns-links.service
sudo systemctl start hns-links
sudo systemctl enable hns-links