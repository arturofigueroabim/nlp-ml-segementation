import numpy as np
import spacy
from spacy.tokens import Doc, Span, Token
nlp = spacy.load("en_core_web_sm")
import re


doc_features = ['num_tokens', 'para_starts']
span_features = ['word_emb', 'num_tokens', 'num_verbs', 'num_pos_pronouns', 'num_conj_adv', 'num_punct', 'is_para_start',
                 'index_in_doc']

# getters that are not used as features
span_utilities = ['prev_unit', 'label']
# methods
span_methods = ['get_nth_unit', 'get_prev_unit_attr']
token_features =['word_emb']



extensions_dict = dict(doc_features=doc_features, span_features=span_features+span_utilities,
                       token_features=token_features, span_methods=span_methods)





def create_extensions(extensions_dict=None, force=True):
    
    # Features that take 'unit' as input refer to the segmentation, they do not work with just any span.
    
    # Property attributes
    
    # Store starting and ending indices of spans in the whole doc
    # 1 list per each document: [(s1_start, s1_end), (s2_start, s2_end),.., (sn_start, sn_end)]
    Doc.set_extension("units_index_list", default=[],force=True)
    
    # Store essay_id within doc
    Doc.set_extension("essay_id", default=None, force=True)

    
    # Feature Getters
    
    def get_label(span):
        
        # Gets ADU vs non-ADU LABEL for the span (intended only for sentences)

        # Works if the span is larger or equal to the adu

        # TODO:
        # DOES NOT WORK IF SPAN IS SMALLER THAN ADU, OR IF ADU IS SPLIT BETWEEN TWO SPANS (NEEDS MORE WORK!!!)
        # CLAIM VS PREMISE
        essay_id = span.doc._.essay_id

        span_start = span[0].idx
        span_end = span[-1].idx  + len(span[-1])
        start_inds = adus[adus['essay_id'] == essay_id ]['start_ind'].values
        end_inds = adus[adus['essay_id'] == essay_id ]['end_ind'].values

        # Checks if starting index of span is smaller than ADU and the ending index of the span is larger than the ADU
        return ((start_inds >= span_start) & (end_inds <= span_end)).any()
    

    
    
    def get_para_starts(doc):
        # Units starting with \n or preceding \n are considered as paragraph starts
        # if start is 0, start -1 goes back to the last token of the doc

        # TODO
        # para_ends can be obtained by shifing this list to the right by one position
        return [int(doc[start].text =='\n' or doc[start-1].text=='\n') for start, end in doc._.units_index_list]
    
    def get_is_para_start(unit):
        
        para_starts = unit.doc._.para_starts
        unit_ind = unit._.index_in_doc
        
        return para_starts[unit_ind]
        
    
    def get_word_emb(obj):
        return obj.vector
    
    def get_num_tokens(obj):
        return len(obj)
    
    def get_num_verbs(span):
        return sum([1 for token in span if token.pos_ == "VERB"])

    def get_num_pos_pronouns(span):
        return sum([1 for token in span if token.tag_ == "PRP$"])

    def get_num_pron(span):
        return sum([1 for token in span if token.pos_ == "PRON"])
    
    def get_num_conj_adv(span):
        conj_advs = ['moreover', 'incidentally', 'next', 'yet', 'finally', 'then', 'for example', 'thus', 'accordingly', 'namely', 'meanwhile', 'that is', 'also', 'undoubtedly', 'all in all', 'lately', 'hence', 'still', 'therefore', 'in addition', 'indeed', 'again', 'so', 'nevertheless', 'besides', 'instead', 'for instance', 'certainly', 'however', 'anyway', 'further', 'furthermore', 'similarly', 'now', 'in conclusion', 'nonetheless', 'thereafter', 'likewise', 'otherwise', 'consequently']
        return sum([len(re.findall(adv, span.text.lower())) for adv in conj_advs])
    
    def get_num_punct(span):
        return sum([1 for token in span if token.tag_ == "."])
    

    def get_index_in_doc(span):
        """Gets index of the segmented unit in the doc"""
        span_start = span.start

        # span end not used yet
        span_end = span.end

        # finds where span_start is in units_index_list [(s1_start, s1_end), (s2_start, s2_end),.., (sn_start, sn_end)]
        # returns the index of the corresponding span
        return np.where([span.start in range(start, end) for start, end in span.doc._.units_index_list])[0][-1]


    def get_prev_unit(span):

        return span._.get_nth_unit(span._.index_in_doc-1)
    
        
    def get_nth_unit(span, n):

        # Tuple containing the start and end index of the nth span
        span_index = span.doc._.units_index_list[n]

        # Return nth span
        return span.doc[span_index[0]: span_index[1]]



    def get_prev_unit_attr(span, attribute):

        return span._.prev_unit._.get(attribute)
    
    

    # Iterate list of features and Set Extensions (Just to not manually set extensions one by one)
    
    for feature in extensions_dict['doc_features']:
        Doc.set_extension(feature, force=force, getter=locals()[f"get_{feature}"])
        
    for feature in extensions_dict['span_features']:
        Span.set_extension(feature, force=force, getter=locals()[f"get_{feature}"])
        
    for feature in extensions_dict['token_features']:
        Token.set_extension(feature, force=force, getter=locals()[f"get_{feature}"])
        
    for method in extensions_dict['span_methods']:
        Span.set_extension(method, force=force, method=locals()[method])


def segmentation(doc=None ,mode = 'sentence'):
    if mode=='paragraph':
        pass
    if mode=='sentence':
        # segment by sentences
        units = [sent for sent in doc.sents  if not (sent.text.isspace() or sent.text =='')] 
        
        # keep track of (start, end) of units in doc object
        doc._.units_index_list = [(unit.start, unit.end) for unit in units]
        return units
    
    if mode =='avg_n_grams':
        # Code to segment with 15 grams here (average)    
        pass
    if mode=='clause':
        # Code to segment by clause
        pass
    if mode=='token':
        return [token for token in doc if not (token.text.isspace() or token.text =='')]

def unit2fv(unit, feature_list):
    
    fv = np.array([unit._.get(feature) for feature in feature_list], dtype='object')
    
    _fv = np.array([np.reshape(feature, -1) for feature in fv], dtype='object')
    
    return np.concatenate(_fv)

# Run
create_extensions(extensions_dict)   