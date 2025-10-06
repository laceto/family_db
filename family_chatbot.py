import streamlit as st  
import json  
import os  
  
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
    "Cura degli Animali Domestici": {  
        "Nome Animale": str,  
        "Tipo": str,  
        "Razza": str,  
        "Età": str,  
        "Istruzioni di Cura": str,  
        "Contatto Veterinario": str,  
        "Note": str  
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
    }  
}  
  
# Caricare i dati esistenti dal file JSON  
def load_data():  
    if os.path.exists("family_data.json"):  
        with open("family_data.json", "r") as f:  
            return json.load(f)  
    return {categoria: [] for categoria in struttura_database_familiare}  
  
# Salvare i dati nel file JSON  
def save_data(data):  
    with open("family_data.json", "w") as f:  
        json.dump(data, f, indent=4)  
  
# App principale di Streamlit  
def main():  
    st.title("Ingresso Database Familiare")  
  
    # Caricare i dati esistenti  
    family_data = load_data()  
  
    # Selezionare la categoria per l'ingresso  
    categoria = st.selectbox("Seleziona una categoria per inserire dati:", list(struttura_database_familiare.keys()))  
  
    # Creare un modulo di ingresso in base alla categoria selezionata  
    with st.form(key='entry_form'):  
        entries = {}  
        for field in struttura_database_familiare[categoria].keys():  
            if struttura_database_familiare[categoria][field] == list:  
                entries[field] = st.text_area(field + " (separati da virgola)", "")  
            elif struttura_database_familiare[categoria][field] == int:  
                entries[field] = st.number_input(field, min_value=0)  
            else:  
                entries[field] = st.text_input(field)  
  
        submit_button = st.form_submit_button(label="Invia")  
  
        if submit_button:  
            # Elaborare le voci  
            if entries['Partecipanti']:  
                entries['Partecipanti'] = [name.strip() for name in entries['Partecipanti'].split(',')]  
            family_data[categoria].append(entries)  
            save_data(family_data)  
            st.success("Voce aggiunta con successo!")  
  
    # Visualizzare le voci esistenti per la categoria selezionata  
    st.write("### Voci Esistenti")  
    for entry in family_data[categoria]:  
        st.write(entry)  
  
if __name__ == "__main__":  
    main()  