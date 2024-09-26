#!/bin/bash

sudo apt update -y

# Add deadsnakes PPA to install Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.10, pip, and other dependencies
sudo apt install python3.10 python3.10-venv python3.10-distutils git -y

# Ensure that python3 points to python3.10
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install pip for Python 3.10
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.10

# Verify installation
python3 --version