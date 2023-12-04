# Lightweight Intrusion Detection System

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Introduction
This is a lightweight Intrusion Detection System (IDS) designed to provide security monitoring and intrusion detection capabilities for your network. LIDS is composed of three parts: Lightweight Intrusion Detection System (LIDS), Lightweight Network Intrusion Detection System (LNIDS), and Lightweight Intrusion Detection System-Distributed (LIDS-D).

#### Lightweight Intrusion Detection System (LIDS):

The LIDS agent detects alerts (malicious network interactions) and is meant to be lightweight on
resource consumption, and terminal and graphic interfaces. This is a detection system that monitors
network traffic on the DAC cyber analyst’s computer and produces alerts when malicious network
packets are detected. The LIDS agent stores both malicious network packets and alerts in the DAC cyber
analyst’s computer. The LIDS agent sends alerts to the LIDS-D agent. The LIDS agent makes use of a
configuration file to identify whitelist nodes and server connection information. The LIDS agent has a
web-based graphical interface and a Command Line Interface. The LIDS system may have several
instances of LIDS agents.

#### Lightweight Network Intrusion Detection System (LNIDS):

The LNIDS agent detects alerts (malicious network interactions) and is meant to be lightweight on
resource consumption and placed on the network SPAN port. The LNIDS agent storesthe network traffic
in external storage and sends alerts to the LIDS-D agent. The LNIDS agent makes use of a configuration
file to identify whitelist nodes and server connection information. The LIDS system has one LNIDS
agent.

#### Lightweight Intrusion Detection System - Distributed (LIDS-D):

The LIDS-D agent accepts connection requests from all LIDS agents and the LNIDS agent on a network.
The LIDS-D agent stores the alerts received from LIDS agents and the LNIDS agent. The LIDS-D agent
notifies the DAC cyber analysts of alerts as received and allows analysts to review all the alerts at any
moment, display the list of nodes, save alerts to external storage, and export alerts. The LIDS-D agent
has a Command Line interface and a web-based graphic interface. The LIDS system has one LIDS-D
agent.

## Features
- Monitor network traffic for suspicious activity and detect intrusions in real-time
- Detect and alert on suspicious activity based on a set of rules
- Provide a graphical user interface (GUI) for the LIDS
- Provide a command line interface (CLI) for the LIDS
- Provide a distributed IDS (LIDS-D) that acts as a central server for multiple LIDS clients
- Provide a network IDS (LNIDS) that monitors network traffic for suspicious activity and detects intrusions in real-time

## Getting Started
### Prerequisites
- Have all the prerequisite software installed on your machine. See the installation section for more details.
- Clone the repository to your local machine using the command

### Installation
1. Install the code editor (e.g. [Visual Studio Code](https://code.visualstudio.com/)
2. Install Node.js v18.17.1 and npm v9.6.7 (e.g. [Node.js](https://nodejs.org/en/))
3. Install wireshark (e.g. [Wireshark](https://www.wireshark.org/))
4. Install python3 v3.11.1 (e.g. [Python](https://www.python.org/downloads/))
5. Install MariaDB (e.g. [https://opensource.com/article/20/10/mariadb-mysql-linux)])
6. Create a DataBase called lids-db and import the following SQL script (https://drive.google.com/file/d/1ZZ3n9PAxce2G5Re2bpGLxXiZR5vmeSba/view?usp=share_link)
7. Go to server folder and run:
    pip install -r requirements.txt

If any questions, please follow the installation videos
https://drive.google.com/drive/folders/1Eh6JXX4HZ5pSe2wiky3mZ30KnW1wrfZp?usp=share_link

## Usage
Provide an overview of how to use your IDS, including any command line arguments or options.
LIDS GUI: To run LIDS using the GUI interface, follow the following steps:
1. Open the terminal and nagivate to the "./lids-flask-server"
2. Run the command: "venv\Scripts\activate" to activate the virtual environment for the flask server
3. Open the terminal and navigate to the lids directory
4. Run the command: "npm start"

Your default browser will open and the LIDS GUI will be displayed.

LIDS CLI: To run LIDS using the CLI interface, follow the following steps:
1. Open the terminal and navigate to the "./lids-cli" directory
2. Run the command: "python lids-cli.py"

The LIDS CLI prompt will be displayed in your terminal.

You may use the following commands to interact with the LIDS CLI:

- "start": "Start the LIDS Program",
- "stop": "Stop the LIDS Program",
- "quit": "Exit LIDS",
- "help": "Display help for commands",
- "config": "Configure the LIDS Program with an XML file",
- "dpcap": "Display the most recent pcap",
- "dalerts": "Display alerts",
- "dalert": "Display a specific alert",
- "spcap": "Stop displaying pcaps",
- "replay": "Replay a pcap file"

LIDS-D: To run LIDS-D, follow the following steps:

LNIDS: To run LNIDS, follow the following steps:

## Configuration
To configure the Lightweight Intrusion Detection System, upload an XML configuration file to the system. The configuration file should contain the following information:

- Name: The name of the LIDS agent
- IP Address: The IP address of the LIDS agent
- Port: The port number of the LIDS agent
- Whitelist: The list of IP addresses that are whitelisted
- MAC Address: The MAC address of the LIDS agent

This information will be used as a reference to identify the LIDS agent and whitelist nodes. The configuration file should be uploaded to the system using the LIDS GUI, this will be the first prompt when the LIDS GUI is opened.

To configure the LIDS CLI run the following command when the CLI is launched:
- config
- Enter the path to the config file (e.g. "Path/To/config.xml")

## Contributing
To create a pull request in GitHub and create your own branch, follow these steps:

1. Fork the repository you want to contribute to by clicking the "Fork" button on the repository's page.
2. Clone the forked repository to your local machine using the command: git clone https://github.com/your-username/repository-name.git.
3. Create a new branch for your changes using the command git checkout -b branch-name.

-----------------------------------------------------------------------------------------------------------------------------
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the client folder, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)