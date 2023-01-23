from everydollar_api import EveryDollarAPI
from datetime import datetime

try:
    from creds import username, password
except ImportError:
    import sys
    print("Please create a creds.py file with the variables username and password defined with your everydollar credentials")
    print("")
    print("example creds.py: ")
    print("username = \"my username\"")
    print("password = \"my password\"")
    sys.exit()

api = EveryDollarAPI()
api.login(username, password)
api.add_transaction(datetime.now(), 'This is a test', 123.45)
