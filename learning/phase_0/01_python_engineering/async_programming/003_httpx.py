# ------------------------------------------------------
# Alhamdulillah
# HTTPX
# ------------------------------------------------------

import requests
import httpx


def print_req_data(req):
    try:
        print(f">> Status Code: {req.status_code}")
    except:
        pass

    try:
        print(f">> Headers    : {req.headers["content-type"]}")
    except:
        pass

    try:
        print(f">> Encoding   : {req.encoding}")
    except:
        pass

    try:
        print(f">> JSON       : {req.json()}")
    except:
        pass

    print()
    print()


print("==> Requests <==")
req = requests.get(
    url = "https://github.com/AAhmeddRRagabb/Agentic-AI",
)

print_req_data(req)


print("==> HTTPX <==")
req_httpx = httpx.get(
    url = 'https://github.com/AAhmeddRRagabb/Agentic-AI'
)

print_req_data(req_httpx)

