import requests
import re
import time

BASE_URL = "http://localhost:8080"
START_URL = f"{BASE_URL}/.hidden/"
FLAG_PATTERN = re.compile(r'[0-9a-f]{64}')
REQUEST_DELAY = 0.01

def find_flag_sequential():
    queue = [START_URL]
    visited = set()
    start_time = time.perf_counter()
    request_count = 0
    
    print(f"[*] Démarrage SÉQUENTIEL...")

    while queue:
        current_url = queue.pop(0)
        if current_url in visited: continue
        
        visited.add(current_url)
        request_count += 1

        req_start = time.perf_counter()
        try:
            r = requests.get(current_url, timeout=5)
            duration = time.perf_counter() - req_start
            print(f"[{request_count}] ({duration:.3f}s) Check: {current_url}")

            if FLAG_PATTERN.search(r.text):
                total_time = time.perf_counter() - start_time
                print(f"\n[!!!] FLAG TROUVÉ : {FLAG_PATTERN.search(r.text).group(0)}")
                print(f"[!] Temps total : {total_time:.2f} secondes pour {request_count} requêtes.")
                return

            if current_url.endswith('/'):
                links = re.findall(r'<a href="([^"]+)">', r.text)
                for link in links:
                    if link not in ["../", "./"]:
                        queue.append(current_url + link if current_url.endswith('/') else current_url + '/' + link)

        except Exception as e:
            print(f"[-] Erreur sur {current_url}: {e}")

        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    find_flag_sequential()