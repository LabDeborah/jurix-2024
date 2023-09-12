import random
import spacy
from spacy.util import minibatch, compounding
from Filesystem import Filesystem
from Metrics import Metrics


class Training:
    def run(self):
        # Get a randomized TRAIN_DATA with specified size
        dataset_size = int(input("Insert the dataset size for training: "))
        dataset = fs.get_dataset(dataset_size)
        TRAIN_DATA = dataset[0]
        TEST_DATA = dataset[1]

        n_iter = 10
        random.seed(0)

        # Create blank model
        nlp = spacy.blank("pt")
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
        for _, entities in TRAIN_DATA:
            e = entities["entities"]
            [labels.append(entity[2]) for entity in e]
        labels = set(labels)
        [ner.add_label(l) for l in labels]

        # Set optimizer
        optimizer = nlp.begin_training()
        # optimizer = nlp.resume_training()

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
                misses = 0
                total_items = 0
                for batch in batches:
                    texts, annotations = zip(*batch)

                    # For each example, nlp.update steps through the words of the input
                    # At each word, it makes a prediction on the text and checks the annotations
                    # If it was wrong, it adjusts its weights
                    try:
                        nlp.update(
                            texts, annotations, sgd=optimizer, drop=0.2, losses=losses
                        )
                        total_items += 1
                    except Exception as e:
                        misses += 1
                        print(f"item , error: {e}")
                print("Losses", losses)
                print("Misses", misses)
                print("Total Items", total_items)

        # Save model to output directory
        nlp.meta["name"] = f"juridic-{dataset_size}"
        nlp.to_disk(f"models/juridic-{dataset_size}")

        mt.run(f"./models/juridic-{dataset_size}", TEST_DATA)


fs = Filesystem()
tr = Training()
mt = Metrics()

tr.run()
