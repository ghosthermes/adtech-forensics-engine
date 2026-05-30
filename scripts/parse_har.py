import json
import urllib.parse
import base64
import re

# Burner hash for xemnasvii@gmail.com
BURNER_HASH = "3961168f1c841446700c02ec035f6063e5e407f3531b40d4ebf949c898b3c375"

trackers = ['facebook', 'google', 'doubleclick', 'tiktok', 'onetrust', 'adobe', 'eyeota', 'demdex']
pii_keys = ['em', 'email', 'uid', 'fbp', 'external_id', 'id', 'cid', 'auid']

def attempt_decode(value):
    if not isinstance(value, str) or len(value) < 10: return value
    # Clean up base64 padding issues
    val_clean = value.strip()
    missing_padding = len(val_clean) % 4
    if missing_padding: val_clean += '=' * (4 - missing_padding)
    try:
        decoded = base64.b64decode(val_clean).decode('utf-8', errors='ignore')
        if '{' in decoded: return "[NESTED JSON DATA]"
        return decoded[:40]
    except: return value[:40]

with open('evidence.har', 'r', encoding='utf-8') as f:
    log = json.load(f)

print(f"{'TRACKER':<15} | {'PII TYPE':<12} | {'DATA/SIGNAL'}")
print("-" * 80)

for entry in log['log']['entries']:
    url = entry['request']['url']
    if any(t in url for t in trackers):
        params = entry['request'].get('queryString', [])
        post_data = entry['request'].get('postData', {}).get('text', '')
        if post_data:
            try:
                params.extend([{'name': k, 'value': v} for k, v in urllib.parse.parse_qsl(post_data)])
            except: pass

        for p in params:
            name, val = p.get('name', '').lower(), str(p.get('value', ''))
            if any(k in name for k in pii_keys) and len(val) > 4:
                tracker_name = next(t for t in trackers if t in url)
                
                # Check for the burner hash specifically
                if BURNER_HASH in val:
                    display_val = "!!! MATCH: XEMNASVII EMAIL HASH !!!"
                else:
                    display_val = attempt_decode(val)
                
                print(f"{tracker_name:<15} | {name:<12} | {display_val}")
