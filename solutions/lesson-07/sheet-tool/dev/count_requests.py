"""Count answers from the Service for N seconds: python count_requests.py 40

Run it inside the cluster (see the lesson), so requests go through the Service like real traffic.
"""
import collections
import sys
import time

import httpx

end = time.time() + float(sys.argv[1])
counts = collections.Counter()
with httpx.Client(timeout=5) as client:
    while time.time() < end:
        try:
            counts[client.get("http://sheet-tool.sheet-tool/", headers={"Connection": "close"}).status_code] += 1
        except httpx.HTTPError as error:
            counts[type(error).__name__] += 1
        time.sleep(0.05)
print(dict(counts))
