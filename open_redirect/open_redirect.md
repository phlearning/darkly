# Redirection Non Validée (Open Redirect)

## Identification de la Vulnérabilité

L'application possède une fonctionnalité de redirection accessible via le paramètre `?page=redirect`. Ce mécanisme est utilisé dans le pied de page pour diriger les utilisateurs vers les réseaux sociaux du projet. La vulnérabilité réside dans le fait que l'application accepte n'importe quelle URL externe dans le paramètre `site` sans vérification préalable de la destination.

## Analyse de l'Exploitation

Cette faille permet à un attaquant de construire une URL qui semble légitime (car elle commence par le nom de domaine de confiance) mais qui redirige en réalité l'utilisateur vers un site malveillant. C'est une technique couramment utilisée pour rendre les attaques de **phishing** plus crédibles.

En modifiant la valeur du paramètre `site` par une URL quelconque (ex: `google.com`), on teste si le serveur autorise la sortie vers un domaine non prévu.

## Exploitation

Pour déclencher le flag, il suffit d'injecter une adresse externe dans la requête GET :

`http://localhost:8080/index.php?page=redirect&site=http://www.google.com`

En accédant à cette URL, le système de sécurité de Darkly détecte la redirection non contrôlée et affiche le message de succès.

## Flag
Après l'injection, le message suivant s'affiche : Good Job Here is the flag : b9e775a0291fed784a2d9680fcfad7edd6b8cdf87648da647aaf4bba288bcab3  

**Flag :** `b9e775a0291fed784a2d9680fcfad7edd6b8cdf87648da647aaf4bba288bcab3`

## Vulnérabilités et préventions

### Classification OWASP

* **A01:2021-Broken Access Control** : Manque de contrôle sur les destinations de redirection.

### Pourquoi cela fonctionne ?

Le serveur traite la valeur du paramètre `site` comme une destination absolue pour la fonction de redirection (ex: `header("Location: " . $_GET['site']);`) sans aucune structure de contrôle ou de liste blanche.

### Remédiation

* **Liste blanche (Whitelist)** : Implémenter une liste de domaines autorisés et rejeter toute redirection vers un domaine inconnu.
* **Redirection indirecte** : Utiliser des jetons ou des identifiants numériques (ex: `site=1` pour Facebook) dont la correspondance avec l'URL réelle est gérée uniquement côté serveur.
* **Validation de domaine** : Vérifier que l'URL commence par le domaine de l'application elle-même avant de procéder à la redirection.