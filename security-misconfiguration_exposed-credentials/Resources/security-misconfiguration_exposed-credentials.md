# Accès Administratif via Exposition de Configuration et Faiblesse de Hachage

## Identification de la Vulnérabilité

Lors de l'audit du serveur, un répertoire nommé `/whatever/` a été identifié. Ce dernier contenait un fichier `.htpasswd` accessible en lecture sans aucune restriction d'accès. Ce fichier est normalement utilisé par le serveur Apache pour stocker les identifiants de sécurité. L'exposition de ce fichier constitue une fuite de données sensibles majeure.

## Analyse de l'Exploitation

Le fichier contenait la ligne suivante : `root:437394baff5aa33daa618be47b75cb49`.
Le mot de passe de l'utilisateur "root" était protégé par un hachage **MD5**. En raison de l'ancienneté de cet algorithme, il est vulnérable aux attaques par "Rainbow Tables". Le hachage a été soumis à une base de données de correspondance (CrackStation), révélant instantanément le mot de passe en clair : `qwerty123@`.

Ces identifiants ont ensuite été utilisés pour s'authentifier sur l'interface d'administration du site située à l'adresse `/admin/`.

## Exploitation

1. **Extraction :** Téléchargement du fichier depuis `http://localhost:8080/whatever/.htpasswd`.
2. **Cracking :** Décodage du hash MD5 `437394baff5aa33daa618be47b75cb49` pour obtenir `qwerty123@`.
3. **Authentification :** Saisie des identifiants sur la page de connexion `?page=signin` ou directement sur `/admin/`.

## Flag

Après l'authentification sur le panneau d'administration, le flag suivant a été généré :

**Flag :** `d19b4823e0d5600ceed56d5e896ef328d7a2b9e7ac7e80f4fcdb9b10bcb3e7ff`

## Vulnérabilités et préventions

### Classification OWASP

* **A05:2021-Security Misconfiguration** : Exposition de fichiers de configuration critiques (.htpasswd).
* **A07:2021-Identification and Authentication Failures** : Utilisation de mots de passe faibles et d'un algorithme de hachage obsolète.

### Pourquoi cela fonctionne ?

Le serveur n'était pas configuré pour bloquer l'accès aux fichiers cachés (`.ht*`). De plus, l'utilisation d'un mot de passe trivial présent dans les dictionnaires d'attaque a rendu la protection cryptographique (MD5) totalement inefficace.

### Remédiation

* **Bloquer l'accès aux fichiers sensibles** : Configurer les règles du serveur web pour interdire l'accès aux fichiers de configuration et de mots de passe.
* **Renforcer le hachage** : Utiliser des algorithmes modernes et lents comme **bcrypt** ou **Argon2** avec un "sel" (salt) unique par utilisateur.
* **Politique de complexité** : Exiger des mots de passe robustes pour les comptes à hauts privilèges (root/admin).
