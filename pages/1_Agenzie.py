import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(
    page_title="Gestione Hotel - Agenzie",
    page_icon="🏢",
    layout="wide"
)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel"
    )

st.title("🏢 Analisi e Localizzazione Agenzie Partner")
st.markdown("""
In questa sezione è possibile monitorare lo stato delle agenzie distribuite sul territorio. 
Il pannello mostra le metriche prestazionali, la loro posizione geografica in tempo reale e 
permette una ricerca mirata basata sulla città di interesse.
""")

st.divider()

# --- 1. METRICHE ---
st.subheader("📊 Indicatori Chiave (Metrics)")

try:
    conn = get_connection()
    
    # Usa Citta_Indirizzo per contare le città
    query_stats = """
        SELECT 
            COUNT(DISTINCT CodA) as tot_agenzie,
            COUNT(DISTINCT Citta_Indirizzo) as tot_citta
        FROM AGENZIA
    """
    df_stats = pd.read_sql(query_stats, conn)
    
    # Usa Citta_Indirizzo per trovare la città con più agenzie
    query_top_citta = """
        SELECT Citta_Indirizzo, COUNT(*) as conteggio
        FROM AGENZIA
        GROUP BY Citta_Indirizzo
        ORDER BY conteggio DESC
        LIMIT 1
    """
    df_top_citta = pd.read_sql(query_top_citta, conn)

    agenzie_distinte = int(df_stats['tot_agenzie'].iloc[0]) if not df_stats.empty else 0
    citta_distinte = int(df_stats['tot_citta'].iloc[0]) if not df_stats.empty else 0
    top_citta = df_top_citta['Citta_Indirizzo'].iloc[0] if not df_top_citta.empty else "N/D"

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Agenzie Totali", value=agenzie_distinte)
    col2.metric(label="Città Partner", value=citta_distinte)
    col3.metric(label="Densità Maggiore (Città)", value=top_citta)

    st.divider()

    # --- 4. RICERCA TESTUALE ---
    st.subheader("🔍 Filtra Agenzie per Città")
    citta_filtro = st.text_input("Inserisci il nome di una città per aggiornare la tabella e la mappa:")

    # --- 2 & 3. QUERY CONCAT, MAPPA E TABELLA ---
    # Unisce Via, Numero e Città per rispettare la consegna del CONCAT
    # Fa il JOIN su Citta_Indirizzo = Nome (della tabella CITTA)
    query_completa = """
        SELECT 
            A.CodA AS `Codice Agenzia`,
            A.Tel AS `Telefono`,
            CONCAT(A.Via_Indirizzo, ' ', A.Numero_Indirizzo, ', ', A.Citta_Indirizzo) AS `Indirizzo Completo`,
            A.Citta_Indirizzo AS `Citta_Controllo`,
            C.Latitudine AS latitude,
            C.Longitudine AS longitude
        FROM AGENZIA A
        JOIN CITTA C ON A.Citta_Indirizzo = C.Nome
    """
    df_agenzie = pd.read_sql(query_completa, conn)
    conn.close()

    if citta_filtro:
        df_agenzie = df_agenzie[df_agenzie['Citta_Controllo'].str.lower().str.contains(citta_filtro.lower(), na=False)]

    with st.expander("🗺️ Mappa Geografica delle Sedi Disponibili", expanded=True):
        if not df_agenzie.empty:
            st.map(df_agenzie[['latitude', 'longitude']])
        else:
            st.warning("Nessuna agenzia da mostrare sulla mappa per i criteri inseriti.")

    st.subheader("📋 Registro Dettagliato")
    if not df_agenzie.empty:
        # Nascondiamo i dati di controllo (Citta_Controllo, lat, long) e mostriamo solo info utili
        colonne_output = ['Codice Agenzia', 'Telefono', 'Indirizzo Completo']
        st.dataframe(df_agenzie[colonne_output], use_container_width=True)
    else:
        st.info("Nessuna agenzia trovata per la città specificata.")

except Exception as e:
    st.error(f"Errore nel caricamento del database: {e}")