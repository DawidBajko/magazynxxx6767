import streamlit as st
import pandas as pd # <-- DODANO: Import biblioteki Pandas

# --- Inicjalizacja Magazynu ---

# Sprawdzamy, czy 'inventory' (magazyn) jest już w stanie sesji.
# Jeśli nie, tworzymy pustą listę. To zapewnia, że lista jest zachowywana
# podczas interakcji użytkownika ze stroną.
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# --- Funkcje do Zarządzania Magazynem ---

def add_item(name, quantity):
    """Dodaje nowy towar do magazynu."""
    if name and quantity > 0:
        st.session_state.inventory.append({"name": name, "quantity": int(quantity)})
        st.success(f"Dodano: {name} w ilości {int(quantity)}.")
    else:
        st.error("Wprowadź prawidłową nazwę i ilość (musi być większa niż 0).")

def remove_item(index):
    """Usuwa towar z magazynu na podstawie indeksu."""
    try:
        # Sprawdzamy, czy indeks jest prawidłowy (w zakresie listy)
        if 0 <= index < len(st.session_state.inventory):
            removed_item = st.session_state.inventory.pop(index)
            st.warning(f"Usunięto: {removed_item['name']} w ilości {removed_item['quantity']}.")
        else:
            st.error("Nieprawidłowy numer (indeks) do usunięcia.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas usuwania: {e}")

# --- Interfejs Użytkownika Streamlit ---

st.title("📦 Prosty Magazyn Towarów")
st.markdown("---")

# Tab A: Dodawanie Towaru
with st.container():
    st.header("➕ Dodaj Nowy Towar")
    
    with st.form(key='add_form', clear_on_submit=True):
        new_name = st.text_input("Nazwa Towaru:")
        # Zapewnienie, że ilość jest liczbą całkowitą
        new_quantity = st.number_input("Ilość:", min_value=1, step=1, value=1)
        
        submit_button = st.form_submit_button(label='Dodaj do Magazynu')

        if submit_button:
            add_item(new_name, new_quantity)

st.markdown("---")

# Tab B: Usuwanie Towaru
with st.container():
    st.header("➖ Usuń Towar")

    st.info("Podaj numer towaru (Lp.) z poniższej listy, aby go usunąć.")

    with st.form(key='remove_form', clear_on_submit=True):
        remove_index_display = st.number_input(
            "Numer (Lp.) Towaru do Usunięcia:", 
            min_value=1, 
            step=1, 
            # Ustawienie maksymalnej wartości, jeśli magazyn nie jest pusty
            max_value=len(st.session_state.inventory) if st.session_state.inventory else 1, 
            value=1
        )
        
        remove_button = st.form_submit_button(label='Usuń z Magazynu')
        
        if remove_button:
            # Konwertujemy numer wyświetlany (Lp.) na faktyczny indeks listy (Lp. - 1)
            remove_item(remove_index_display - 1)


st.markdown("---")

# Tab C: Wyświetlanie Magazynu
st.header("📑 Aktualny Stan Magazynu")

if st.session_state.inventory:
    # 1. Tworzymy listę słowników do wyświetlenia
    display_data = []
    for i, item in enumerate(st.session_state.inventory):
        display_data.append({
            "Lp.": i + 1,  # Numer pozycji dla użytkownika (zaczynając od 1)
            "Nazwa": item['name'],
            "Ilość": item['quantity']
        })
        
    # 2. Tworzymy Pandas DataFrame
    df = pd.DataFrame(display_data)
    
    # 3. Wyświetlamy za pomocą st.dataframe z opcją hide_index=True
    st.dataframe(
        df, 
        hide_index=True, # <-- KLUCZOWA ZMIANA: Ukrywa domyślną kolumnę indeksu
        use_container_width=True
    )
    
else:
    st.info("Magazyn jest pusty. Dodaj pierwszy towar!")
