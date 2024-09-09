First Step:
anaconda - python preprocess.py

Second Step:
anaconda - python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./dev.spacy

if error:
	anaconda -python -m spacy download pt_core_news_lg

