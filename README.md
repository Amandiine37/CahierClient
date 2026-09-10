# Cahier clientèle — Les Ailes de Flo

Application mobile (PWA) pour tenir le cahier clientèle, les rendez-vous et les revenus
d'auto-entreprise d'une praticienne en massages bien-être.

Même principe que **suivi-revente** : un site web qui s'installe sur l'écran d'accueil du
téléphone et fonctionne hors connexion. **Aucune donnée ne part sur internet.**

---

## Les trois onglets

| Onglet | Ce qu'il contient |
|---|---|
| **Clientes** | Prénom, nom, adresse mail, téléphone, notes. Recherche, fiche détaillée avec l'historique des séances, appel et mail en un geste. Bouton **« Écrire à mes clientes »** pour un envoi groupé. |
| **Rendez-vous** | Un mois à la fois. Date, heure, prestation, durée, montant réglé, mode de règlement, statut (à venir / faite / annulée). |
| **Revenus** | Chiffre d'affaires encaissé du mois, panier moyen, provision URSSAF, **dépenses**, **ce qu'il te reste**, répartition par mode de règlement, **cartes cadeaux vendues**, 12 derniers mois, cumul de l'année et plafond micro. |

Les **réglages et la sauvegarde** sont derrière la roue crantée, en haut à droite.

## Cartes cadeaux (comptées à la bonne date)

En micro-entreprise, le chiffre d'affaires se compte **à l'encaissement**. Une carte cadeau
est donc du chiffre d'affaires **le jour où elle est vendue**, pas le jour où elle est utilisée.

- **Vendre une carte** : onglet Revenus → « + Vendre une carte cadeau » (montant, date, mode de
  règlement réel, et pour qui c'est facultatif). La vente entre dans le CA de sa date.
- **Utiliser une carte** : à la séance, choisir le règlement **« Réglée par une carte cadeau »**.
  Cette séance **ne compte pas** dans le CA — elle a déjà été encaissée à la vente. Sans ça, la
  même somme serait comptée deux fois et la provision URSSAF serait gonflée.

L'export Excel porte une colonne **« Compte dans le CA » (Oui/Non)** qui rend tout cela lisible
pour le comptable, plus une section dédiée aux cartes vendues.

## Dépenses (loyer, produits…) et bénéfice réel

Onglet Revenus → section **Dépenses** → « + Ajouter une dépense » (date, poste, montant, libellé).
Les postes proposés : loyer, produits & consommables, matériel, linge, fournitures, déplacements,
assurance, publicité, formation, frais bancaires, cotisations, autre — et tu peux en taper d'autres.

Juste en dessous, **« Ce qu'il te reste »** = encaissé − dépenses − charges URSSAF estimées.

> ⚠️ Important : en micro-entreprise, **les dépenses ne réduisent pas les charges URSSAF** (calculées
> sur le chiffre d'affaires **brut**). L'app ne les déduit **jamais** du CA ni de la provision URSSAF ;
> elles ne servent qu'à estimer le bénéfice réel. C'est écrit à l'écran pour éviter toute confusion.

Les dépenses figurent dans l'export Excel (section dédiée + colonnes « Dépenses » et « Reste estimé »
dans le récap mensuel) et dans le rapport PDF (dépenses par poste + « ce qu'il reste »).

## Écrire à mes clientes (envoi groupé)

Depuis l'onglet Clientes, « ✉️ Écrire à mes clientes » prépare un mail :

- objet + message, puis la liste des clientes **qui ont une adresse mail** (cochées par défaut) ;
- **« Ouvrir mon appli mail »** ouvre un brouillon avec toutes les clientes en **copie cachée (Cci)**
  — personne ne voit l'adresse des autres. C'est un brouillon : **rien n'est envoyé** tant qu'on
  n'appuie pas sur Envoyer soi-même ;
- l'expéditeur visible est l'adresse renseignée dans les réglages (« Ton adresse mail ») ;
- si la liste est trop longue pour l'appli mail, **« Copier les adresses (Cci) »** donne la liste
  à coller à la main, et **« Copier le message »** le texte.

L'app **n'envoie jamais** de mail elle-même : elle prépare, c'est tout.

## La provision URSSAF

L'onglet Revenus calcule `chiffre d'affaires encaissé × taux de charges`, puis :

1. une case **« J'ai mis cette somme de côté »**, à cocher une fois l'argent viré ;
2. le montant réellement mis de côté reste modifiable (arrondi, mois partiel…) ;
3. une **cagnotte** = tout ce qui est mis de côté moins ce qui a déjà été versé ;
4. un bouton **« J'ai payé l'URSSAF »** qui enregistre un versement et vide la cagnotte.

> ⚠️ Le taux (24,6 % par défaut) et le plafond micro (77 700 €) sont des **valeurs de
> départ, à vérifier sur urssaf.fr** : elles changent d'une année à l'autre et dépendent
> du régime (BIC / BNC, versement libératoire ou non). Les deux se corrigent dans les
> réglages. Ce calcul est une aide à la mise de côté, **jamais une déclaration**.

## Prestations et tarifs

Les 15 prestations pré-remplies viennent du site **les-ailes-de-flo.com** (massage
californien, lomi-lomi, pierres chaudes, drainages DIC et doux, japonais du visage,
Amma assis, escales, madérothérapie, cures, carte cadeau). Choisir une prestation
remplit automatiquement la durée et le montant. La liste s'ajuste dans les réglages.

## Où sont les données

Uniquement dans le navigateur du téléphone (`localStorage`), comme pour suivi-revente.
Ni compte, ni serveur, ni synchronisation. Conséquence : **vider les données du
navigateur ou changer de téléphone sans sauvegarde efface tout.**

Trois exports dans les réglages (roue crantée), comme sur Reventes :

- **Export Excel** (`.csv`) — une ligne par rendez-vous + un récapitulatif par mois, pour le comptable ;
- **Export PDF** — le rapport d'activité d'un mois ou d'une année, aussi disponible en bas de
  l'onglet Revenus : chiffres clés, charges estimées, modes de règlement, prestations et détail
  des séances. Il s'enregistre via l'impression du téléphone (« Enregistrer en PDF ») ;
- **Sauvegarde complète** (`.json`) — se recolle dans « Restaurer » pour tout remettre en place.

Les chiffres du rapport PDF passent par les mêmes fonctions que les écrans (`estEncaisse`,
`estImpaye`) : le PDF ne peut pas afficher un autre total que l'onglet Revenus.

Un bandeau de rappel s'affiche quand les données ont changé depuis la dernière
sauvegarde (fréquence réglable, report de 2 jours possible).

## Charte graphique

Reprise du site les-ailes-de-flo.com, couleurs relevées directement sur la page :

| Rôle | Clair | Sombre |
|---|---|---|
| Vert principal | `#4F6450` | `#A9C0A8` |
| Vert secondaire / texte doux | `#798978` | `#A4ADA1` |
| Bordures | `#CED2C9` | `#3A4A45` |
| Fond | `#F8F6F1` | `#1C2826` |
| Surfaces | `#FFFEFB` | `#24312E` |
| Doré (accent) | `#AF9D69` | `#C9B685` |

Polices : **Fraunces** (titres) et **Work Sans** (texte), comme le site, chargées depuis
Google Fonts avec une repli système si le réseau manque.

Thème clair / sombre automatique, forçable par le bouton lune de la barre du haut.

---

## Les fichiers

```
index.html            toute l'application (structure, styles, code)
manifest.webmanifest  nom, icônes et couleurs de l'app installée
sw.js                 service worker : hors connexion + bandeau de mise à jour
icon-192.png          icônes : l'arbre du site, crème sur fond vert (régénérables)
icon-512.png
arbre-separateur.png  l'arbre repris du site les-ailes-de-flo.com (source des icônes)
serve.py              serveur de test local (développement uniquement)
icones.py             regénère les deux icônes depuis arbre-separateur.png (sans bibliothèque)
README.md             ce fichier
```

## Tester en local

```bash
python serve.py
```

puis ouvrir <http://localhost:4177>. Une entrée `cahier` (port 4177) existe aussi dans
`IdeaProjects/.claude/launch.json`.

## Mettre en ligne

Comme suivi-revente : dépôt **public** sur le compte GitHub **personnel** (`amandiine37`),
GitHub Pages sur `main` / racine. Le code est public, **les données restent sur le téléphone**.

⚠️ **À chaque livraison : incrémenter `VERSION` dans `sw.js`.** C'est la modification de ce
fichier qui déclenche le bandeau « Une nouvelle version de l'appli est prête ». Sans ce
changement, le bandeau n'apparaît jamais et le téléphone garde l'ancienne version.
Déposer donc toujours `sw.js` **en plus** d'`index.html`.

## Données personnelles

Ce cahier contient des noms, mails et numéros de téléphone de vraies personnes. Rien ne
circule sur internet, mais le téléphone doit rester verrouillé, et une fiche doit pouvoir
être supprimée dès qu'une cliente le demande (bouton « Supprimer cette fiche », qui
efface aussi ses rendez-vous).

Le rapport PDF et l'export Excel contiennent les noms des clientes : à ne transmettre
qu'à qui en a besoin (comptable), et jamais à déposer sur GitHub.

---

Projet **personnel**, sans lien avec les projets OptimaHR : pas de GitLab, pas de branche,
pas de merge request.
