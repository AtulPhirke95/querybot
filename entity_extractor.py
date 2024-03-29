import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

class EntityMatcher(object):
    name = 'entity_matcher'

    def __init__(self, nlp, var, label):
        patterns = [nlp.make_doc(text) for text in var]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(label, None, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        spans = []
        for label, start, end in matches:
            span = Span(doc, start, end, label=label)
            spans.append(span)
        doc.ents = spans
        return doc
