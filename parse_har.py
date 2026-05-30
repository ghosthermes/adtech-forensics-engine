import json
from urllib.parse import urlparse

with open('evidence.har', 'r') as f:
    log = json.load(f)

found_domains = set()
for entry in log['log']['entries']:
    domain = urlparse(entry['request']['url']).netloc
    found_domains.add(domain)

print("TOP 20 DOMAINS CAPTURED:")
for d in sorted(list(found_domains))[:20]:
    print(f" - {d}")

# Expanded whitelist for litigation targets
trackers = ['facebook', 'google', 'doubleclick', 'tiktok', 'onetrust', 'criteo', 'adroll', 'demdex', 'omtrdc', 'adobe', 'marketing', 'pixel']
pii_indicators = ['em', 'email', 'ph', 'fn', 'ln', 'uid', 'fbp', 'fbc', 'guid', 'mid']

print(f"\n{'TRACKER':<15} | {'PII FOUND':<10} | {'URL PATH'}")
print("-" * 80)

for entry in log['log']['entries']:
    url = entry['request']['url']
    if any(t in url for t in trackers):
        params = [p['name'] for p in entry['request'].get('queryString', [])]
        found_pii = [p for p in params if p in pii_indicators]
        
        tracker_name = next(t for t in trackers if t in url)
        pii_signal = "YES" if found_pii else "no"
        print(f"{tracker_name:<15} | {pii_signal:<10} | {url[:50]}...")
