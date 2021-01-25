# ASCII generator

Front-end to the ASCII generator repo this was forked from.

## Note: 
You can test out the program before V2 here: [pic-2ascii.herokuapp.com](https://pic-2ascii.herokuapp.com/)

V2 will not be pushed to Heroku so as to not incur charges from its [Redis To Go](https://elements.heroku.com/addons/redistogo) addon, which is required for this project to run.

It can be run locally though. You can install it following the instructions below:

## Installation

### Note: This project was done in WSL with Ubuntu 20.04 on a computer running Windows 10.

- Clone the repo and navigate to its folder
- Create a virtual environment

    1. Install pip if you haven't: `sudo apt install -y python3-pip`
    2. Install Python 3's standard virtual environment library: `sudo apt install -y python3-venv`
    3. Create the virtual environment: `python3 -m venv <your_venv_name>`
- Activate the virtual environment: `source <your_venv_name>/bin/activate`
- Install the application's requirements: `pip install -r requirements.txt`

- Get an Imgur Client ID
    1. Navigate to https://api.imgur.com/oauth2/addclient
    2. Get the Client ID
    3. Paste it here in `imageoperations.py`:
    ![Ingur Client ID](https://i.imgur.com/GYa1kpJ.png)

    
## Running the application

- Create two instances of bash
- In the first instance, navigate to the repo's folder
    1. Activate the virtual environment: ` source <your_venv_name>/bin/activate`
    2. Start the redis server: `sudo service redis-server start`
    3. Run the worker: `python worker.py`

- In the second instance,
    1. Activate the virtual environment: ` source <your_venv_name>/bin/activate`
    2. Run the main program: `python main.py`


By:
- [Gokul Viswanath](https://1gokul.github.io/)
- [Shubham Bhagwat](https://shubhamxb.github.io/)
