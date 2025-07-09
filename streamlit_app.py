import streamlit as st 
import pandas as pd
import duckdb_amazon
import duckdb

FICHIER_CSV = 'data/amazon.csv'
NOM_TABLE = 'produits'

# 🎨 Interface Streamlit
st.set_page_config(page_title="Dashboard Produits Amazon", layout="wide")

st.title("📊 Dashboard Produits Amazon")
st.markdown("Analyse des données produits extraites d’Amazon (catégories, prix, avis, notes…).")

# 📥 Chargement et Nettoyage des Données

# Définir manuellement les noms de colonnes
colonnes = [
    "product_id", "product_name", "category", "discounted_price", "actual_price", 
    "discount_percentage", "rating", "rating_count", "about_product",
    "user_id", "user_name", "review_id", "review_title", "review_content", 
    "img_link", "product_link"
]

# Charger les données
df = pd.read_csv(FICHIER_CSV, sep='\t', header=None, names=colonnes, encoding='utf-8', engine='python')

# Nettoyage avec pandas AVANT de l'envoyer dans DuckDB
def clean_price_column(col):
    return pd.to_numeric(
        col.astype(str)
           .str.replace(",", "", regex=False)
           .str.replace("₹", "", regex=False)
           .str.extract(r"(\d+\.?\d*)")[0],
        errors="coerce"
    ).fillna(0)

df["discounted_price"] = clean_price_column(df["discounted_price"])
df["actual_price"] = clean_price_column(df["actual_price"])

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.extract(r"(\d+\.?\d*)")[0]
    .astype(float)
    .fillna(0)
)

df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
df["category"] = df["category"].astype(str).fillna("Inconnue")

# Connexion à DuckDB
conn = duckdb.connect(database=':memory:')

# Enregistrer df comme une vue temporaire
conn.register("df", df)

# Créer la table DuckDB depuis la vue
conn.execute(f"CREATE TABLE {NOM_TABLE} AS SELECT * FROM df")

# ====================
# 🎯 Filtres Interactifs
# ====================

with st.sidebar:
    st.header("🎯 Filtres")
    categories = sorted(df["category"].dropna().unique().tolist())
    if not categories:
        st.warning("Aucune catégorie valide trouvée.")
        selected_categories = []
    else:
        selected_categories = st.multiselect("📂 Catégories", categories, default=categories[:3])

    min_rating, max_rating = st.slider("⭐ Note minimum", 0.0, 5.0, (3.0, 5.0), 0.1)

    # Filtrer les prix valides (non nuls)
    valid_prices = df["discounted_price"].loc[df["discounted_price"] > 0]

    if valid_prices.empty:
        st.warning("Aucune valeur valide pour le prix réduit")
        selected_price = (0, 0)
    else:
        min_price = float(valid_prices.min())
        max_price = float(valid_prices.max())
        if min_price == max_price:
            selected_price = (min_price, max_price)
        else:
            selected_price = st.slider("💰 Prix réduit", min_price, max_price, (min_price, max_price))

# Application des filtres
filtered_df = df[
    (df["category"].isin(selected_categories)) &
    (df["rating"].between(min_rating, max_rating)) &
    (df["discounted_price"].between(*selected_price))
]

# ====================
# 📋 Résultats Filtrés
# ====================
st.subheader("📃 Produits filtrés")
st.write(f"{len(filtered_df)} produits trouvés")
st.dataframe(filtered_df, use_container_width=True)

