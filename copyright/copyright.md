# Manipulation d'en-têtes HTTP (Referer & User-Agent)

## Identification de la Vulnérabilité

En inspectant le code source HTML de la page de copyright (`?page=b7e44...`), deux commentaires cachés ont été découverts. Ces commentaires indiquent que le serveur effectue des vérifications sur la provenance de la requête et sur l'identité du client (navigateur) avant d'afficher le contenu sensible. Cette méthode de sécurisation est obsolète car les en-têtes HTTP sont fournis par le client et peuvent donc être falsifiés.

## Analyse de l'Exploitation

Pour contourner les restrictions, il est nécessaire de forger une requête HTTP incluant deux en-têtes spécifiques demandés par le serveur :

* **Referer** : Doit être défini sur `https://www.nsa.gov/` pour simuler une provenance depuis ce site.
* **User-Agent** : Doit être défini sur `ft_bornToSec` pour simuler l'utilisation d'un navigateur spécifique.

L'outil `cURL` est idéal pour cette tâche car il permet de manipuler précisément chaque champ de l'en-tête HTTP.

## Exploitation

L'exécution de la commande suivante a permis de tromper le serveur et de récupérer le flag :

```bash
curl -e "https://www.nsa.gov/" -A "ft_bornToSec" "http://localhost:8080/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"

```

* `-e` : Simule l'en-tête `Referer`.
* `-A` : Simule l'en-tête `User-Agent`.

## Flag

Le flag est apparu dans la réponse HTML sous la balise `<h2>` :

**Flag :** `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

## Vulnérabilités et préventions

### Classification OWASP

* **A04:2021-Insecure Design** : Utilisation de mécanismes de contrôle d'accès reposant sur des données client non fiables.

### Pourquoi cela fonctionne ?

Le serveur fait l'erreur de considérer les métadonnées transmises par le navigateur comme une preuve de confiance. Or, le protocole HTTP permet à tout utilisateur d'éditer manuellement ces informations avant qu'elles ne soient envoyées au serveur.

### Remédiation

* **Authentification et Autorisation** : Ne jamais utiliser d'en-têtes informatifs (`User-Agent`, `Referer`, `X-Forwarded-For`) pour gérer la sécurité. Utiliser des sessions sécurisées côté serveur ou des jetons d'accès (Tokens).
* **Nettoyage du code** : Retirer les indices sensibles (comme les instructions de configuration) des commentaires HTML publics.