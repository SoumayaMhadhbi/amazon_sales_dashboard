# app.py
import streamlit as st
import pandas as pd
import duckdb
from visualizations.kpis import afficher_kpis

st.set_page_config(page_title="Amazon Sales Dashboard", layout="wide")
st.title("📦 Amazon Sales Dashboard")

uploaded_file = st.file_uploader("📁 Téléverser le fichier CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Fichier chargé avec succès.")
    conn = duckdb.connect(":memory:")
    conn.register("amazon", df)

    st.sidebar.header("🎛 Filtres")
    df['Date'] = pd.to_datetime(df['Date'])

    min_date, max_date = df["Date"].min(), df["Date"].max()
    selected_dates = st.sidebar.date_input("Période", [min_date, max_date])
    selected_products = st.sidebar.multiselect("🛍️ Produits", df["Product"].unique())
    selected_regions = st.sidebar.multiselect("🌍 Régions", df["Region"].unique())

    query = "SELECT * FROM amazon WHERE 1=1"
    if selected_dates:
        start, end = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
        query += f" AND Date BETWEEN '{start}' AND '{end}'"
    if selected_products:
        products = "', '".join(selected_products)
        query += f" AND Product IN ('{products}')"
    if selected_regions:
        regions = "', '".join(selected_regions)
        query += f" AND Region IN ('{regions}')"

    df_filtered = conn.execute(query).fetchdf()

    with st.expander("🔍 Aperçu des données filtrées"):
        st.dataframe(df_filtered)

    afficher_kpis(df_filtered, conn)
