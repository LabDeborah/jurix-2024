import json
import os
import random
import spacy
from spacy.util import minibatch, compounding

def get_train_data():
    dir = './train-data'
    dataset = []

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        # checking if it is a file
        if os.path.isfile(path):
            f = open(path, encoding="utf8")
            data = json.load(f)

            entities = []

            for item in data['items']:
                entities.append(
                    (item['start'], item['end'], item['type'])
                )

            dataset.append(
                [data['source'], {
                    'entities': entities
                }]
            )
    
    return dataset

def train():
    TRAIN_DATA = get_train_data()

    n_iter = 10
    random.seed(0)

    # Create blank model
    nlp = spacy.blank('pt')
    # nlp = spacy.load('pt_core_news_sm')

    ner = None

    # Get ner pipeline component (create if necessary)
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    else:
        ner = nlp.get_pipe("ner")

    # Add new entity labels to entity recognizer
    labels = []
    for (_, entities) in TRAIN_DATA:
        e = entities['entities']
        [labels.append(entity[2]) for entity in e]
    labels = set(labels)
    [ner.add_label(l) for l in labels]

    # Set optimizer
    optimizer = nlp.begin_training()
    # optimizer = nlp.resume_training()

    move_names = list(ner.move_names)

    # Get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    # Only train NER pipe
    with nlp.disable_pipes(*other_pipes):
        # Process our training examples in iterations using shuffle, batches, and dropouts
        sizes = compounding(1, 16, 1.001)
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                # For each example, nlp.update steps through the words of the input 
                # At each word, it makes a prediction on the text and checks the annotations 
                # If it was wrong, it adjusts its weights
                nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)
            print("Losses", losses)

    # Save model to output directory
    nlp.meta["name"] = "juridic"
    nlp.to_disk('models/juridic')

train()
