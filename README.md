## I. Informations - Projet 2

### Versions des outils utilisés

- **IDE** : Antigravity IDE Version 2.5.5
- **Python** : 3.14.2
- **Git** : 2.56.0.windows.2

### Liens utiles

- **Compte GitHub** : [Kal-Pr0t0n](https://github.com/Kal-Pr0t0n)
- **Repo GitHub perso du projet** : [Codebase-P2-DFS-Back-end-avanc-Python](https://github.com/Kal-Pr0t0n/Codebase-P2-DFS-Back-end-avanc-Python.git)

### Gestion de l'environnement virtuel (Python)

#### 1. Création de l'environnement virtuel

```powershell
python -m venv .venv
```

#### 2. Activation de l'environnement virtuel

```powershell
.\.venv\Scripts\activate
```

## II. Récupération du repository

```powershell
git clone https://github.com/OpenClassrooms-Student-Center/Codebase-P2-DFS-Back-end-avanc-Python.git
```

## III. Lire le README et installer les dépendances

<span style="color: red;"><i>Il n'y a de READ_ME dans le projet et il n'y a pas de fichier listant les dépendances non plus.</i></span>

## IV. EXECUTER UNE PREMIER FOIS L'APPLICATION et VERSIONNER LE PROJET

### a. EXECUTER UNE PREMIER FOIS L'APPLICATION

```powershell
python main.py
```

**Sortie obtenue :**

```text
The repo has been cloned and the program works!
Run at: 2026-10-18 18:13:22.251581
```

### b. CREATION D'UNE NOUVELLE BRANCHE GIT

```powershell
git status 
```

**Sortie obtenue :**

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Création de la nouvelle branche

```powershell
git branch develop 
```

Activation de la nouvelle branche

```powershell
git checkout develop
```

```powershell
git branch
```

**Sortie obtenue :**

```text
* develop
  main
```

## V. LECTURE ET COMPREHNESION DU CONTENU DU CODE

### a. main.py

le fichier <i>main.py</i> est un programme qui :

- importe le module externe <i>datetime</i> qui permet d'afficher la date et l'heure
- puis lance la fonction principale <i>"main"</i> (lignes 6-8) qui va afficher deux ligne à l'écran (sortie dans le terminal):  

```text
The repo has been cloned and the program works!
Run at: 2026-10-18 18:13:22.251581
```

Ce script ne lance pas l'autre script python présent dans le repo nommé <i>"expenses.py"</i>

### b. expenses.py

l'initialisation du programme se trouve à la <i>ligne 136</i> et va lancer la fonction principale <i>"main"</i>.

le programme est constitué de de 5 autres fonctions :

- <i>show_menu() (lignes 112-118)</i> : qui affiche dans le terminal les différentes actions possible par l'utilisateur:
  - Affichier l'historique
  - Ajouter une dépense
  - Quitter l'application
- <i>add_expense() (ligne 91 - 109)</i>: est la fonction qui permet à l'utilisateur d'ajouter une nouvelle dépense.  il commence par demander à l'utilisateur de saisir une catégorie et une description, puis de préciser le montant en euros. Un formatage du texte est effectué puis une tentative de convertion au format <i>float</i> pour le montant. Si la convertion fonctionne, la sauvegarde peut continuer, la date du jour est ensuite récupérée via le module externe <i>datetime</i>. Les données sont affectés à l'instance de Classe <i>"Expense"</i>, puis une demande de sauvegarde des données est envoyé à la fonction <i>save_expense()</i>.

- <i>show_history() (ligne 66 - 88)</i> :  cette fonction commence par appeler une autre fonction nommée <i>read_expenses</i> pour récupérer la liste des données présents dans le fichier .csv. Si des données ont pu être récupérées, le programme continue et affiche le titre <i>"\n--- Expense history ---"</i>, puis le titre des colonnes et penfin affiche chaque ligne de dépense enregistré. La valeur du montant total de dépense est aussi calculé a chaque ligne pour pouvoir obtenir le résultat final à la fin.

- <i>save_expense() (ligne 40 - 64)</i> : cette fonction permet d'enregistrer une nouvelle dépense de le fichier de sauvegarde <i>emma_expenses.csv</i>. Une première vérification est effetuée sur l'existance du fichier, si le fichier existe, il est ouvert en écriture (mode <i>append</i> précisé avec l'argument <i>"a"</i>). Et la ligne de dépense est rajouté à la fin du fichier. si le fichier n'existe pas, un fichier vide est créé, la ligne des titres de colonnes est d'abord ajouté, puis la nouvelle ligne de dépense.

- <i>read_expenses() (ligne 18 - 38)</i> : Cette fonction va vérifier l'existance du fichier de sauvegarde <i>emma_expenses.csv</i>. Si le fichier n'existe pas, il retourne une liste vide. Si le fichier existe, il est ouvert en mode lecture (mode <i>"r"</i>) puis chaque ligne lue est ajouté dans la liste des données.
