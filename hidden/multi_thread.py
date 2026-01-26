import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8080"
START_URL = f"{BASE_URL}/.hidden/"
MAX_THREADS = 20
FLAG_PATTERN = re.compile(r'[0-9a-f]{64}')

visited = set()
flag_found = None
request_count = 0

def process_url(url):
    global flag_found, request_count
    if flag_found or url in visited: return []
    
    visited.add(url)
    req_start = time.perf_counter()
    try:
        r = requests.get(url, timeout=5)
        duration = time.perf_counter() - req_start
        request_count += 1
        print(f"[{request_count}] ({duration:.3f}s) Thread Check: {url}")

        match = FLAG_PATTERN.search(r.text)
        if match:
            flag_found = (match.group(0), url)
            return []

        if url.endswith('/'):
            links = re.findall(r'<a href="([^"]+)">', r.text)
            return [url + l for l in links if l not in ["../", "./"]]
    except:
        pass
    return []

def find_flag_threaded():
    global flag_found
    start_time = time.perf_counter()
    queue = [START_URL]
    
    print(f"[*] Démarrage MULTI-THREADÉ ({MAX_THREADS} threads)...")
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while queue and not flag_found:
            futures = {executor.submit(process_url, url): url for url in queue}
            queue = []
            for future in as_completed(futures):
                if flag_found: break
                queue.extend(future.result())

    if flag_found:
        total_time = time.perf_counter() - start_time
        print(f"\n[!!!] FLAG TROUVÉ : {flag_found[0]}")
        print(f"[!] Temps total : {total_time:.2f} secondes pour {request_count} requêtes.")

if __name__ == "__main__":
    find_flag_threaded()