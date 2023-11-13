# EveryDollar Selenium Api
Selenium based API for interacting with the EveryDollar budget app's website

I made this because I needed to import transactions from a bank that wasn't
supported by the app

# Usage
All functions are encapsulated by the EveryDollarAPI class

### `EveryDollarAPI.login(username, password)`
Logs in to the EveryDollar web page, this must be done first

### `EveryDollarAPI.add_transaction(date, merchant, amount, type)`
Adds an uncategorized transaction to the account
- date - datetime object (only month, day, and year are used)
- merchant - string representing who was paid
- amount - float - the transaction amount
- type - string - the transaction type: expense or income