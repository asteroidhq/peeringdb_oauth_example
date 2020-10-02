import requests
import urllib.parse
import random
import string
import configparser


class PeeringdbAuth(object):
    """
    Do things with PeeringDB OAuth 2.0
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('/etc/peeringdb_oauth.ini')
        self.OAUTH_CLIENT_KEY = config["peeringdb_oauth"]["oauth_client_key"]
        self.OAUTH_CLIENT_SEC = config["peeringdb_oauth"]["oauth_client_sec"]
        self.redirect_to = config["peeringdb_oauth"]["redirect_to"]
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
        