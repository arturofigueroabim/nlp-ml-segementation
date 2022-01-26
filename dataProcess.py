import numpy as np
import spacy
nlp = spacy.load("en_core_web_sm")
from featureExtraction import segmentation, span_features, unit2fv


def rawText2fv(text):

    doc = nlp(text)
    
    #segmented_docs = [segmentation(doc, mode='sentence') for doc in docs]
    segmented_docs = segmentation(doc, mode='sentence')
    
    # Flatten lists (Dissolve docs boundaries and store all units together in one huge list)
    units = list(segmented_docs)
    
    X_features = span_features
    

    X = np.array([unit2fv(unit, X_features) for unit in units])
    
    return X , segmented_docs 

