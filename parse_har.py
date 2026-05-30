import json

tracker_domains = ['facebook.com', 'google-analytics.com', 'doubleclick.net', 'tiktok.com', 'onetrust.com']

with open('evidence.har', 'r') as f:
    data = json.load(f)

print(f"{'DOMAIN':<25} | {'URL PATH':<40} | {'PARAMS'}")
print("-" * 100)

for entry in data['log']['entries']:
    url = entry['request']['url']
    if any(domain in url for domain in tracker_domains):
        # Extract query parameters
        params = [p['name'] for p in entry['request'].get('queryString', [])]
        clean_url = url.split('?')[0][:40]
        domain = next(d for d in tracker_domains if d in url)
        print(f"{domain:<25} | {clean_url:<40} | {', '.join(params)}")
