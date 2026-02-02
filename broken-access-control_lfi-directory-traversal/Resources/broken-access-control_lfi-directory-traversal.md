# Traversée de Répertoire (Local File Inclusion - LFI)

## Description de la faille

L'application utilise un paramètre `page` dans l'URL pour déterminer quel contenu afficher. Cependant, elle ne filtre pas les séquences de remontée de répertoire (`../`). Cette vulnérabilité, appelée **Local File Inclusion (LFI)**, permet à un attaquant d'accéder à des fichiers sensibles situés en dehors de l'arborescence du site web, sur le système de fichiers du serveur.

## Méthode d'exploitation

L'objectif est de remonter jusqu'à la racine du système Linux pour lire un fichier dont le chemin est connu, comme `/etc/passwd` (qui contient la liste des utilisateurs du système).

1. **Analyse de l'URL :** `http://localhost:8080/index.php?page=home`
2. **Injection du Payload :** En utilisant plusieurs séquences `../`, on force le serveur à sortir du répertoire `/var/www/html/...` pour atteindre la racine.
3. **URL d'attaque :**
`http://localhost:8080/index.php?page=../../../../../../../etc/passwd`

## Résultat

Le serveur a interprété la requête et, au lieu d'afficher une erreur, a détecté la tentative d'accès à un fichier système critique, ce qui a déclenché l'affichage du flag.

**Flag :** `b12c4b2cb8094750ae121a676269aa9e2872d07c06e429d25a63196ec1c8c1d0`

## Pourquoi cela fonctionne ?

La fonction côté serveur (probablement `include()` ou `require()` en PHP) prend la chaîne de caractères fournie dans l'URL et l'utilise directement comme chemin d'accès. Comme il n'y a pas de "liste blanche" des pages autorisées, le système d'exploitation résout le chemin relatif fourni par l'attaquant et accède au fichier demandé.

## Remédiation

* **Utiliser une Liste Blanche (Whitelist) :** Ne permettre que des valeurs prédéfinies pour le paramètre `page` (ex: `home`, `contact`, `about`).
* **Désactiver l'accès aux fichiers distants :** Configurer PHP pour empêcher l'inclusion de fichiers via des URLs (`allow_url_include = Off`).
* **Sanitisation :** Utiliser la fonction `basename()` pour ne garder que le nom du fichier et ignorer les chemins ou les séquences de remontée.
* **Chroot Jail :** Isoler l'application web dans un environnement où elle n'a physiquement pas accès au reste du système Linux.