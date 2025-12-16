import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Magazyn z Wykresem", layout="wide")

st.title("📦 Magazyn z ilościami i historią")

# 1. Inicjalizacja stanów w sesji
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = {}  # Słownik {nazwa: ilosc}

if 'historia_stanu' not in st.session_state:
    # Zaczynamy od stanu 0
    st.session_state.historia_stanu = [0]

# Funkcja pomocnicza do aktualizacji wykresu
def aktualizuj_historie():
    suma_produktow = sum(st.session_state.magazyn.values())
    st.session_state.historia_stanu.append(suma_produktow)

# Układ kolumn dla formularzy
col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ Dodaj / Aktualizuj produkt")
    nazwa_dodaj = st.text_input("Nazwa produktu:", key="add_name")
    ilosc_dodaj = st.number_input("Ilość:", min_value=1, value=1, key="add_qty")
    
    if st.button("Zatwierdź dodawanie"):
        if nazwa_dodaj:
            if nazwa_dodaj in st.session_state.magazyn:
                st.session_state.magazyn[nazwa_dodaj] += ilosc_dodaj
            else:
                st.session_state.magazyn[nazwa_dodaj] = ilosc_dodaj
            
            st.success(f"Zaktualizowano {nazwa_dodaj}")
            aktualizuj_historie()
            st.rerun()
        else:
            st.error("Podaj nazwę produktu!")

with col2:
    st.subheader("🗑️ Usuń produkt")
    if st.session_state.magazyn:
        produkt_do_usun = st.selectbox("Wybierz produkt:", list(st.session_state.magazyn.keys()))
        if st.button("Usuń całkowicie z bazy"):
            del st.session_state.magazyn[produkt_do_usun]
            st.warning(f"Usunięto {produkt_do_usun}")
            aktualizuj_historie()
            st.rerun()
    else:
        st.info("Magazyn jest pusty.")

# --- WIZUALIZACJA DANYCH ---
st.divider()
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("📋 Aktualny stan")
    if st.session_state.magazyn:
        df_magazyn = pd.DataFrame(
            [(k, v) for k, v in st.session_state.magazyn.items()],
            columns=["Produkt", "Ilość"]
        )
        st.table(df_magazyn)
        st.metric("Suma wszystkich sztuk", sum(st.session_state.magazyn.values()))
    else:
        st.write("Brak danych.")

with c2:
    st.subheader("📈 Wykres ogólnego stanu magazynu")
    if len(st.session_state.historia_stanu) > 1:
        # Tworzymy wykres liniowy z historii
        st.line_chart(st.session_state.historia_stanu)
        st.caption("Oś X: Kolejne operacje | Oś Y: Całkowita liczba sztuk w magazynie")
    else:
        st.info("Wykonaj pierwszą operację, aby zobaczyć wykres zmian.")
