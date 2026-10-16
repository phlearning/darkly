# Glossaire

🇬🇧 [English version](GLOSSARY.md) · [Retour au README](README.fr.md)

Les termes techniques sont volontairement conservés en anglais.

| Terme | Définition |
|-------|------------|
| **Brute force** | Essayer systématiquement de nombreux identifiants ou valeurs jusqu'à trouver le bon. |
| **Cookie tampering** | Modifier la valeur d'un cookie côté client pour changer le comportement du serveur. |
| **CrackStation / Rainbow table** | Table précalculée hash vers clair, utilisée pour inverser des hash faibles non salés. |
| **Data URI** | URL `data:` qui embarque directement le contenu (ex. `data:text/html;base64,...`). |
| **Directory indexing** | Un serveur web qui liste le contenu d'un répertoire. |
| **Directory traversal** | Utiliser des séquences `../` pour sortir du répertoire prévu. |
| **Hidden input** | Champ `<input type="hidden">` : invisible mais entièrement modifiable par le client. |
| **`.htpasswd`** | Fichier Apache stockant les identifiants pour l'authentification HTTP. |
| **Insecure Design** | Catégorie OWASP : failles dans la conception même, pas seulement l'implémentation. |
| **LFI (Local File Inclusion)** | Faire inclure ou lire par le serveur un fichier local choisi par l'attaquant. |
| **MD5** | Fonction de hachage obsolète, rapide et sujette aux collisions ; inadaptée aux mots de passe. |
| **Open redirect** | Endpoint de redirection acceptant n'importe quelle destination, utile pour le phishing. |
| **OWASP Top 10** | Liste de référence des risques de sécurité les plus critiques des applications web. |
| **Parameter tampering** | Altérer les paramètres d'une requête au-delà de ce que l'interface permet. |
| **Prepared statement** | Requête SQL paramétrée qui sépare code et données, empêchant l'injection SQL. |
| **Rate limiting** | Limiter le nombre de requêtes qu'un client peut faire sur une période donnée. |
| **Referer / User-Agent** | En-têtes HTTP définis par le client, donc falsifiables. |
| **Reflected XSS** | Script injecté renvoyé immédiatement dans la réponse à la même requête. |
| **Security through obscurity** | Compter sur le secret d'un emplacement ou d'une conception plutôt que sur un vrai contrôle d'accès. |
| **SQL injection (SQLi)** | Injecter des fragments SQL dans une requête via une entrée non assainie. |
| **Stored XSS** | Script injecté, enregistré par le serveur puis servi aux visiteurs suivants. |
| **UNION-based SQLi** | SQLi utilisant `UNION SELECT` pour ajouter des données choisies au résultat d'une requête. |
| **Unrestricted file upload** | Accepter des fichiers uploadés sans valider correctement type, extension ou contenu. |
| **Whitelist** | Liste de valeurs autorisées ; tout le reste est rejeté. |
| **XSS (Cross-Site Scripting)** | Injecter du JavaScript qui s'exécute dans le navigateur d'un autre utilisateur. |
