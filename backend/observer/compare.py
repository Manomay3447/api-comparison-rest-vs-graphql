import requests
import time
import json
import os
import psutil
from datetime import datetime

REST_URL = "http://localhost:5001/users"
GRAPHQL_URL = "http://localhost:5002/graphql"
REPORT_PATH = os.path.join(os.path.dirname(__file__), "report.json")

def measure_rest():
    result = {}
    try:
        start = time.time()
        res = requests.get(REST_URL)
        ttfb = res.elapsed.total_seconds()
        duration = time.time() - start

        result = {
            "duration": duration,
            "ttfb": ttfb,
            "data": res.json(),
            "size": len(res.content),
            "status_code": res.status_code,
            "headers": dict(res.headers),
            "success": True
        }
    except Exception as e:
        result = {
            "duration": None,
            "ttfb": None,
            "data": None,
            "size": 0,
            "status_code": None,
            "headers": {},
            "error": str(e),
            "success": False
        }
    return result

def measure_graphql():
    result = {}
    query = {"query": "{ users { id name email address { city } company { name department } } }"}
    try:
        start = time.time()
        res = requests.post(GRAPHQL_URL, json=query)
        ttfb = res.elapsed.total_seconds()
        duration = time.time() - start

        json_data = res.json()
        users_data = json_data.get("data", {}).get("users", [])

        result = {
            "duration": duration,
            "ttfb": ttfb,
            "data": json_data,
            "user_list": users_data,
            "size": len(res.content),
            "status_code": res.status_code,
            "headers": dict(res.headers),
            "success": True
        }
    except Exception as e:
        result = {
            "duration": None,
            "ttfb": None,
            "data": None,
            "user_list": [],
            "size": 0,
            "status_code": None,
            "headers": {},
            "error": str(e),
            "success": False
        }
    return result

def get_pid_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return int(f.read().strip())
    except Exception:
        return None

def get_process_metrics(pid):
    try:
        p = psutil.Process(pid)

        # Prime the CPU measurement by calling once without interval
        p.cpu_percent(interval=None)
        time.sleep(1)  # Allow time for CPU % to be measured
        cpu = p.cpu_percent(interval=None)
        mem = p.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

        return {"cpu_percent": cpu, "memory_mb": round(mem, 2)}
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return {"cpu_percent": 0, "memory_mb": 0}

def estimate_users():
    users = 0
    for proc in psutil.process_iter(attrs=['cmdline']):
        try:
            cmd = " ".join(proc.info['cmdline'])
            if "load_client.py" in cmd:
                if "--threads" in cmd:
                    idx = cmd.split().index("--threads")
                    threads = int(cmd.split()[idx + 1])
                    users += threads
                else:
                    users += 10  # default threads if not specified
        except Exception:
            continue
    return users

rest_pid = get_pid_from_file("../../rest_api.pid")
graphql_pid = get_pid_from_file("../../graphql_api.pid")

# REST and GraphQL measurement functions (assuming these are defined)
rest_result = measure_rest()
gql_result = measure_graphql()

# Get metrics
rest_metrics = get_process_metrics(rest_pid)
graphql_metrics = get_process_metrics(graphql_pid)

# Record counts
rest_count = len(rest_result["data"]) if rest_result["success"] and rest_result["data"] else 0
graphql_count = len(gql_result["user_list"]) if gql_result["success"] else 0

user_load = estimate_users()
# Timestamp
timestamp = datetime.now().isoformat()

# Construct entry
entry = {
    "timestamp": timestamp,
    "rest": {
        "duration": rest_result["duration"],
        "ttfb": rest_result["ttfb"],
        "count": rest_count,
        "size": rest_result["size"],
        "status_code": rest_result["status_code"],
        "headers": rest_result["headers"],
        "error": rest_result.get("error"),
        "cpu_percent": rest_metrics["cpu_percent"],
        "memory_mb": rest_metrics["memory_mb"]
    },
    "graphql": {
        "duration": gql_result["duration"],
        "ttfb": gql_result["ttfb"],
        "count": graphql_count,
        "size": gql_result["size"],
        "status_code": gql_result["status_code"],
        "headers": gql_result["headers"],
        "error": gql_result.get("error"),
        "cpu_percent": graphql_metrics["cpu_percent"],
        "memory_mb": graphql_metrics["memory_mb"]
    },
    "system": {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_percent": psutil.virtual_memory().percent
    },
    "scalability_users": user_load
}
# Append to report.json file
if os.path.exists(REPORT_PATH):
    with open(REPORT_PATH, "r") as f:
        try:
            report_list = json.load(f)
            if not isinstance(report_list, list):
                report_list = [report_list]
        except json.JSONDecodeError:
            report_list = []
else:
    report_list = []

report_list.append(entry)

with open(REPORT_PATH, "w") as f:
    json.dump(report_list, f, indent=2)

print("Appended new result to:", REPORT_PATH)

