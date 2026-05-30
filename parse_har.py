import json
import urllib.parse
import base64
import re

# The "Target" hash for xemnasvii@gmail.com (SHA-256)
TARGET_HASH = "3961168f1c841446700c02ec035f6063e5e407f3531b40d4ebf949c898b3c375"

trackers = ['facebook', 'google', 'doubleclick', 'tiktok', 'onetrust', 'criteo', 'adroll', 'demdex', 'adobe', 'eyeota', 'advertising']
pii_indicators = ['em', 'email', 'ph', 'fn', 'ln', 'uid', 'fbp', 'fbc', 'guid', 'mid', 'id']

def attempt_decode(value):
    if not isinstance(value, str) or len(value) < 8: return value
    # Handle Base64 padding
    missing_padding = len(value) % 4
    if missing_padding: value += '=' * (4 - missing_padding)
    try:
        decoded = base64.b64decode(value).decode('utf-8', errors='ignore')
        if '{' in decoded: return json.loads(re.search(r'\{.*\}', decoded).group())
        return decoded
    except: return value

with open('evidence.har', 'r', encoding='utf-8') as f:
    log = json.load(f)

print(f"{'TRACKER':<15} | {'PII TYPE':<10} | {'DATA'}")
print("-" * 100)

for entry in log['log']['entries']:
    url = entry['request']['url']
    if any(t in url for t in trackers):
        params = entry['request'].get('queryString', [])
        post_data = entry['request'].get('postData', {}).get('text', '')
        if post_data:
            try:
                parsed_post = urllib.parse.parse_qsl(post_data)
                params.extend([{'name': k, 'value': v} for k, v in parsed_post])
            except: pass

        for p in params:
            name, val = p.get('name', '').lower(), p.get('value', '')
            if any(ind in name for ind in pii_indicators) and len(val) > 5:
                decoded_val = attempt_decode(val)
                tracker_name = next(t for t in trackers if t in url)
                
                # Flag the burner email hash specifically
                status = "!!! STOLEN EMAIL HASH !!!" if TARGET_HASH in str(val) else decoded_val
                print(f"{tracker_name:<15} | {name:<10} | {status}")
