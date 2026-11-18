import streamlit as st
import mysql.connector
import pandas as pd

# Configurazione iniziale della pagina (Layout ottimizzato)
st.set_page_config(
    page_title="Gestione Hotel - Analisi Prenotazioni",
    page_icon="📊",
    layout="wide"
)

# Funzione per stabilire la connessione con il database locale
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel"
    )

# --- PERSONALIZZAZIONE TESTI (Richiesta Generale) ---
st.title("📊 Analisi Economica e Andamento Prenotazioni")
st.markdown("""
In questa pagina vengono elaborati i flussi finanziari relativi ai soggiorni effettuati presso l'hotel.
Il pannello permette di monitorare l'andamento del costo medio giornaliero su base mensile e di individuare 
le specifiche camere che hanno generato il rendimento più elevato in ciascun periodo d'attività.
""")

st.divider()

try:
    conn = get_connection()
    
    # Query di JOIN per estrarre i dati delle prenotazioni uniti alle caratteristiche delle stanze
    query_prenotazioni = """
        SELECT 
            P.STANZA_CodS AS `Codice Stanza`,
            S.Piano AS `Piano`,
            S.Superficie AS `Superficie (mq)`,
            S.Type AS `Tipo`,
            P.DataInizio,
            P.DataFine,
            P.Costo
        FROM PRENOTAZIONE P
        JOIN STANZA S ON P.STANZA_CodS = S.CodS
    """
    df_p = pd.read_sql(query_prenotazioni, conn)
    conn.close()

    if not df_p.empty:
        # --- PRE-ELABORAZIONE DEI DATI CON PANDAS ---
        # Trasformiamo le colonne delle date (salvate come testo nel DB) in oggetti Datetime di Pandas
        df_p['DataInizio'] = pd.to_datetime(df_p['DataInizio'])
        df_p['DataFine'] = pd.to_datetime(df_p['DataFine'])
        
        # Calcoliamo la durata del soggiorno in giorni
        df_p['Giorni'] = (df_p['DataFine'] - df_p['DataInizio']).dt.days
        # Clausola di sicurezza: se inizio e fine coincidono, contiamo 1 giorno per evitare divisioni per zero
        df_p['Giorni'] = df_p['Giorni'].apply(lambda x: 1 if x <= 0 else x)
        
        # Calcoliamo il costo medio giornaliero della singola prenotazione
        df_p['Costo Giornaliero (€)'] = df_p['Costo'] / df_p['Giorni']
        
        # Estraiamo l'identificativo del mese in formato testo ordinabile (AAAA-MM, es. "2023-01")
        df_p['Mese'] = df_p['DataInizio'].dt.strftime('%Y-%m')

        # --- 1. RICHIESTA: STANZA CON IL COSTO MEDIO GIORNALIERO MENSILE PIÙ ALTO ---
        st.subheader("🏆 Camere con Maggior Rendimento Giornaliero per Mese")
        st.markdown("La seguente tabella individua per ciascun mese i dettagli strutturali della stanza che ha registrato il costo medio giornaliero più alto:")
        
        # Raggruppiamo per mese e stanza per calcolare la media del costo giornaliero di quella sistemazione nel mese
        # (Qui abbiamo applicato la correzione della superficie)
        df_stanze_mese = df_p.groupby(['Mese', 'Codice Stanza', 'Piano', 'Superficie (mq)', 'Tipo'])['Costo Giornaliero (€)'].mean().reset_index()
        
        # Estraiamo l'indice del valore massimo di costo giornaliero per ogni rispettivo mese
        idx_max = df_stanze_mese.groupby('Mese')['Costo Giornaliero (€)'].idxmax()
        df_top_stanze = df_stanze_mese.loc[idx_max].sort_values('Mese')
        
        # Mostriamo la tabella formattando la colonna monetaria con due cifre decimali
        st.dataframe(df_top_stanze.style.format({'Costo Giornaliero (€)': '{:.2f} €'}), use_container_width=True)

        st.divider()

        # --- 2. RICHIESTA: LINE CHART DELL'ANDAMENTO DEL COSTO MEDIO GIORNALIERO ---
        st.subheader("📈 Andamento Temporale del Costo Medio Giornaliero")
        
        # Utilizziamo l'elemento di layout COLONNE per strutturare i dati affiancati
        col_tabella, col_grafico = st.columns([1, 2])
        
        # Calcoliamo la media generale dei costi giornalieri di tutte le prenotazioni aggregate per mese
        df_andamento = df_p.groupby('Mese')['Costo Giornaliero (€)'].mean().reset_index().sort_values('Mese')

        with col_tabella:
            st.markdown("#### 📋 Storico Valori Medi")
            st.dataframe(df_andamento.style.format({'Costo Giornaliero (€)': '{:.2f} €'}), use_container_width=True)
            
        with col_grafico:
            st.markdown("#### 📊 Grafico a Linee")
            # Per consentire a st.line_chart di tracciare correttamente l'asse X, impostiamo il Mese come indice
            df_chart_data = df_andamento.set_index('Mese')
            st.line_chart(df_chart_data)

    else:
        st.info("Nessun record di prenotazione rilevato all'interno del database.")

except Exception as e:
    st.error(f"Errore durante l'elaborazione dell'analisi finanziaria: {e}")