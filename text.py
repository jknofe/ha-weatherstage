import requests

r = requests.get("https://weatherstage.com/ingest/85edb2fe-2573-4013-a725-5ca5df116a6e")

print(r.status_code)
