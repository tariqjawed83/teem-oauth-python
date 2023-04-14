# Teem OAUTH QuickStart using Python

Follow these steps to create a simple Python command-line app that makes requests to Teem's APIs.

## Prerequisites

To run this quickstart, you'll need:

1. Python 2.6 or greater
2. [pip](https://pypi.python.org/pypi/pip) package management tool - To install OAUTH management packages.
3. A Teem Developer Account (API Key and Secret)

Assuming you have your App Name, Client ID, and Client Secret, you can setup the quickstart on your local machine.

## Step 1: Install required packages via `pip`

Run the following command to install the Python packages used for OAUTH:

    $ pip install --upgrade requests_oauthlib

## Step 2: Set up your QuickStart App

  Update `CLIENT_ID` and `CLIENT_SECRET` with your App's ID and Secret from Step 1 in the quickstart/quickstart.py

## Step 3: Run your app

Run your app with the following command:

    $ python quickstart.py

1. If you are running the app for the first time, the app will open your browser and ask to connect to your Teem Login Screen. 

> Log in with your user account (if needed).

2. Click the `Grant Access` button.

3. Your app will continue automatically, and you may close the window/tab.

**Done!** Your app will print the API response.


## Try this next...

### Notes

* Authorization information is stored on the file system, so subsequent executions will not prompt for authorization.
* The authorization flow in this example is designed for a command-line application only.
