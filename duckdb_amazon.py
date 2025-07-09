import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os

# Configuration de la page
st.set_page_config(page_title="Analyse des données Amazon avec DuckDB", layout="wide")

# Titre de l'application
st.title("📊 Analyse des Données Amazon")
st.markdown("""
Bienvenue dans cette application interactive d’analyse des données issues d'Amazon.  
<<<<<<< Updated upstream
Grâce à la puissance de *DuckDB* et la simplicité de *Streamlit*, explorez facilement :
=======
Grâce à la puissance de **DuckDB** et la simplicité de **Streamlit**, explorez facilement :
>>>>>>> Stashed changes
- les produits,
- les avis clients,
- les tendances de prix et de notation.

Utilisez les filtres, visualisez les tableaux dynamiques et plongez dans les insights pour mieux comprendre les comportements d'achat !
""")

# Fonction pour charger les données de démonstration du Amazon
def charger_donnees_amazon_demo():
    # URL des données Amazon de démonstration
    url = "data/amazon.csv"
    return pd.read_csv(url)

# Sidebar pour le chargement des données
st.sidebar.title("Source de données")
source_option = st.sidebar.radio(
    "Choisir la source de données:",
    ["Télécharger un fichier CSV"]
)

# Initialiser la connexion DuckDB
conn = duckdb.connect(database=':memory:', read_only=False)

# Obtenir les données
if source_option == "Données Amazon de démonstration":
    df = charger_donnees_amazon_demo()
    st.sidebar.success("Données Amazon de démonstration chargées!")
    
    # Enregistrer les données dans DuckDB
    conn.execute("CREATE TABLE IF NOT EXISTS produits AS SELECT * FROM df")
    
else:
    uploaded_file = st.sidebar.file_uploader("Télécharger un fichier CSV", type=["csv"])
    if uploaded_file is not None:
        # Sauvegarder temporairement le fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Créer une table à partir du CSV avec DuckDB
        conn.execute(f"CREATE TABLE IF NOT EXISTS produits AS SELECT * FROM read_csv_auto('{tmp_path}')")
        
        # Charger les données pour affichage
        df = conn.execute("SELECT * FROM produits").fetchdf()
        st.sidebar.success(f"{len(df)} Produits!")
        
        # Supprimer le fichier temporaire
        os.unlink(tmp_path)
    else:
        st.info("Veuillez télécharger un fichier CSV ou utiliser les données de démonstration.")
        st.stop()

# Afficher un aperçu des données
st.subheader("Aperçu des données")
st.dataframe(df.head(10))

def get_resume_global(conn, table_name):
    query = f"""
        SELECT
            COUNT(*) AS NbProduits,
            AVG(discounted_price) AS PrixMoyen,
            AVG(actual_price) AS PrixInitialMoyen,
            AVG(discount_percentage) AS RemiseMoyenne,
            AVG(rating) AS NoteMoyenne
        FROM {table_name}
        WHERE discounted_price IS NOT NULL
          AND actual_price IS NOT NULL
          AND discount_percentage IS NOT NULL
          AND rating IS NOT NULL
    """
    return conn.execute(query).fetchdf()

def get_top_rated_products(conn, table_name):
    return conn.execute(f"""
        SELECT product_name, rating, rating_count
        FROM {table_name}
        WHERE rating IS NOT NULL
        ORDER BY rating DESC, rating_count DESC
        LIMIT 10
    """).fetchdf()

def get_most_reviewed_products(conn, table_name):
    return conn.execute(f"""
        SELECT product_name, rating_count
        FROM {table_name}
        WHERE rating_count IS NOT NULL
        ORDER BY rating_count DESC
        LIMIT 10
<<<<<<< Updated upstream
    """).fetchdf()
=======
    """).fetchdf()

def get_distribution_par_categorie(conn, table_name):
    return conn.execute(f"""
        SELECT category, COUNT(*) AS nb_produits
        FROM {table_name}
        GROUP BY category
        ORDER BY nb_produits DESC
    """).fetchdf()
>>>>>>> Stashed changes
