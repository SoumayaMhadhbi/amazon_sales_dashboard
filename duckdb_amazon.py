import duckdb
import pandas as pd
import plotly.express as px

FICHIER_CSV = 'data/amazon.csv'

def load_and_clean_csv():
    df = pd.read_csv(FICHIER_CSV, encoding='utf-8')

    # Nettoyage des colonnes prix et remise
    df['discounted_price'] = df['discounted_price'].replace('[₹,]', '', regex=True).astype(float)
    df['actual_price'] = df['actual_price'].replace('[₹,]', '', regex=True).astype(float)
    df['discount_percentage'] = df['discount_percentage'].replace('%', '', regex=True).astype(float)

    # Conversion note & nombre d’avis en numérique
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(0).astype(int)

    return df

def create_duckdb_conn(df: pd.DataFrame):
    conn = duckdb.connect(database=':memory:')
    conn.register('amazon', df)
    return conn

def get_product_count_by_category(conn):
    query = """
    SELECT category, COUNT(DISTINCT product_id) AS product_count
    FROM amazon
    GROUP BY category
    ORDER BY product_count DESC
    LIMIT 10
    """
    return conn.execute(query).df()

def get_top_products_by_rating_count(conn, category=None):
    query = """
    SELECT product_name, rating_count
    FROM amazon
    """
    if category:
        query += " WHERE category = ? "
    query += """
    ORDER BY rating_count DESC
    LIMIT 10
    """
    if category:
        return conn.execute(query, [category]).df()
    else:
        return conn.execute(query).df()

def get_avg_rating_by_category(conn):
    query = """
    SELECT category, AVG(CAST(rating AS DOUBLE)) AS avg_rating
    FROM amazon
    WHERE rating IS NOT NULL
    GROUP BY category
    ORDER BY avg_rating DESC
    LIMIT 10
    """
    return conn.execute(query).df()

def get_top_products_by_discount(conn):
    query = """
    SELECT product_name, discount_percentage
    FROM amazon
    ORDER BY discount_percentage DESC
    LIMIT 10
    """
    return conn.execute(query).df()

def get_top_users_by_review_count(conn):
    query = """
    SELECT user_name, COUNT(review_id) AS review_count
    FROM amazon
    GROUP BY user_name
    ORDER BY review_count DESC
    LIMIT 10
    """
    return conn.execute(query).df()

def get_review_distribution(conn):
    query = """
    SELECT rating, COUNT(*) AS review_count
    FROM amazon
    GROUP BY rating
    ORDER BY rating
    """
    return conn.execute(query).df()
