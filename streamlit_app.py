import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

from duckdb_amazon import (
    load_and_clean_csv,
    create_duckdb_conn,
    get_product_count_by_category,
    get_top_products_by_rating_count,
    get_top_products_by_discount,
    get_top_users_by_review_count,
    get_review_distribution
)

st.title("Dashboard Ventes Amazon avec DuckDB & Streamlit")

uploaded_file = st.file_uploader("Chargez votre fichier amazon.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success("Fichier chargé avec succès !")

    conn = create_duckdb_conn(df)

    st.header("Nombre de produits par catégorie")
    prod_by_cat = get_product_count_by_category(conn)
    st.bar_chart(prod_by_cat.set_index('category')['product_count'])

    # Ajout d'un selectbox pour choisir la catégorie filtrée
    categories = [''] + prod_by_cat['category'].tolist()
    selected_category = st.selectbox("Filtrer Top 10 produits par nombre d'avis par catégorie", categories)

    st.header("Top 10 produits par nombre d'avis")
    if selected_category == '':
        top_products_rating_count = get_top_products_by_rating_count(conn)
    else:
        top_products_rating_count = get_top_products_by_rating_count(conn, selected_category)

    # Tronquer noms trop longs
    top_products_rating_count['product_name'] = top_products_rating_count['product_name'].apply(
        lambda x: x[:40] + '...' if len(x) > 40 else x)

    fig = px.bar(
        top_products_rating_count,
        x='rating_count',
        y='product_name',
        orientation='h',
        labels={'rating_count': 'Nombre d\'avis', 'product_name': 'Produit'},
        color='rating_count',
        color_continuous_scale='Blues'
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), width=1000, height=400, margin=dict(l=300, r=10, t=40, b=40))

    st.plotly_chart(fig)

else:
    st.info("Veuillez charger un fichier amazon.csv pour démarrer.")
