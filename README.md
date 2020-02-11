# Linux Package Info Browser Web Application

_Developed by Matheos Mattsson_

## About
This small web application was made as a pre-assignment for a job application to [Reaktor](https://www.reaktor.com/). At the time of writing I have a live version running for demonstration purposes on Heroku: https://linux-pkg-info.herokuapp.com/

The purpose of this application is for it to run on a Linux machine and read the Linux package info file _status_ located at _/var/lib/dpkg/status_ on Debian based distributions. The web application provides an easy to use and simplistic list interface which lists all the installed packages. Each package in the list links to its own package specific information page where package name, description, dependencies and, by the app itself calculated, reverse dependencies (list of packages that the depend on the package in question). The interface also allows the user to view package specific info for the listed dependencies and reverse dependencies straight from another package's info page.

The application is written in Python using the Flask framework. The implementation could probably be simplified with the use of more external libraries but as stated in the assignment, I chose to keep the usage of external libraries to a minimum (Flask and its dependencies being the only ones).

## Requirements
- Python 3.X with pip
- Linux OS

## Setup and run
1. Clone this repository
2. cd into the repository directory and run _pip install -r requirements.txt_ (Tip: Use a virtual environment to not affect your global pip installation)
3. Run the server using _python server.py_
4. The server should now be running on localhost port 80 (can be configured in the .py file)

## Configuration
- The port as well as the server accessability can be configured in the _server.py_ file at the very bottom.
- If you are using a distribution that does not store the _status_ file in the default path, this path can easily be changed by modifying the _FILE_PATH_ variable at the top of the _server.py_ file. 
