from dotenv import load_dotenv
import mysql.connector
import streamlit as st
import os
import json

load_dotenv()

DB_CONFIG = json.loads(os.getenv('DB_CONFIG', '{}'))

@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None