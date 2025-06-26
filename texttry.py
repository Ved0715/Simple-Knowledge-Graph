import spacy

nlp = spacy.load("en_core_web_sm")
text = "Leonardo DiCaprio acted in Inception directed by Christopher Nolan."

doc = nlp(text)


for ent in doc.ents:
    print(ent.text, ent.label_)