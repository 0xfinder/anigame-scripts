# Filter account tokens

import os

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.txt")) as f:
    accountlist = f.read().splitlines()

accounts = []
for i in range(len(accountlist)):
    account = accountlist[i].split(":")
    accounts.append({
        "email": account[0],
        "password": account[1],
        "token": account[2],
    })

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokens.txt"), "w") as f:
    for account in accounts:
        f.write(f"{account['token']}\n")
