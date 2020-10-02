import requests
import urllib.parse
import random
import string

class PeeringdbAuth(object):
    """
    Do things with PeeringDB OAuth 2.0
    """

    def __init__(self):
        self.OAUTH_CLIENT_KEY = "PETL5TEEPnQHoqNwO1WMmNwj4smI04n6OqFoPRPC"
        self.OAUTH_CLIENT_SEC = "9ftHbaWZrTNoSJpM4O4YCrMY42mLSGREOv2caVk6pFM6ELaNNIReghTJoWgWeq6OwEfRxXrhbmfliGat0eHqgS54MbNvvlYnfd00eyZonMdAsK3g79H1gfNGWb3rHhNS"
        self.redirect_to = "https://localhost:5000/auth/login/peeringdb/callback"
        return

    def calculate_redirect_url(self):
        call_to_pdb = {}
        redirect_to = urllib.parse.quote(self.redirect_to)
        call_to_pdb["state"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        call_to_pdb["redirect"] = "https://auth.peeringdb.com/oauth2/authorize/?response_type=code&client_id={}&redirect_uri={}&scope=profile+email+networks&state={}".format(self.OAUTH_CLIENT_KEY, redirect_to, call_to_pdb["state"])
        return call_to_pdb

    def get_access_token(self, auth_code):
        payload = {"grant_type": "authorization_code",
                   "code": auth_code,
                   "redirect_uri": self.redirect_to,
                   "client_id": self.OAUTH_CLIENT_KEY,
                   "client_secret": self.OAUTH_CLIENT_SEC,
                  }

        req = requests.post("https://auth.peeringdb.com/oauth2/token/", data=payload)
        if req.status_code == 200:
            peeringdb_token = req.json()
            print(peeringdb_token)
            return peeringdb_token
        else:
            print("Response from PeeringDB: {}".format(req.status_code))
            print(req.request.body)
            print(req.json())
            raise RuntimeError("PeeringDB returned fault {}".format(req.status_code))
        