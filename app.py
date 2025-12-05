import streamlit as st
import pandas as pd
import psycopg2
import json

# ---------------------------------------------------------
# LOAD CREDENTIALS FROM STREAMLIT SECRETS
# ---------------------------------------------------------
db_conf = st.secrets["neon"]

# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------
def get_connection():
    return psycopg2.connect(
        host=db_conf["host"],
        port=db_conf["port"],
        user=db_conf["user"],
        password=db_conf["password"],
        database=db_conf["database"],
        sslmode="require"
    )

# ---------------------------------------------------------
# QUERY FUNCTION
# ---------------------------------------------------------
def fetch_data():
    conn = get_connection()
    query = """
        SELECT *
        FROM pivot_presence
        WHERE "Date" >= CURRENT_DATE - INTERVAL '30 days';
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------------------------------------------------
# API MODE (bypass Streamlit UI)
# ---------------------------------------------------------
params = st.experimental_get_query_params()

if "api" in params:
    df = fetch_data()
    st.write(df.to_json(orient="records"))
    st.stop()

# ---------------------------------------------------------
# OPTIONAL UI MODE
# ---------------------------------------------------------
st.title("Presence List API")

st.write("This endpoint exposes Neon PostgreSQL.")

st.subheader("Preview data:")
df = fetch_data()
st.dataframe(df)
