import json
import subprocess
import time
import sys

repo = "nist0/CoDev"
# tokens to match workflow/run names (lowercase)
tokens = [
    "unit tests",
    "unit-tests",
    "unit tests",
    "routing ci",
    "validate routing",
    "readme-registry",
    "validate-readme-registry",
    "readme registry",
]

def gh_run_list():
    try:
        out = subprocess.check_output([
            "gh", "run", "list", "--repo", repo, "--branch", "main", "--limit", "200",
            "--json", "databaseId,name,status,conclusion,url,createdAt"
        ], text=True)
        return json.loads(out)
    except subprocess.CalledProcessError as e:
        print("ERROR: gh run list failed:", e, file=sys.stderr)
        return []

def gh_run_view(rid):
    try:
        out = subprocess.check_output([
            "gh", "run", "view", str(rid), "--repo", repo, "--json", "databaseId,name,status,conclusion,url,createdAt"
        ], text=True)
        return json.loads(out)
    except subprocess.CalledProcessError as e:
        print("ERROR: gh run view failed for", rid, e, file=sys.stderr)
        return None

print("Scanning recent runs on branch 'main' to find matching workflows...")
found = {}
start = time.time()
# wait up to N seconds to discover runs
discover_timeout = 120
while True:
    runs = gh_run_list()
    for r in runs:
        name = (r.get("name") or "").lower()
        for t in tokens:
            if t in name:
                rid = r.get("databaseId")
                if rid and rid not in found:
                    found[rid] = {"name": r.get("name"), "status": r.get("status"), "conclusion": r.get("conclusion"), "url": r.get("url")}
    if found:
        break
    if time.time() - start > discover_timeout:
        print(f"No matching runs found after waiting {discover_timeout}s; exiting.")
        sys.exit(0)
    time.sleep(5)

print(f"Found {len(found)} matching run(s). Monitoring until completion (timeout 10m)...")
for rid,info in found.items():
    print(f"- {rid}: {info['name']}  status={info['status']} conclusion={info['conclusion']} {info.get('url')}")

# Poll until all complete or timeout
timeout = 600
poll_interval = 8
end = time.time() + timeout
completed = {}
while found and time.time() < end:
    for rid in list(found.keys()):
        info = gh_run_view(rid)
        if not info:
            continue
        status = info.get("status")
        conclusion = info.get("conclusion")
        name = info.get("name")
        url = info.get("url")
        print(f"[{time.strftime('%H:%M:%S')}] Run {rid} - {name}: status={status}, conclusion={conclusion}")
        if status == "completed":
            completed[rid] = {"name": name, "conclusion": conclusion, "url": url}
            del found[rid]
    if not found:
        break
    time.sleep(poll_interval)

print("\nFinal summary:")
for rid,c in completed.items():
    print(f"- {rid}: {c['name']} => {c['conclusion']} {c['url']}")
if found:
    print("\nTimed out waiting for these runs to complete:")
    for rid,info in found.items():
        print(f"- {rid}: {info['name']} (last known status: {info['status']}) {info.get('url')}")
    sys.exit(2)
else:
    sys.exit(0)
