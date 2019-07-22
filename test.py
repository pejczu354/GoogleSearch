from googleapiclient.discovery import build
from pprint import pprint
from flask import request, jsonify  

my_api_key = "AIzaSyB3kaR6p-JKBhEP8JYBR9Z0WL4lOGeRFWE"
my_cse_id = "010130671253552981765:sv-2jfffhbw"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    print(res.keys())
    print(res['searchInformation'])
    print(res['url'])
    print(request.environ['REMOTE_ADDR'])
    return res['items']

results = google_search(
    'python', my_api_key, my_cse_id, num=10)

pprint(results)