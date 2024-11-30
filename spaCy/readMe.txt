We used seed "6789" for reproducibility.

First Step:
Use requiriments.yml to install all necessary libraries. We used anaconda for managing packages.

Second Step:
Move ./Train to ./dataset, so you will end up with ./dataset/Train

(In the spaCy directory):
Third Step:
Run command: preprocess.py

Fourth Step:
Run command: python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy

if error:
	python -m spacy download pt_core_news_lg 
and
	pip install spacy-lookups-data
