

# Dashboard Ventes Amazon avec Streamlit & DuckDB

## Description

Ce projet propose un tableau de bord interactif pour analyser les données de ventes Amazon.
Il utilise DuckDB pour exécuter des requêtes SQL rapides sur un DataFrame Pandas, et Streamlit pour afficher des visualisations dynamiques.

## Fonctionnalités

* Visualisation du nombre de produits par catégorie
* Top 10 des produits par nombre d'avis, avec filtre par catégorie
* Top 10 des produits avec la plus grosse remise, avec filtre par catégorie et plage de remise
* Répartition des avis par note
* Top 10 des utilisateurs les plus actifs

## Installation

1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd amazon_dashboard
```

2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Usage

1. Lancer l'application Streamlit

```bash
streamlit run streamlit_app.py
```

2. Charger un fichier CSV Amazon (`amazon.csv`) via l'interface
3. Utiliser les filtres et visualisations interactives pour explorer les données

## Fichiers principaux

* `streamlit_app.py` : interface utilisateur avec Streamlit
* `duckdb_amazon.py` : fonctions de chargement, nettoyage et requêtes DuckDB

## Format du fichier CSV attendu

Le fichier CSV doit contenir au minimum ces colonnes :

* `product_id`
* `product_name`
* `category`
* `discounted_price` (ex : `₹399`)
* `actual_price`
* `discount_percentage` (ex : `20%`)
* `rating`
* `rating_count`
* `user_name`
* `review_id`
* `review`

## Nettoyage des données

Les valeurs monétaires (ex : `₹399`) sont nettoyées pour enlever le symbole `₹` et converties en nombres.
Les pourcentages de remise (ex : `20%`) sont convertis en floats.
Les notes et nombres d'avis sont castés en valeurs numériques.

---


