import json
from os import listdir
from os.path import isfile, join
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans

nlp = spacy.blank("pt")


def get_dataset(path: str) -> list:
    files = [
        join(path, f)
        for f in listdir(path)
        if isfile(join(path, f)) and f != ".DS_Store"
    ]
    spacy_data = []

    # Opening JSON file
    for file in files:
        try:
            with open(file, encoding="utf8") as json_file:
                data = json.load(json_file)

                # Convert everything to spacy dataset format
                # e.g. ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING"), (15, 18, "HEIGHT")]),
                # In the end we should have a list of items like this example above, each one
                # representing one JSON file

                # Found items
                # e.g. [(0, 11, "BUILDING"), (15, 18, "HEIGHT")]
                spacy_data_items = []

                for item in data["items"]:
                    spacy_data_items.append((item["start"], item["end"], item["type"]))

                spacy_data.append((data["source"], spacy_data_items))
        except Exception as error:
            print(f"There was an error while trying to read {file}: {error}")

    return spacy_data


testing_data_list = get_dataset(".\dataset")
training_data_list = get_dataset(".\dataset\Train")

# The DocBin will store the example documents
db = DocBin()
for text, annotations in training_data_list:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span == None:
            pass
        else:
            ents.append(span)
    filtered = filter_spans(ents)
    doc.ents = filtered
    db.add(doc)

# Do the same thing for the test dataset
db_test = DocBin()
for text, annotations in testing_data_list:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        if span == None:
            pass
        else:
            ents.append(span)
    filtered = filter_spans(ents)
    doc.ents = filtered
    db_test.add(doc)

# Save the training dataset to the spacy format
db.to_disk("./train.spacy")
db_test.to_disk("./dev.spacy")