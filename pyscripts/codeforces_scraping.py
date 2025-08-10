import json
import time
import hashlib
import requests
import random
from environ import Env
# Your Codeforces API keys
env = Env(
    # Set default values for environment variables
    CF_API_KEY=(str),
    CF_SECRET_API_KEY=(str),
)
API_KEY = env("CF_API_KEY")
API_SECRET = env("CF_SECRET_API_KEY")
rand = str(random.randint(100000, 999999))  # Random number for signature
t = str(int(time.time()))

contestId = 2128
#params for getting contest question
params = {
    'contestId': contestId,
    'from': 1,
    'count': 1,
}
methodName = "contest.standings"

#params to get user submissions

params = {
    'handle': 'salaarsenpai',
    'from': 1,
    'count': 1,
}
methodName = "user.status"


#ye part sabme same
def preparation(methodName, params):
    params['apiKey'] = API_KEY
    params['time'] = t
    sorted_params_string = '&'.join([f"{k}={params[k]}" for k in sorted(params.keys())])
    signature_base = f"{rand}/{methodName}?{sorted_params_string}#{API_SECRET}"
    sha512_hash = hashlib.sha512(signature_base.encode('utf-8')).hexdigest()
    apiSig = rand + sha512_hash
    params['apiSig'] = apiSig
    url = f"https://codeforces.com/api/{methodName}"
    response = requests.Request('GET', url, params=params)
    response = requests.get(url, params=params)
    return response.json()

def check_user(username, contestId, index):
    userparams = {
        'handle': username,
        'from': 1,
        'count': 3,
    }
    usermethodName = "user.status"

    user_submissions = preparation(usermethodName, userparams)
    # return user_submissions
    for i in range(len(user_submissions['result'])):
        if user_submissions['result'][i]['contestId'] == contestId and user_submissions['result'][i]['problem']['index'] == index and user_submissions['result'][i]['verdict'] == 'OK':
            return True

    return False

# ans = check_user('salaarsenpai', 1890, 'A')
# print(ans)