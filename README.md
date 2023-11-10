# What is LIDS?

The software product to be produced is a Lightweight Intrusion Detection System (LIDS) specifically designed to cater to the needs of the Cyber Experimentation and Analysis Division (CEAD) within the U.S. Army Combat Capabilities Development Command (DEVCOM) Analysis Center (DAC). 

LIDS aims to monitor and secure network traffic by identifying and reporting malicious and anomalous packets files within a network. Developed after an extensive needs analysis, the system focuses on efficiency and reliability in intrusion detection. While LIDS will proactively detect potential threats and alert the CEAD security team, it will not perform direct remediation. As a vital component of the DEVCOM Analysis Center's cyber capabilities, LIDS offers top-level benefits such as the reduced risk of data breaches, enhanced network visibility, and improved incident response times. By ensuring the confidentiality, integrity, and availability of the network, LIDS aims to provide a reliable, cost-effective, and user-friendly solution that strengthens the cyber defense posture of the U.S. Army DEVCOM Analysis Center.

# How To Run Lids App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

The steps to run LIDS and LIDS-D will have the same instructions, but lids will be replaced with lids-d

# Needed Installs for Running Program
### `flask`
### `flask_cors`
### `axios`

In the project directory, you can run doing these two steps:

# How To Run Lids CLI
### `open lids-app folder`

Then activate the server:
### `open server`
### `python run main.py`

Open a seperate terminal and activate the front end client:
### `open client`
### `npm install`
### `npm start`

# How To Run LIDS D
### `open lids-d-app folder`

Then activate the server:
### `open server`
### `python run main.py`

Open a seperate terminal and activate the front end client:
### `open client`
### `npm install`
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.

# How To Run Lids CLI
In the project directory, you can run:
### `LIDS-CLI.py`

Wireshark needs to be installed in your machine in order to use pyshark.
Pyshark is used to capture packets. 
Import pyshark using 'pip install pyshark' and insert wireshark to your machine's main PATH.


