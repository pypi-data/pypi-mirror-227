# Test

import requests

url = "http://68.183.93.228:5000/api/v1/call/status"

res = requests.get(url, json={
    "from": "917428730000",
    "to": "917428730000",
    "ring_url": "https://www.google.com",
},
headers={
    "Authorization":"#hLduv5SAu!HIA3pTGfBTwjdjPx-7?9mfnIsCRD7K8omkGLbw4LdW!XqD4XBnYLZqo5EivYZ1qE0ux8F"
})
print(res.text)