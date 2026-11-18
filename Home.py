import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="App Turismo Italia",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dbdmg.polito.it/',
        'Report a bug': "https://dbdmg.polito.it/",
        'About': "# Corso di *Basi di Dati*"
    }
)
st.title("📈 App Turismo Italia")
st.subheader("Laboratorio: Applicazioni Web per Basi di Dati")
st.divider()
col_info, col_studente = st.columns([2, 1])

with col_info:
    st.markdown("### 📋 Informazioni Generali")
    st.write(
        "Questa applicazione multi-pagina è stata sviluppata per interfacciarsi con il database "
        "`hotel` locale. Permette di analizzare i dati relativi alle agenzie sul territorio, "
        "filtrare le stanze in base ai servizi offerti e monitorare l'andamento economico delle prenotazioni."
    )
    
    # Utilizzo di elementi di layout (Tab) richiesti dalla guida per organizzare i dettagli delle pagine
    st.markdown("#### 🗺️ Guida alla navigazione")
    tab1, tab2, tab3 = st.tabs(["🏢 Agenzie", "🛏️ Stanze", "📊 Prenotazioni"])
    
    with tab1:
        st.write("**Pagina Agenzie:** Mostra metriche chiave, la localizzazione geografica su mappa e l'elenco filtrabile delle agenzie partner.")
    with tab2:
        st.write("**Pagina Stanze:** Permette di cercare le camere d'albergo applicando filtri avanzati come tipologia, optional e presenza della cucina.")
    with tab3:
        st.write("**Pagina Prenotazioni:** Analizza l'andamento del costo medio giornaliero mensile e individua le stanze più redditizie.")


with col_studente:
    # 3. Nome dello studente inserito in un box evidenziato (expander o info)
    st.markdown("### 👨‍💻 Sviluppatore")
    with st.expander("Visualizza Dettagli Studente", expanded=True):
        st.write("**Nome:** Luca Mastrosanti")
        st.write("**Corso:** Ingegneria Informatica")
        st.write("**Insegnamento:** Basi di Dati")

st.divider()
st.info("💡 Usa il menu laterale a sinistra per navigare tra le diverse sezioni dell'applicazione.")