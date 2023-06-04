# Dungeon Master

## Description
Dungeon Master est un jeu Rogue-like dans lequel les joueurs doivent affronter des monstres et progresser à travers différents niveaux jusqu'à atteindre le niveau final.

## Installation
Assurez-vous d'avoir Python installé (version 3.10 ou supérieure) sur votre machine.

Installez les dépendances nécessaires en exécutant la commande suivante :
```bash
pip install -r requirements.txt
```

## Comment jouer
1. Ouvrez un terminal ou une ligne de commande.
2. Naviguez jusqu'au répertoire contenant les fichiers du jeu.
3. Exécutez la commande suivante pour lancer le jeu :
```bash
python main_affichage.py
```

## Auteurs

- CUVELIER Mathieu
- LAMOUR Loïc
- LUCENAY Léonard

## Compatibilité Python
Ce jeu nécessite Python 3.10 ou supérieur pour fonctionner correctement en raison de l'utilisation de la structure `match`.

## Fonctionnalités ajoutées
- Esquive qui se produit aléatoirement mais avec de plus en plus de chance au fur et à mesure que le héros gagne en level 
- Multiple action des monstres (Déplacement/Attaque rapide) de manière aléatoire 
- Compétence débloquée lorsque le héros atteint le niveau 5,10,15
