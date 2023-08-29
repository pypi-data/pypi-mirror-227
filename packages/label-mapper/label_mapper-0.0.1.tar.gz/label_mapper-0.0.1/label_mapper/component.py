from spacy.language import Language
import spacy

@Language.factory("label_fixer")
class LabelFixer:
    def __init__(self, nlp, name, label_map):
        self.label_map = label_map

    def __call__(self, doc):
        new_ents = []
        for ent in doc.ents:
            # change ent.label_ to new label in label_map
            new_label = self.label_map.get(ent.label_, ent.label_)
            new_ent = spacy.tokens.Span(doc, ent.start, ent.end, label=new_label)
            new_ents.append(new_ent)
        doc.ents = new_ents
        return doc
