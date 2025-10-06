import json  
  
# Load existing data  
with open('family_data.json', 'r') as file:  
    data = json.load(file)  
  
# Make your updates (this is just an example)  
new_entry = {  
    "Nome Evento": "Nuovo Evento",  
    "Data": "2023-11-01",  
    "Ora": "19:00",  
    "Luogo": "Giardino",  
    "Partecipanti": ["Alice", "Bob"],  
    "Descrizione": "Una nuova descrizione.",  
    "Ricorrenza": "Una volta",  
    "Note": "Note aggiuntive."  
}  
  
data["Attività Familiari"].append(new_entry)  
  
# Save updated data  
with open('family_data.json', 'w') as file:  
    json.dump(data, file, indent=4)  