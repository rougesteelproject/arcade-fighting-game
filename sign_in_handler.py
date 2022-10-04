import json
import logging
import requests
from requests.exceptions import HTTPError

import constants

class SignInHandler():
    def __init__(self) -> None:
        pass

    def sign_in_email_pass(self, email, password):
    #Credit to Bob Thomas on medium.com
        request_url = "%s:signInWithPassword?key=%s" % (constants.FIREBASE_REST_API, constants.FIREBASE_API_KEY)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        
        resp = requests.post(request_url, headers=headers, data=data)
        # Check for errors
        try:
            resp.raise_for_status()
        except HTTPError as e:
            logging.exception(resp.text)
            
        return resp.json()