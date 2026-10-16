# Darkly

> 🇬🇧 [English version](README.md) · 📖 [Glossaire](GLOSSARY.fr.md)

Projet de sécurité web du cursus 42. L'objectif est d'auditer un site volontairement vulnérable (l'ISO `Darkly`, exécutée dans une VM), de trouver **14 vulnérabilités**, de chacune les exploiter pour récupérer un flag, puis de documenter l'exploitation et la correction.

> ⚠️ **Attention spoilers :** chaque write-up `Resources/*.md` contient le flag et toute la démarche d'exploitation.

## Installation

La cible est une VM VirtualBox construite à partir de l'ISO officielle (`Darkly_i386.iso`).

```bash
./vm.sh   # télécharge l'ISO, crée et configure la VM (port forwarding 4242)
```

Le site est ensuite accessible via l'IP de la VM (ou par port forwarding, ex. `http://localhost:8080`).

## Structure du dépôt

Chaque vulnérabilité a son propre dossier, nommé `<catégorie-owasp>_<technique>` :

```
<catégorie-owasp>_<technique>/
├── flag          # le flag obtenu
└── Resources/    # write-up (.md), scripts, wordlists, payloads
```

## Vulnérabilités

| # | Dossier | Technique | OWASP Top 10 (2021) |
|---|---------|-----------|---------------------|
| 1 | `broken-access-control_cookie-tampering` | Forger le cookie `I_am_admin` (hash MD5 faible de `false` remplacé par celui de `true`) | A01 Broken Access Control |
| 2 | `broken-access-control_directory-indexing-bruteforce` | Parcours multi-thread de l'arborescence `/.hidden/` (~18 000 fichiers README) | A01 Broken Access Control |
| 3 | `broken-access-control_hidden-input-manipulation` | Modifier un `hidden input` du formulaire de récupération de mot de passe | A01 Broken Access Control |
| 4 | `broken-access-control_lfi-directory-traversal` | Traversée `../` dans le paramètre `page` pour lire `/etc/passwd` | A01 Broken Access Control |
| 5 | `broken-access-control_open-redirect` | Paramètre `site` non validé dans la fonction de redirection | A01 Broken Access Control |
| 6 | `broken-access-control_parameter-tampering-survey` | Envoyer une note hors limites en modifiant la valeur du `<select>` | A01 Broken Access Control |
| 7 | `broken-access-control_unrestricted-file-upload` | Upload d'un fichier `.php` déguisé en `image/jpeg` | A01 / A04 |
| 8 | `identification-and-authentication-failures_brute-force` | Brute-force du login `admin` (formulaire en GET, pas de rate limiting) avec un script Python | A07 Identification and Authentication Failures |
| 9 | `injection_reflected-xss-data-uri-bypass` | XSS réfléchie via une URI `data:text/html;base64` pour contourner le filtre de caractères | A03 Injection |
| 10 | `injection_sql-union-based` | Injection SQL union-based sur la page member (quotes contournées avec l'hexadécimal) | A03 Injection |
| 11 | `injection_sql-union-search-image` | Injection SQL union-based sur la recherche d'images, puis décodage MD5 et SHA-256 | A03 Injection |
| 12 | `injection_stored-xss-client-bypass` | XSS stockée répartie sur deux champs pour contourner le `maxlength` côté client | A03 Injection |
| 13 | `insecure-design_http-header-tampering` | Falsifier `Referer` et `User-Agent` avec `curl` | A04 Insecure Design |
| 14 | `security-misconfiguration_exposed-credentials` | `.htpasswd` exposé dans `/whatever/`, hash MD5 cassé, connexion sur `/admin/` | A05 Security Misconfiguration |

## Outils utilisés

`curl`, DevTools du navigateur, `hashcat`, CrackStation, Python (`requests`, `ThreadPoolExecutor`), wordlists SecLists.

## Enseignements clés

- Ne jamais faire confiance aux données côté client (cookies, hidden fields, headers, `maxlength`, valeurs de `<select>`) : **valider côté serveur**.
- Utiliser des whitelists pour les chemins de fichiers, les cibles de redirection et les types d'upload.
- Utiliser des prepared statements et l'output encoding contre les injections.
- Ne pas compter sur la sécurité par l'obscurité, ni stocker des secrets avec des hash rapides et cassés comme MD5.
- Mettre en place du rate limiting et un lockout sur les endpoints d'authentification.
