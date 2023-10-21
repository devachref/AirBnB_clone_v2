#!/bin/bash

# Update the package manager and install necessary development tools
sudo apt-get update
sudo apt-get install -y build-essential libffi-dev libssl-dev python3-dev python3-pip python3-venv

# Create a Python 3 virtual environment
python3 -m venv server

# Activate the virtual environment
source server/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages and dependencies
pip install pyparsing appdirs setuptools==40.1.0 cryptography==2.8 bcrypt==3.1.7 PyNaCl==1.3.0 Fabric3==1.14.post1

# Deactivate the virtual environment when you're done
deactivate