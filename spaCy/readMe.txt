First Step:
Use requiriments.yml to install all necessary libraries. We used anaconda for managing packages.

(In the spaCy diractory):
Second Step:
Run command: preprocess.py

Third Step:
Run command: python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy

if error:
	anaconda -python -m spacy download pt_core_news_lg
