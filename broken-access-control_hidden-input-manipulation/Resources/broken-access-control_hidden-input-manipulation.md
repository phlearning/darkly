 # Récupération de mot de passe - Modification de paramètre (Hidden Input)

## Identification de la Vulnérabilité

En explorant la fonctionnalité de récupération de mot de passe (`?page=recover`), on accède à un formulaire demandant une adresse email. L'inspection du code source HTML (F12) révèle la présence d'un champ caché (**hidden input**) qui semble définir la cible de l'envoi du mail de récupération.

* **Champ visible :** Saisie de l'email utilisateur.
* **Champ caché :** `<input type="hidden" name="mail" value="webmaster@borntosec.com">`

L'application fait l'erreur critique de faire confiance à une donnée fournie par le client pour identifier le destinataire ou valider la requête, plutôt que de gérer cette information exclusivement côté serveur.

## Analyse de l'Exploitation

La faille est de type **Broken Access Control** (Contrôle d'accès défaillant). Comme le champ est de type `hidden`, il n'est pas censé être modifié par un utilisateur normal. Cependant, un attaquant peut intercepter la requête ou modifier le DOM pour changer cette valeur.

En modifiant la valeur `webmaster@borntosec.com` par une adresse arbitraire, on force le script de traitement à valider une condition imprévue par les développeurs, ce qui déclenche l'affichage du flag.

## Exploitation

Il existe deux méthodes principales pour exploiter cette faille.

### Méthode 1 : Modification du DOM (Navigateur)

1. Faites un clic droit sur la page de récupération et choisissez **Inspecter**.
2. Modifiez la valeur du champ `hidden` :
* Ancien : `value="webmaster@borntosec.com"`
* Nouveau : `value="test@test.com"`


3. Saisissez n'importe quel email dans le champ visible et cliquez sur **Submit**.

### Méthode 2 : Requête directe (cURL)

On peut simuler l'envoi du formulaire en envoyant directement une requête POST avec le paramètre modifié.

```bash
curl 'http://[IP_DE_LA_VM]/?page=recover' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-raw 'mail=test%40test.com&Submit=Submit'

```

Dans mon cas:
```
curl 'http://localhost:8080/?page=recover' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-raw 'mail=test%40test.com&Submit=Submit'
```

## Flag
 `1d4855f7337c0c14b6f44946872c4eb33853f40b2d54393fbe94f49f1e19bbb0`


## Vulnérabilités et préventions

### La confiance envers les données client

La règle d'or en sécurité web est que **tout ce qui provient du navigateur est modifiable**. Un champ `hidden` n'est pas un champ sécurisé, c'est simplement un champ qui n'est pas affiché graphiquement.

* **Mauvaise pratique :** Passer des informations sensibles ou des paramètres de contrôle (ID utilisateur, prix d'un article, email cible) dans des champs cachés ou des paramètres d'URL.
* **Bonne pratique :** Récupérer l'information directement depuis la session utilisateur côté serveur ou depuis une base de données sécurisée.

### Manipulation de paramètres (Insecure Direct Object Reference)

Cette faille s'apparente à une IDOR. L'attaquant modifie une référence d'objet (ici une adresse email servant d'identifiant de cible) pour manipuler le comportement du serveur.

**Exemple de correction en PHP :**

```php
// MAUVAIS : Le serveur utilise la valeur POSTée sans vérification
$target_mail = $_POST['mail']; 
send_recovery_link($target_mail);

// BON : Le serveur utilise l'email lié à la session ou vérifie la légitimité
session_start();
$user = $db->getUserById($_SESSION['user_id']);
$target_mail = $user->getEmail(); // On récupère l'email fiable en DB
send_recovery_link($target_mail);

```

### Résumé des bonnes pratiques

1. **Validation côté serveur :** Ne jamais traiter une donnée sensible provenant du client sans vérification stricte.
2. **Principe du moindre privilège :** Le client ne devrait envoyer que le strict minimum (ex: son identifiant), et le serveur doit valider si cet identifiant a le droit d'effectuer l'action demandée.
3. **Utilisation de Jetons (Tokens) :** Pour les formulaires sensibles, utiliser des jetons CSRF qui lient la soumission à une session spécifique et empêchent les rejoues de requêtes malveillantes.

