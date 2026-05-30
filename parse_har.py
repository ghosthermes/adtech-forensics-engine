import json

# Expanded tracker list including common privacy-violating domains
trackers = ['facebook', 'google-analytics', 'doubleclick', 'tiktok', 'onetrust', 'criteo', 'adroll', 'demdex']
# Parameters that usually indicate PII or persistent tracking
pii_indicators = ['em', 'email', 'ph', 'fn', 'ln', 'uid', 'fbp', 'fbc', 'guid']

with open('evidence.har', 'r') as f:
    log = json.load(f)

print(f"{'TRACKER':<15} | {'PII FOUND':<10} | {'URL PATH'}")
print("-" * 80)

for entry in log['log']['entries']:
    url = entry['request']['url']
    if any(t in url for t in trackers):
        params = [p['name'] for p in entry['request'].get('queryString', [])]
        found_pii = [p for p in params if p in pii_indicators]
        
        tracker_name = next(t for t in trackers if t in url)
        pii_signal = "YES" if found_pii else "no"
        print(f"{tracker_name:<15} | {pii_signal:<10} | {url[:50]}...")
