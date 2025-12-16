import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="Magazyn Industrial", layout="wide")

# 2. Wstrzyknięcie CSS dla szarego tła i stylizacji
st.markdown("""
    <style>
    /* Tło głównej aplikacji */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Stylizacja nagłówka z ikoną */
    .main-header {
        font-size: 45px;
        font-weight: bold;
        color: #444444;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    /* Stylizacja kontenerów (kart) */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Nagłówek z "obrazkiem" (ikoną koła zębatego)
st.markdown('<div class="main-header">⚙️ System Zarządzania Magazynem</div>', unsafe_allow_html=True)
st.write("Wersja przemysłowa z podglądem zmian.")

# --- LOGIKA APLIKACJI ---

if 'magazyn' not in st.session_state:
    st.session_state.magazyn = {}

if 'historia_stanu' not in st.session_state:
    st.session_state.historia_stanu = [0]

def aktualizuj_historie():
    suma = sum(st.session_state.magazyn.values())
    st.session_state.historia_stanu.append(suma)

# Układ interfejsu
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Operacje")
    with st.container():
        nazwa = st.text_input("Nazwa produktu:")
        ilosc = st.number_input("Ilość (szt.):", min_value=1, value=1)
        
        c_btn1, c_btn2 = st.columns(2)
        if c_btn1.button("Dodaj/Aktualizuj", use_container_width=True):
            if nazwa:
                st.session_state.magazyn[nazwa] = st.session_state.magazyn.get(nazwa, 0) + ilosc
                aktualizuj_historie()
                st.rerun()
        
        if c_btn2.button("Usuń produkt", use_container_width=True):
            if nazwa in st.session_state.magazyn:
                del st.session_state.magazyn[nazwa]
                aktualizuj_historie()
                st.rerun()

with col2:
    st.subheader("📊 Statystyki ogólne")
    if len(st.session_state.historia_stanu) > 1:
        st.line_chart(st.session_state.historia_stanu, color="#444444")
    else:
        st.info("Brak danych do wyświetlenia wykresu.")

# --- TABELA STANU ---
st.divider()
st.subheader("📋 Aktualna lista produktów")
if st.session_state.magazyn:
    df = pd.DataFrame(
        [(k, v) for k, v in st.session_state.magazyn.items()],
        columns=["Produkt", "Ilość w magazynie"]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.write("Magazyn jest obecnie pusty.")
