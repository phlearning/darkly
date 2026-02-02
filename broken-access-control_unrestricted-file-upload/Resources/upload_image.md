# Upload de fichier - Contournement de restriction (File Upload Bypass)

## Identification de la Vulnérabilité

En explorant la fonctionnalité d'ajout d'image (`?page=upload`), on accède à un formulaire permettant de télécharger un fichier sur le serveur. L'application prétend n'accepter que des fichiers de type image (JPEG/PNG).

* **Champ visible :** Sélection d'un fichier local via un bouton "Parcourir".
* **Contrainte apparente :** Le serveur bloque les fichiers qui ne semblent pas être des images, empêchant ainsi l'exécution de scripts (comme du PHP).

L'application fait l'erreur de se baser sur des informations fournies par le client (`Content-Type` ou extension déclarée) pour valider la sécurité de l'upload, sans vérifier réellement le contenu du fichier ou son extension finale après enregistrement.

## Analyse de l'Exploitation

La faille est de type **Unrestricted File Upload**. Un attaquant peut manipuler les métadonnées de la requête HTTP pour faire passer un script malveillant pour une image légitime.

En changeant le paramètre `filename` lors de l'envoi pour lui donner une extension `.php`, tout en conservant un `Content-Type: image/jpeg`, on trompe le filtre de sécurité. Si le serveur enregistre le fichier avec l'extension `.php`, il pourra être exécuté par le moteur PHP du serveur web.

## Exploitation

Il existe deux méthodes principales pour exploiter cette faille.

### Méthode 1 : Modification via Firefox (Edit and Resend)

1. Ouvrez l'inspecteur (F12) et allez dans l'onglet **Réseau**.
2. Tentez d'uploader un fichier quelconque (ex: `image.jpg`).
3. Faites un clic droit sur la requête POST générée et choisissez **Modifier et renvoyer**.
4. Dans le corps de la requête (**Body**), modifiez :
* `filename=""` par `filename="exploit.php"`
* Laissez `Content-Type: image/jpeg` tel quel.


5. Cliquez sur **Envoyer** et examinez la réponse pour trouver le flag.

### Méthode 2 : Requête directe (cURL)

On peut simuler l'envoi du formulaire en forçant les en-têtes nécessaires pour tromper le serveur.

```bash
curl 'http://[IP_DE_LA_VM]/?page=upload' \
  -X POST \
  -F "Upload=Upload" \
  -F "uploaded=@/votre/chemin/image.jpg;filename=exploit.php;type=image/jpeg"

```

Dans mon cas :

```bash
curl 'http://localhost:8080/?page=upload' \
  -X POST \
  -F "Upload=Upload" \
  -F "uploaded=@image.jpg;filename=exploit.php;type=image/jpeg"

```

## Flag

`46910d9ce35b385885a9f7e2b336249d622f29b267a1771fbacf52133beddba8`

## Vulnérabilités et préventions

### Classification OWASP
  - **Broken Access Control :** Contournement des restrictions d'écriture sur le serveur.
  - **Insecure Design :** Défaut de conception dans la logique de vérification des fichiers (confiance aveugle envers le client).

### La confiance envers le Content-Type

Le `Content-Type` envoyé par le client est purement déclaratif. Un attaquant peut envoyer du code PHP tout en prétendant envoyer une image JPEG.

* **Mauvaise pratique :** Se fier à l'en-tête `Content-Type` ou à l'extension fournie par le navigateur.
* **Bonne pratique :** Utiliser des bibliothèques côté serveur (comme `getimagesize()` ou `Fileinfo` en PHP) pour vérifier la signature réelle du fichier (magic bytes).

### Gestion des fichiers uploadés

Le serveur ne doit jamais conserver le nom de fichier original fourni par l'utilisateur, surtout son extension.

* **Mauvaise pratique :** Enregistrer le fichier dans un répertoire accessible publiquement avec son nom d'origine.
* **Bonne pratique :** 1.  Renommer le fichier avec un hash (ex: `a1b2c3d4.jpg`).
2.  Forcer l'extension en fonction de l'analyse réelle du type de fichier.
3.  Stocker les fichiers hors de la racine web (Document Root) ou désactiver l'exécution de scripts dans le dossier d'upload (via `.htaccess` ou configuration Nginx).

### Résumé des bonnes pratiques

1. **Vérification des "Magic Bytes" :** Vérifier que les premiers octets du fichier correspondent réellement à une image.
2. **Liste blanche (Whitelist) :** N'autoriser que les extensions `.jpg, .jpeg, .png`.
3. **Désactivation de l'exécution :** Configurer le serveur pour qu'il ne traite aucun fichier dans le dossier `/uploads` comme un script exécutable.
