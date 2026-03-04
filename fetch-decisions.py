import urllib.request, json, os

TOKEN = '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'
URL = 'https://api.github.com/repos/dubbleoco/OWL/contents/decisions.json'

req = urllib.request.Request(URL, headers={
    'Authorization': 'token ' + TOKEN,
    'Accept': 'application/vnd.github.v3+json'
})
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    import base64
    content = base64.b64decode(data['content']).decode('utf-8')
    with open(os.path.expanduser('~/OWL/decisions.json'), 'w') as f:
        f.write(content)
    print('Fetched decisions.json')
except Exception as e:
    print(f'No decisions to fetch: {e}')
