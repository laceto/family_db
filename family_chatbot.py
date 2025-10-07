import streamlit as st
import json
import os
from datetime import datetime

# Definire la struttura del database familiare
struttura_database_familiare = {
    "Attività Familiari": {
        "Nome Evento": str,
        "Data": str,
        "Ora": str,
        "Luogo": str,
        "Partecipanti": list,
        "Descrizione": str,
        "Ricorrenza": str,
        "Note": str
    },
    "Inventario della Casa": {
        "Nome Oggetto": str,
        "Categoria": str,
        "Quantità": int,
        "Condizione": str,
        "Posizione": str,
        "Data di Acquisto": str,
        "Note": str
    },
    "Inventario di Cibo e Generi Alimentari": {
        "Nome Oggetto": str,
        "Categoria": str,
        "Quantità": int,
        "Data di Scadenza": str,
        "Note": str
    },
    "Faccende e Responsabilità": {
        "Nome Compito": str,
        "Membro della Famiglia Assegnato": str,
        "Frequenza": str,
        "Data di Scadenza": str,
        "Stato": str,
        "Note": str
    },
    "Documenti Familiari": {
        "Nome Documento": str,
        "Tipo": str,
        "Data di Creazione": str,
        "Proprietario": str,
        "Posizione": str,
        "Note": str
    },
    "Contatti Importanti": {
        "Nome": str,
        "Relazione": str,
        "Numero di Telefono": str,
        "Email": str,
        "Indirizzo": str,
        "Note": str
    },
    "Tradizioni Familiari": {
        "Nome Tradizione": str,
        "Descrizione": str,
        "Frequenza": str,
        "Note": str
    },
    "Obiettivi e Progetti Familiari": {
        "Nome Obiettivo/Progetto": str,
        "Descrizione": str,
        "Membro della Famiglia Assegnato(i)": str,
        "Data di Inizio": str,
        "Data di Fine": str,
        "Stato": str,
        "Note": str
    },
    "Nuove Attività Fatte da Niccolò": {
        "Nome Attività": str,
        "Data": str,
        "Descrizione": str,
        "Tempo Impiegato": int,
        "Note": str,
        "Completata": str
    },
    "Informazioni di Emergenza": {
        "Tipo Emergenza": str,
        "Descrizione Piano": str,
        "Numeri di Contatto": str,
        "Posizione delle Forniture": str,
        "Note": str
    },
    "Cartelle Sanitarie Familiari": {
        "Nome Membro della Famiglia": str,
        "Condizione Sanitaria": str,
        "Medicina": str,
        "Medico": str,
        "Date degli Appuntamenti": str,
        "Note": str
    },
    "Piani di Viaggio": {
        "Destinazione": str,
        "Date": str,
        "Alloggio": str,
        "Trasporto": str,
        "Itinerario": str,
        "Lista di Cose da Portare": str,
        "Note": str
    },
    "Attività di Trading": {
        "Simbolo": str,
        "Data del Trade": str,
        "Tipo": str,
        "Ragione del Trade": str,
        "Quantità": int,
        "Prezzo di Ingresso": float,
        "Prezzo di Uscita": float,
        "Profitto/Perdita": float,
        "Note": str
    },
    "Progetti IT": {
        "Nome Progetto": str,
        "Descrizione": str,
        "Tecnologie": list,
        "Data di Inizio": str,
        "Data di Fine": str,
        "Stato": str,
        "Obiettivo": str,
        "Risultati": str,
        "Repository": str,
        "Note": str
    },
    "Note Libere": {
        "Titolo Nota": str,
        "Data": str,
        "Testo": str,
        "Tag": list,
        "Note Aggiuntive": str
    }
}

# Helper function to validate date format (DD/MM/YYYY)
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# Helper function to validate inputs based on field type and category
def validate_entries(entries, categoria):
    errors = []
    for field, field_type in struttura_database_familiare[categoria].items():
        value = entries[field]
        
        # Check for required string fields (non-empty)
        if field_type == str and field in ["Nome Evento", "Nome Oggetto", "Nome Compito", "Nome Documento",
                                          "Nome", "Nome Tradizione", "Nome Obiettivo/Progetto", "Nome Attività",
                                          "Tipo Emergenza", "Nome Membro della Famiglia", "Destinazione", "Simbolo",
                                          "Nome Progetto", "Titolo Nota", "Testo"]:
            if not value.strip():
                errors.append(f"Il campo '{field}' è obbligatorio e non può essere vuoto.")
        
        # Validate integer fields (non-negative)
        if field_type == int and value < 0:
            errors.append(f"Il campo '{field}' deve essere un numero non negativo.")
        
        # Validate float fields (for prices, ensure non-negative; profit/loss can be negative)
        if field_type == float:
            try:
                value = float(value)
            except ValueError:
                errors.append(f"Il campo '{field}' deve essere un numero valido.")
            if "Prezzo" in field and value < 0:
                errors.append(f"Il campo '{field}' deve essere un valore non negativo.")
        
        # Validate date fields
        if field_type == str and "Data" in field and value.strip() and not is_valid_date(value):
            errors.append(f"Il campo '{field}' deve essere una data valida nel formato GG/MM/AAAA.")
        
        # Validate list fields (non-empty after splitting)
        if field_type == list and value.strip():
            items = [item.strip() for item in value.split(",")]
            if not any(items):
                errors.append(f"Il campo '{field}' contiene valori non validi.")
            entries[field] = items  # Update entries with processed list
        
        # Validate Tipo in Trading (short or long)
        if field == "Tipo" and value.strip().lower() not in ["short", "long"]:
            errors.append(f"Il campo 'Tipo' deve essere 'short' o 'long'.")
        
    return errors

# Synchronous function to load data from JSON file
def load_data():
    if os.path.exists("family_data.json"):
        with open("family_data.json", "r") as f:
            return json.load(f)
    return {categoria: [] for categoria in struttura_database_familiare}

# Synchronous function to save data to JSON file
def save_data(data):
    with open("family_data.json", "w") as f:
        json.dump(data, f, indent=4)

# Main Streamlit app (synchronous)
def main():
    st.title("Ingresso Database Familiare")

    # Load data synchronously
    family_data = load_data()

    # Selezionare la categoria per l'ingresso
    categoria = st.selectbox("Seleziona una categoria per inserire dati:", list(struttura_database_familiare.keys()))

    # Creare un modulo di ingresso in base alla categoria selezionata
    with st.form(key='entry_form'):
        entries = {}
        for field, field_type in struttura_database_familiare[categoria].items():
            if field_type == list:
                entries[field] = st.text_area(field + " (separati da virgola)", "")
            elif field_type == int:
                entries[field] = st.number_input(field, min_value=0, step=1)
            elif field_type == float:
                entries[field] = st.number_input(field, step=0.01)
            else:
                entries[field] = st.text_input(field)

        submit_button = st.form_submit_button(label="Invia")

        if submit_button:
            # Validare le voci
            errors = validate_entries(entries, categoria)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Elaborare le voci per i campi di tipo lista
                for field, field_type in struttura_database_familiare[categoria].items():
                    if field_type == list and entries[field]:
                        entries[field] = [name.strip() for name in entries[field].split(',')]
                family_data[categoria].append(entries)
                # Save data synchronously
                save_data(family_data)
                st.success("Voce aggiunta con successo!")

    # Visualizzare le voci esistenti per la categoria selezionata
    st.write("### Voci Esistenti")
    for entry in family_data[categoria]:
        st.write(entry)

if __name__ == "__main__":
    main()