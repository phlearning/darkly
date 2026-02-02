# Injection XSS Stockée & Contournement de Limitation Client

## Description de la faille

La page `/feedback` permet aux utilisateurs de soumettre des commentaires. Le formulaire possède des restrictions de longueur de caractères côté client (attribut `maxlength`) et tente de filtrer les balises HTML. Cependant, ces protections sont insuffisantes et permettent une injection de script (XSS).

## Méthode d'exploitation

1. Se rendre sur la page `?page=feedback`.
2. Inspecter le champ **Name** avec les outils de développement (F12). On remarque un attribut `maxlength="10"`.
3. Tenter d'injecter une balise script en la répartissant sur les deux champs pour contourner la limite de caractères et le filtrage :
* **Champ Name :** `<script>al` (le reste est tronqué par la limite).
* **Champ Comment :** `ert('XSS')</script>`


4. Cliquer sur **Sign Guestbook**.
5. Le serveur détecte l'injection de balises interdites dans les paramètres de la requête et génère le flag.

## Pourquoi cela fonctionne ?

* **Validation côté client uniquement :** La limite de caractères (`maxlength`) est facilement contournable en modifiant le HTML ou en soumettant la requête directement.
* **Filtrage incomplet :** Le serveur ne semble pas nettoyer correctement les entrées utilisateur avant de les traiter ou de les stocker, ce qui permet à des fragments de code malveillant d'être interprétés.

## Flag

> **0fbb54bbf7d099713ca4be297e1bc7da0173d8b3c21c1811b916a3a86652724e**

### Remédiation

* **Côté Serveur :** Toujours valider la longueur et le contenu des données côté serveur, jamais uniquement côté client.
* **Échappement (Escaping) :** Utiliser des fonctions comme `htmlspecialchars()` en PHP pour transformer les caractères spéciaux (`<`, `>`, `"`, `'`) en entités HTML avant l'affichage.
* **CSP :** Mettre en place une *Content Security Policy* pour interdire l'exécution de scripts inline.
