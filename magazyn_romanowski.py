import streamlit as st

# Konfiguracja tytułu strony
st.set_page_config(page_title="Prosty Magazyn")

st.title("📦 Prosta Aplikacja Magazynowa")

# Inicjalizacja listy produktów w sesji (żeby nie znikały przy każdym kliknięciu)
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = []

# --- SEKCJA DODAWANIA ---
st.subheader("Dodaj nowy produkt")
nowy_produkt = st.text_input("Nazwa produktu:", key="input_dodaj")

if st.button("Dodaj do bazy"):
    if nowy_produkt:
        if nowy_produkt not in st.session_state.magazyn:
            st.session_state.magazyn.append(nowy_produkt)
            st.success(f"Dodano: {nowy_produkt}")
        else:
            st.warning("Ten produkt już jest na liście.")
    else:
        st.error("Wpisz nazwę produktu!")

# --- SEKCJA USUWANIA ---
st.divider()
st.subheader("Usuń produkt")

if st.session_state.magazyn:
    produkt_do_usuniecia = st.selectbox("Wybierz produkt do usunięcia:", st.session_state.magazyn)
    
    if st.button("Usuń zaznaczony"):
        st.session_state.magazyn.remove(produkt_do_usuniecia)
        st.info(f"Usunięto: {produkt_do_usuniecia}")
        st.rerun() # Odświeżenie aplikacji, aby zaktualizować listę
else:
    st.write("Magazyn jest pusty.")

# --- WIDOK MAGAZYNU ---
st.divider()
st.subheader("Aktualny stan magazynu:")
if st.session_state.magazyn:
    for i, p in enumerate(st.session_state.magazyn, 1):
        st.write(f"{i}. {p}")
else:
    st.info("Brak produktów do wyświetlenia.")
