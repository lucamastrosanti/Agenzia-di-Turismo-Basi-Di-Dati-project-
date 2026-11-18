import streamlit as st
import mysql.connector
import pandas as pd

# Configurazione iniziale della pagina
st.set_page_config(
    page_title="Gestione Hotel - Ricerca Stanze",
    page_icon="🛏️",
    layout="wide"
)

# Funzione di connessione al database locale
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel"
    )

# --- PERSONALIZZAZIONE TESTI (Richiesta Generale) ---
st.title("🛏️ Ricerca e Visualizzazione Stanze")
st.markdown("""
In questa pagina è possibile esplorare l'elenco delle camere disponibili nell'hotel. 
Utilizza il pannello dei filtri sottostante per restringere la ricerca in base alla tipologia di stanza, 
agli optional inclusi e ai servizi specifici presenti.
""")

st.divider()

# --- 1. RICHIESTA: EXPANDER "FILTRI" CON COMPONENTI INTERATTIVI ---
with st.expander("🔍 Filtri di Ricerca", expanded=True):
    
    # Radio button per la tipologia (singola, doppia, tripla, tutte)
    tipo_scelto = st.radio(
        "Seleziona il tipo di stanza:",
        ["Tutte", "singola", "doppia", "tripla"],
        horizontal=True
    )
    
    # Recupero dinamico degli optional dal database per popolare il Multiselect
    try:
        conn = get_connection()
        query_opt = "SELECT DISTINCT OPTIONAL_Optional FROM HAS_OPTIONAL"
        lista_optional = pd.read_sql(query_opt, conn)['OPTIONAL_Optional'].tolist()
        conn.close()
    except Exception:
        # Fallback manuale se il database non fosse raggiungibile momentaneamente
        lista_optional = ["balcone", "jacuzzi", "minibar", "pay-tv"]

    # Multiselect per gli optional
    optional_scelti = st.multiselect(
        "Seleziona gli optional desiderati:",
        options=lista_optional
    )
    
    # Checkbox per la cucina
    cucina_presente = st.checkbox("Mostra solo stanze con Cucina inclusa")

st.divider()

# --- COSTRUZIONE DELLA QUERY SQL DINAMICA ---
# Nel database la colonna si chiama 'Type', usiamo un alias 'Tipo' per comodità in output
query_base = """
    SELECT 
        CodS AS `Codice Stanza`,
        Piano AS `Piano`,
        Superficie AS `Superficie (mq)`,
        Type AS `Tipo`
    FROM STANZA
    WHERE 1=1
"""

# Applichiamo il filtro del Radio Button
if tipo_scelto != "Tutte":
    query_base += f" AND Type = '{tipo_scelto}'"

# Applichiamo il filtro della cucina (tabella HAS_SPAZI)
if cucina_presente:
    query_base += " AND CodS IN (SELECT STANZA_CodS FROM HAS_SPAZI WHERE SPAZI_Spazi = 'cucina')"

# Applichiamo i filtri degli optional multipli (tabella HAS_OPTIONAL)
if optional_scelti:
    for opt in optional_scelti:
        query_base += f" AND CodS IN (SELECT STANZA_CodS FROM HAS_OPTIONAL WHERE OPTIONAL_Optional = '{opt}')"

# --- ESECUZIONE QUERY E VISUALIZZAZIONE DATI ---
try:
    conn = get_connection()
    df_stanze = pd.read_sql(query_base, conn)
    conn.close()

    # --- 5. RICHIESTA: VISUALIZZAZIONE STANDARD SOTTO FORMA DI TABELLA ---
    st.subheader("📋 Risultati della Ricerca")
    if not df_stanze.empty:
        st.dataframe(df_stanze, use_container_width=True)
    else:
        st.info("Nessuna stanza corrisponde ai criteri di filtraggio selezionati.")

    st.divider()

    # --- 6 & 7. RICHIESTA OPZIONALE: MAX 5 STANZE, ITERAZIONE E LAYOUT A DUE COLONNE ---
    st.subheader("📸 Anteprima Dettagliata (Primi 5 Risultati)")
    
    # Limitiamo il DataFrame a un massimo di 5 righe
    df_anteprima = df_stanze.head(5)
    
    # Dizionario di immagini d'esempio basate sulla tipologia
    immagini_catalogo = {
        "singola": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=500",
        "doppia": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=500",
        "tripla": "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=500"
    }

    if not df_anteprima.empty:
        # Iterazione sulle righe usando iterrows() come richiesto dall'hint
        for index, row in df_anteprima.iterrows():
            
            # Creazione di un container grafico per separare visivamente le stanze
            with st.container():
                # Strutturazione in due colonne
                col_testo, col_immagine = st.columns(2)
                
                with col_testo:
                    st.markdown(f"### 🛏️ Camera Codice: {row['Codice Stanza']}")
                    st.write(f"**Dislocazione:** Piano {row['Piano']}")
                    st.write(f"**Dimensione:** {row['Superficie (mq)']} metri quadri")
                    st.write(f"**Tipologia:** {row['Tipo'].capitalize()}")
                    
                with col_immagine:
                    # Recupero dell'immagine in base al tipo (con fallback di sicurezza)
                    tipo_camera = row['Tipo'].lower()
                    url_img = immagini_catalogo.get(tipo_camera, "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=500")
                    st.image(url_img, caption=f"Configurazione Stanza {row['Tipo'].capitalize()}", use_container_width=True)
                
                st.divider() # Linea orizzontale divisoria per l'iterazione
    else:
        st.info("Nessun dato da mostrare nell'anteprima fotografica.")

except Exception as e:
    st.error(f"Errore durante l'elaborazione dei dati delle stanze: {e}")