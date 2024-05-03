import os
import requests

def send_msg_to_ntfy(string: str):
    url = str(os.environ.get('NTFY_URL'))
    key = str(os.environ.get('NTFY_KEY'))
    
    requests.post(url,
    data=string,
    timeout=30,
    headers={
        "Title": "Backup System @ docker.boomnet.homes",
        "Priority": "1",
        "Tags": "boom,desert",
        "Authorization": "Bearer " + key
    })
