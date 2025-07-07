import requests
import time
import threading
import argparse

REST_URL = "http://localhost:5001/users"
GRAPHQL_URL = "http://localhost:5002/graphql"
GRAPHQL_QUERY = {
    "query": """
    {
        users {
            id
            name
            email
            address {
                city
                }
                company {
                    name
                    department
                    }
            }
        }
    }
    """
}

def load_rest(n):
    for _ in range(n):
        try:
            start = time.time()
            res = requests.get(REST_URL)
            print(f"[REST] Status: {res.status_code}, Time: {time.time() - start:.3f}s")
        except Exception as e:
            print(f"[REST] Error: {e}")

def load_graphql(n):
    for _ in range(n):
        try:
            start = time.time()
            res = requests.post(GRAPHQL_URL, json=GRAPHQL_QUERY)
            print(f"[GraphQL] Status: {res.status_code}, Time: {time.time() - start:.3f}s")
        except Exception as e:
            print(f"[GraphQL] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate load on REST and GraphQL APIs")
    parser.add_argument('--threads', type=int, default=10, help='Number of concurrent threads')
    parser.add_argument('--requests', type=int, default=100, help='Number of requests per thread')
    parser.add_argument('--target', type=str, choices=['rest', 'graphql', 'both'], default='both')

    args = parser.parse_args()

    threads = []
    for _ in range(args.threads):
        if args.target in ('rest', 'both'):
            threads.append(threading.Thread(target=load_rest, args=(args.requests,)))
        if args.target in ('graphql', 'both'):
            threads.append(threading.Thread(target=load_graphql, args=(args.requests,)))

    print(f"Launching {len(threads)} threads with {args.requests} requests each...")
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Load testing complete.")

