# peeringdb_oauth_example

This is an EXAMPLE Python 3 library which implements the OAuth 2.0 PeeringDB service, in the manner based on a presentation by Barry O'Donovan of INEX: https://indico.uknof.org.uk/event/48/contributions/704/attachments/938/1245/uknof45-202001-oauth-for-netops.pdf

It's designed to be lightweight, it only relies on Python's requests library.

If you use Flask you might use it in the way described in this README.  Note if you have a web application with user interactions done on a frontend and business operations done on a backend API, your frontend app might do step 2 and 3, and your backend api might do step 4.

## Step 1: Register your app on PeeringDB

Example on Slide 7 of the above preso (remember the redirect URIs need to be HTTPS)
Copy the file etc/peeringdb_oauth.ini to /etc/peeringdb_oauth.ini and copy/paste the client ID and secret in that the PeeringDB website provides you when you register your app.

## Step 2: Make your endpoint which redirects users to the PeeringDB Auth service:

Based on Slide 9 of the above preso

The library also generates a pseudo random code to use as the state for later comparison.  You should store that somewhere, this example suggests a Flask session.

```
from peeringdb_oauth import PeeringdbAuth

@app.route('/login/peeringdb')
def auth_login_peeringdb():
    session.clear()
    p = PeeringdbAuth()
    peeringdb_redirect = p.calculate_redirect_url()
    session['login_oauth_state'] = peeringdb_redirect["state"]
    return redirect(peeringdb_redirect["redirect"])
```

## Step 3: Make your endpoint which receives the callback from the end user:

Based on slide 12 of the above preso. We swap this access code for a token we can use to ask questions about the user

```
@app.route('/login/peeringdb/callback')
def auth_login_peeringdb_callback():
    if session['login_oauth_state'] != request.args.get('state'):
        abort(400, description="The OAuth state does not match")
    peering_db_code = request.args.get('code')
    p = PeeringdbAuth()
    try:
        peeringdb_token = p.get_access_token(peering_db_code)
    except RuntimeError as err:
        abort(403, description="{}".format(err))
    # Implement your successful login stuff
    # You will need the values in peeringdb_token["access_token"] 
    # and peeringdb_token["refresh_token"], maybe store them somewhere
```

## Step 4: Use the access token to get the user information to log in the user to your app

