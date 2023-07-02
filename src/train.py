import random
import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example

# Create a new spaCy project
nlp = spacy.blank("pt")

def train(text: str):
    TRAIN_DATA = [
        (text, 
        {
            "entities": 
                [
                    (0, 10, "TIPO_DE_RECURSO"),   # PEDIDO DE UNIFORMIZAÇÃO NACIONAL
                    # (5, 12, "TIPO_DE_PECA"),      # PETIÇÃO DE CHAMAMENTO DO FEITO À ORDEM
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

train("RECLAMAÇÃO. BENEFÍCIO ASSISTENCIAL. RECEBIMENTO A MAIOR. DEVOLUÇÃO DETERMINADA EM PROCESSO JUDICIAL ANTERIOR. ADEQUAÇÃO AO TEMA 979 DO STJ. ÓBICE À APLICAÇÃO ANTE A EXISTÊNCIA DE COISA JULGADA. DISTINGUISHING APTO A ENSEJAR A MANUTENÇÃO DO ACÓRDÃO. VIOLAÇÃO À AUTORIDADE DE DECISÃO DA TNU NÃO VERIFICADA. RECLAMAÇÃO CONHECIDA E DESPROVIDA.")
train("RECLAMAÇÃO. INSURGÊNCIA CONTRA DECISÃO DO JUÍZO PRELIMINAR DE ADMISSIBILIDADE NA ORIGEM. NÃO CABIMENTO DA RECLAMAÇÃO, NOS TERMOS DO ARTIGO 41, II, DO RITNU. INICIAL INDEFERIDA.")

# Save model to disk
nlp.to_disk("pt_juridic")
