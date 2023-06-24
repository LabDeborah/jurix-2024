import random
import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example

# Create a new spaCy project
nlp = spacy.blank("pt")

text = """PEDIDO DE UNIFORMIZAÇÃO NACIONAL. PETIÇÃO DE CHAMAMENTO DO FEITO À ORDEM RECEBIDA COMO AGRAVO INTERNO. 
ERRO DE AUTUAÇÃO EXISTENTE DESDE O DESPACHO DA PETIÇÃO INICIAL. AÇÃO PROPOSTA EM FACE DO INSS EM QUE FIGUROU COMO 
PARTE NA AUTUAÇÃO A UNIÃO. AUSÊNCIA DE PARTICIPAÇÃO DO INSS NA RELAÇÃO PROCESSUAL. DIVERSAS PETIÇÕES DA UNIÃO 
ALERTANDO PARA O ERRO DE AUTUAÇÃO. DECISÃO DESTA RELATORIA QUE, TAMBÉM SEM OBSERVAR REFERIDO ERRO DE AUTUAÇÃO, 
DEU PROVIMENTO AO PEDIDO DE UNIFORMIZAÇÃO DO AUTOR. NULIDADE CONFIGURADA DESDE O DESPACHO DA INICIAL. ANULAÇÃO 
DO PROCESSO DESDE O DESPACHO DA PETIÇÃO INICIAL. AGRAVO INTERNO CONHECIDO E PROVIDO."""

TRAIN_DATA = [
    (text, 
    {
        "entities": 
            [
                # (0, 4, "TIPO_DE_PROCESSO"),   # PEDIDO DE UNIFORMIZAÇÃO NACIONAL
                # (5, 12, "TIPO_DE_PECA"),      # PETIÇÃO DE CHAMAMENTO DO FEITO À ORDEM
                # (14, 16, "TIPO_DE_PECA"),     # AGRAVO INTERNO
                (193, 197, "ORGAO_JURIDICO"),     # INSS
                (238, 243, "ORGAO_JURIDICO"),     # UNIÃO
                (273, 276, "ORGAO_JURIDICO"),     # INSS
                (322, 327, "ORGAO_JURIDICO"),     # UNIAO
            ],
    })
]

# Add entities to model
for annotation in TRAIN_DATA:
    (_, entities) = annotation

    for entry in entities.get("entities"):
        nlp.vocab.strings.add(entry[2])

# Begin training
optimizer = nlp.begin_training()

losses = {}
random.shuffle(TRAIN_DATA)
batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))

for batch in batches:
    texts, annotations = zip(*batch)
    
    example = []
    # Update the model with iterating each text
    for i in range(len(texts)):
        doc = nlp.make_doc(texts[i])
        example.append(Example.from_dict(doc, annotations[i]))
    
    # Update the model
    nlp.update(example, drop=0.5, losses=losses)

# Save model to disk
nlp.to_disk("pt_juridic")
