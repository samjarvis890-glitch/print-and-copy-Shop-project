import urllib.request
import urllib.parse
import re

query = 'site:unsplash.com/photos "printing press" OR "print shop"'
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
    matches = re.findall(r'unsplash\.com/photos/([a-zA-Z0-9_-]+)', html)
    print("Found photo slugs:", len(matches))
    for m in set(matches)[:10]:
        print(" ", m)
except Exception as e:
    print("Failed:", e)
