
# Manipulation de Paramètres de Formulaire (Survey)

## Description de la faille

La page de sondage (`/survey`) présente une vulnérabilité de **Manipulation de Paramètres** (*Parameter Tampering*). Le site utilise un menu déroulant pour limiter les choix de l'utilisateur (notes de 1 à 10). Cependant, le serveur ne valide pas si la valeur reçue en `POST` correspond bien à l'une de ces options. Le déclenchement automatique du formulaire via l'événement JavaScript `onchange` donne une fausse impression de sécurité.

## Méthode d'exploitation

1. Se rendre sur la page `?page=survey`.
2. Identifier le formulaire de vote dans le code source :
```html
<select name="valeur" onchange="javascript:this.form.submit();">
    <option value="1">1</option>
    ...
</select>

```


3. Utiliser les outils de développement du navigateur (F12) pour modifier la valeur d'une option. Remplacer par exemple `value="1"` par `value="100"`.
4. Alternativement, via la **Console**, modifier la valeur de l'option et soumettre le premier formulaire :
```javascript
const select = document.querySelector('select[name="valeur"]');
select.options[0].value = "100"; // Modifie la valeur envoyée
select.form.submit();           // Envoie le formulaire

```


5. Le serveur accepte la valeur "100" et retourne le flag.

## Pourquoi cela fonctionne ?

Le développeur a fait confiance à l'interface client pour restreindre les entrées. Comme le `onchange` soumet le formulaire immédiatement, il a probablement supposé que l'utilisateur ne pourrait pas altérer la valeur. Or, toute donnée provenant du client (navigateur) est sous le contrôle total de l'utilisateur et peut être modifiée avant l'envoi.

## Flag

> **03a944b434d5baff05f46c4bede5792551a2595574bcafc9a6e25f67c382ccaa**

### Remédiation

* **Validation côté serveur :** Vérifier systématiquement que la valeur reçue appartient à l'intervalle autorisé (ex: entre 1 et 10) avant de traiter le vote.
* **Contrôle de type :** S'assurer que la donnée reçue est bien un entier.
