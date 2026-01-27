# Injection XSS Réfléchie (Contournement via Data URI)

## Identification de la Vulnérabilité

La page `?page=media` utilise un paramètre `src` pour charger dynamiquement des ressources dans une balise HTML `<object>`. Une analyse du code source a révélé que les tentatives d'injection standard (utilisant des balises `<script>` ou des guillemets) sont neutralisées par le serveur, qui transforme les caractères spéciaux en entités HTML (ex: `&lt;`, `&quot;`). Cependant, le serveur ne valide pas le protocole (schéma) utilisé dans l'URL.

## Analyse de l'Exploitation

Pour contourner la protection par filtrage de caractères, l'utilisation du schéma `data:text/html;base64` est privilégiée. Ce protocole permet d'embarquer directement du contenu HTML/JavaScript encodé en Base64. Comme la chaîne encodée ne contient aucun caractère spécial (`<`, `>`, `"`), elle traverse le filtre du serveur sans être modifiée. Une fois arrivée sur le navigateur, ce dernier décode la ressource et exécute le script.

## Exploitation

L'attaque a été réalisée en injectant le payload suivant dans le paramètre `src` de l'URL :

`?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==`

* **Chaîne décodée :** `<script>alert(1)</script>`
* **Structure finale générée :** `<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></object>`

Le navigateur interprète l'objet, décode le JavaScript et l'exécute immédiatement.

## Flag

Suite à l'exécution du script, le système a généré le flag suivant :

**The flag is : 928d819fc19405ae09921a2b71227bd9aba106f9d2d37ac412e9e5a750f1506d**

## Vulnérabilités et préventions

### Classification OWASP

* **A03:2021-Injection** : Inclusion de contenu actif via des vecteurs d'encodage non sécurisés.

### Pourquoi cela fonctionne ?

La faille réside dans une stratégie de défense reposant uniquement sur le nettoyage des caractères spéciaux (blacklisting) plutôt que sur la validation stricte de la nature de la ressource. En omettant de vérifier le protocole de l'URL, le serveur laisse la porte ouverte à l'injection de données autonomes exécutables.

### Remédiation

* **Validation de protocole (Whitelist)** : Restreindre le paramètre `src` aux protocoles sécurisés (`https://`) ou aux chemins relatifs internes.
* **Content Security Policy (CSP)** : Implémenter une directive `object-src 'self'` pour interdire le chargement de données via le schéma `data:`.
* **Sanitization stricte** : Utiliser des bibliothèques de nettoyage de contenu (comme DOMPurify) si l'insertion de HTML dynamique est nécessaire.
