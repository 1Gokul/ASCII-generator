# ASCII generator v1.5

Front-end to the ASCII generator repo this was forked from.

This v1.5 version of this app is the version that is hosted on Heroku, as it does not use [RQ](https://nvie.com/posts/introducing-rq/) for performing tasks.

You can test out the app here: [pic-2ascii.herokuapp.com](https://pic-2ascii.herokuapp.com/)

You can install and run it following the instructions below:

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

- Run `main.py`.


By:
- [Gokul Viswanath](https://1gokul.github.io/)
- [Shubham Bhagwat](https://shubhamxb.github.io/)
