import pandas as pd
import numpy as np
import sqlite3

def cargar_y_limpiar_pitchfork(db_path):
    """
    Funcion maestra para extraer, unir y limpiar las 6 tablas de Pitchfork.
    """
    conn = sqlite3.connect(db_path)
    
    # Extraccion
    df_rev = pd.read_sql_query("SELECT * FROM reviews", conn)
    df_gen = pd.read_sql_query("SELECT * FROM genres", conn)
    df_lab = pd.read_sql_query("SELECT * FROM labels", conn)
    df_con = pd.read_sql_query("SELECT * FROM content", conn)
    df_art = pd.read_sql_query("SELECT * FROM artists", conn)
    df_yrs = pd.read_sql_query("SELECT * FROM years", conn)
    conn.close()

    # Integracion (Joins)
    df = df_rev.merge(df_gen, on='reviewid', how='left')
    df = df.merge(df_lab, on='reviewid', how='left')
    df = df.merge(df_yrs, on='reviewid', how='left')
    df = df.merge(df_con, on='reviewid', how='left')
    df = df.merge(df_art, on='reviewid', how='left', suffixes=('', '_extra'))

    # Limpieza Tecnica
    df = df.drop_duplicates(subset=['reviewid']).copy()
    df['genre'] = df['genre'].fillna('unassigned').str.strip().str.lower()
    df['label'] = df['label'].fillna('independent').str.strip()
    df['content'] = df['content'].str.strip()
    
    # Optimizacion de Memoria
    df['score'] = df['score'].astype('float32')
    df['pub_year'] = pd.to_numeric(df['pub_year'], downcast='integer')
    df['genre'] = df['genre'].astype('category')
    
    return df