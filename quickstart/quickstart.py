# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from requests_oauthlib import OAuth2Session  
import os
import pickle
import json

# Replace with your App's Client ID and Secret
CLIENT_ID     = 'YOUR_CLIENT_ID_HERE'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE'

# If modifying these scopes, delete the file hstoken.pickle.
SCOPES        = ['reservations']

#================================================================
#==== QuickStart Command-line App

def main():

    app_config = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scopes': SCOPES,
        'auth_uri': 'https://app.teem.com/oauth/authorize',
        'token_uri': 'https://app.teem.com/oauth/token/?'
    }

    # The file hstoken.pickle stores the app's access and refresh tokens for the Teem you connect to.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('hstoken.pickle'):
        with open('hstoken.pickle','rb') as tokenfile:
            token = pickle.load(tokenfile)
    # If no token file is found, let the user log in (and install the app if needed)
    else:
        token = InstallAppAndCreateToken(app_config)
        # Save the token for future runs
        SaveTokenToFile(token)

    # Create an OAuth session using your app_config and token
    teem_api = OAuth2Session(
        app_config['client_id'],
        token=token,
        auto_refresh_url=app_config['token_uri'],
        auto_refresh_kwargs=app_config,
        token_updater=SaveTokenToFile
    )

    # Call the 'Get all users' API endpoint
    response = teem_api.get(
            'https://app.teem.com/api/v4/accounts/users'
        )

    # Pretty-print our API result to console
    print(json.dumps(response.json(), indent=2, sort_keys=True))

    print('Here is the acess token: ')
    print(token)

    
#===================================================================
#==== Supporting Functions and Classes used by the command-line app. 

def InstallAppAndCreateToken(config, port=3000):
    """
    Creates a simple local web app+server to authorize your app with a HubSpot hub.
    Returns the refresh and access token.
    """  
    from wsgiref import simple_server
    import webbrowser

    local_webapp = SimpleAuthCallbackApp()
    local_webserver = simple_server.make_server(host='localhost', port=port, app=local_webapp)

    redirect_uri = 'http://{}:{}/oauth/callback/'.format('localhost', local_webserver.server_port)

    oauth = OAuth2Session(
        client_id=config['client_id'],
        scope=config['scopes'],
        redirect_uri=redirect_uri
    )

    auth_url, _ = oauth.authorization_url(config['auth_uri'])
    
    print('-- Authorizing your app via Browser --')
    print('If your browser does not open automatically, visit this URL:')
    print(auth_url)
    webbrowser.open(auth_url, new=1, autoraise=True)
    local_webserver.handle_request()

    # Https required by requests_oauthlib 
    auth_response = local_webapp.request_uri.replace('http','https')

    token = oauth.fetch_token(
        config['token_uri'],
        authorization_response=auth_response,
        # HubSpot requires you to include the ClientID and ClientSecret
        include_client_id=True,
        client_secret=config['client_secret']
    )
    return token

class SimpleAuthCallbackApp(object):
    """
    Used by our simple server to receive and 
    save the callback data authorization.
    """
    def __init__(self):
        self.request_uri = None
        self._success_message = (
            'All set! Your app is authorized.  ' + 
            'You can close this window now and go back where you started from.'
        )

    def __call__(self, environ, start_response):
        from wsgiref.util import request_uri
        
        start_response('200 OK', [('Content-type', 'text/plain')])
        self.request_uri = request_uri(environ)
        return [self._success_message.encode('utf-8')]

def SaveTokenToFile(token):
    """
    Saves the current token to file for use in future sessions.
    """
    with open('hstoken.pickle', 'wb') as tokenfile:
        pickle.dump(token, tokenfile)
        
if __name__ == '__main__':
    main()
