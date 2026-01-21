# Manipulation de Cookie

## Identification de la Vulnérabilité

Lors de l'exploration du site, une inspection des cookies (Outils de développement -> Application -> Cookies) a révélé un cookie nommé `I_am_admin`. La valeur de ce cookie ressemble à une empreinte **MD5**.

* **Nom du cookie :** `I_am_admin`
* **Valeur initiale :** `68934a3e9455fa72420237eb05902327`

## Analyse et Déchiffrement

En utilisant un service de déchiffrement MD5 en ligne ou un outil comme `hashcat`, on peut retrouver la chaîne de caractères originale :

* `68934a3e9455fa72420237eb05902327`  **"false"**

L'application web semble donc vérifier si l'utilisateur est administrateur en comparant simplement la valeur hashée de ce cookie. Pour devenir administrateur, nous devons changer cette valeur par le hash du mot **"true"**.

**Note:**
     Voici la commande utilisée pour hashcat `hashcat -m 0 [hash] [chemin_vers_la_wordlist.txt]`

## Exploitation

Il suffit de générer le nouveau hash MD5 pour la chaîne de caractères "true".

**Génération du MD5 :**

* **Entrée :** `true`
* **Résultat (MD5) :** `b326b5062b2f0e69046810717534cb09`

### Solution

1. Ouvrez le site cible dans votre navigateur.
2. Accédez à la **Console** des outils de développement (F12).
3. Modifiez le cookie directement sur le local storage en mettant la valeur `b326b5062b2f0e69046810717534cb09` dans le cookie `I_am_admin` ou avec la commande JavaScript suivante :
```javascript
document.cookie = "I_am_admin=b326b5062b2f0e69046810717534cb09; path=/";

```
4. **Actualisez** la page (F5).
5. Le serveur valide le nouveau hash et montre le flag

## Flag
`df2eb4ba34ed059a1e3e89ff4dfc13445f104a1a52295214def1c4fb1693a5c3`

## Vulnérabilités et préventions

Cette faille repose sur deux erreurs majeures de sécurité (Insecure Direct Object Reference (IDOR) et Broken Authentication):

###  L'utilisation d'un algorithme obsolète

MD5 n'est plus considéré comme sécurisé car il est trop facile à inverser via des tables de correspondance (Rainbow Tables) et possède beaucoup de collisions (ceci se produit lorsque 2 inputs différents rentre en collision suite au hash). 

Il faut plutôt prioritiser le BCrypt pour qui salt automatiquement (ajout d'un sel unique / ajout de donnée avant le hachage) et unique pour chaque user.
```
$2a$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW
\__/\/ \____________________/\_____________________________/
Alg Cost      Salt                        Hash
```
Le Cost Factor est le nombre d'itération de la fonction, par exemple 12 -> 2^12 = 4096 itérations

### La confiance envers les données client
La règle d'or en sécurité web est que **tout ce qui provient du navigateur de l'utilisateur est potentiellement malveillant**.

* **Mauvaise pratique :** Stocker le rôle (`admin=true`) ou les permissions dans un cookie côté client.
* **Bonne pratique :** Stocker uniquement un **ID de session** unique et aléatoire dans le cookie. Le serveur utilise ensuite cet ID pour vérifier le rôle de l'utilisateur dans sa propre base de données.

**Ex:**
```php
// MAUVAIS : Basé sur le cookie client
if ($_COOKIE['I_am_admin'] === md5("true")) {
    render_admin_panel();
}

// BON : Vérification côté serveur via la session
session_start();
if (isset($_SESSION['user_id'])) {
    $user = $db->getUser($_SESSION['user_id']);
    if ($user->isAdmin()) {
        render_admin_panel();
    }
}
```

### Utiliser des Cookies Sécurisés

Si des informations de session sont stockées dans des cookies, ils doivent être protégés par des attributs spécifiques :

* **HttpOnly :** Empêche l'accès au cookie via JavaScript (évite les vols de session via XSS).
* **Secure :** Garantit que le cookie n'est envoyé que sur des connexions HTTPS chiffrées.
* **SameSite=Strict :** Protège contre les attaques de type CSRF (Cross-Site Request Forgery).

### Une solution moderne : Le JSON Web Token (JWT)

Dans les architectures modernes, on remplace souvent les cookies simples par des **JWT**. Contrairement au cookie de l'exercice `I_am_admin`, un JWT ne repose pas sur le secret du hachage, mais sur la **vérification de l'intégrité**.

Un JWT est composé de trois parties séparées par des points : `Header.Payload.Signature`.

* **Header & Payload :** Ce sont des données lisibles (en Base64). Le pirate peut voir que le cookie contient `"role": "user"`.
* **Signature :** C'est la partie cruciale. Le serveur crée cette signature en combinant le contenu du Header et du Payload avec une **clé secrète** que lui seul connaît.

#### Pourquoi cela bloque l'attaque vue sur Darkly ?

Si un utilisateur tente de modifier manuellement le Payload pour passer de `"role": "user"` à `"role": "admin"`, la signature devient invalide. Comme l'attaquant ne possède pas la clé secrète du serveur, il est incapable de générer une nouvelle signature correspondante. Le serveur rejettera le token dès qu'il tentera de le vérifier.

### Protections Avancées contre le Vol de Session (Anti-Hijacking)

Pour contrer les malwares qui volent les cookies directement sur l'ordinateur de l'utilisateur (outrepassant `HttpOnly`), les standards modernes évoluent :

* **DBS (Device Bound Session Credentials) :** C'est ce qu'on appelle la **Liaison Cryptographique au Dispositif**. Le cookie est lié à une clé privée stockée dans le **TPM** (puce de sécurité) de l'ordinateur. Même si le pirate copie le cookie, il ne possède pas la clé matérielle pour l'utiliser.
* **Analyse Contextuelle et Comportementale :** Le serveur ne se contente plus de vérifier le cookie. Il vérifie l'**Empreinte Numérique (Browser Fingerprinting)** : si l'adresse IP, la résolution d'écran ou le système d'exploitation change brutalement, la session est révoquée.
* **Chiffrement au Repos (Encryption at Rest) :** Les navigateurs utilisent désormais les API natives du système (comme *DPAPI* sur Windows ou *Keychain* sur macOS) pour chiffrer la base de données des cookies. Un malware ne peut donc pas simplement "lire" le fichier sans les privilèges de l'utilisateur connecté.

### Résumé des bonnes pratiques (Checklist)

1. **Ne jamais stocker de logique métier dans le cookie** (ex: `is_admin=true`).
2. **Signer les cookies** : Utiliser un secret côté serveur pour empêcher toute modification manuelle.
3. **Utiliser les drapeaux de sécurité** :
* `HttpOnly` pour bloquer les scripts malveillants (XSS).
* `Secure` pour limiter le cookie au HTTPS.
* `SameSite=Lax/Strict` pour empêcher le CSRF.

4. **Lier la session au matériel (DBS)** : Pour les applications critiques, lier le jeton à la puce TPM de l'appareil de l'utilisateur.

 
