import spacy

# Load model
nlp = spacy.load("pt_juridic")

# Exemplo de uso do modelo
text = text = """RECLAMAÇÃO"""
doc = nlp(text)

print(doc.ents)

for ent in doc.ents:
    print(ent.text, ent.label_)
