Le fichier principal est Main.py, 
et le module pour travailler sur les dépendances fonctionnelles
est nommé FunctionalDependancesOnTables.py.
Main.py contient le menu de l'application, une table 
et des dépendances fonctionnelles s'appliquant sur celle-ci.
(La table est tirée d'un exercice du cours)
Le module contient toutes les méthodes demandées pour le projet.

Les 3 premières dépendances fonctionnelles sont correctes
contrairement à celles-qui suivent. Ces dernières sont-là
à titre d'exemples pour montrer les résultat de la méthode
cherchant les mauvaises dépendances fonctionnelles.

La méthode permettant de conseiller des dépendances fonctionnelles
est opérationnelle mais pas très utile dans notre cas,
car la table utilisée ne contient pas assez de lignes
et certaines dépendances fausses sont donc supposée car
rien ne la contredit (Exemple: Films : Minutes -> Premiere)