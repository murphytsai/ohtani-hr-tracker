import requests
import json

OHTANI_ID = 660271

res = requests.get(f"https://statsapi.mlb.com/api/v1/people/{OHTANI_ID}/stats?stats=gameLog&group=hitting&gameType=R&season=2024").json()
print("Keys:", res.keys())
if 'stats' in res and len(res['stats']) > 0:
    print("Splits count:", len(res['stats'][0].get('splits', [])))
else:
    print(res)
