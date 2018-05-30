import os

from nltk import word_tokenize, sent_tokenize, pos_tag
import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk import ne_chunk
from nltk.tree import Tree


class AnalyticsFunction:

    def read_data(self):
        DIRNAME = os.path.dirname(__file__)
        file_path = DIRNAME + str("/../resource/data.txt")
        data = open(file_path, "r")
        text_data = data.read()
        return text_data

    def get_doc(self):
        text_data = self.read_data()
        doc_complete = sent_tokenize(text_data)
        print(len(doc_complete))
        print(doc_complete)
        return doc_complete

    def clean(self, doc):
        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation)
        lemma = WordNetLemmatizer()
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    def generate_doc_term_matrix(self):
        doc_complete = self.get_doc();
        doc_clean = [self.clean(doc).split() for doc in doc_complete]
        dictionary = corpora.Dictionary(doc_clean)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
        return (doc_term_matrix, dictionary)

    def pos_entities(self, text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        prev = None
        continuous_chunk = []
        current_chunk = []
        entity_pos_relation = []
        str_rel = ""
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []

        return continuous_chunk


    def generic_pos_relation(self, text, most_scored_term):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        dic = {}
        values = ""
        ls = []
        dic[most_scored_term] = ls
        for i in chunked:
            if type(i) == Tree:
                # print("tree ======> ",i, i.leaves()[0][0])
                if i.leaves()[0][0] == most_scored_term:
                    dic[most_scored_term] = ls
            else:
                # print("not tree ==> ", i,i[0],i[1])
                if i[1] == "CC" and len(values.strip()) > 20:
                    ls.append(values)
                    values = ""
                else:
                    # print("VAL =======> ", i[0], i[1])
                    flag = True
                    if (i[0] == "," or i[0] == "(" or i[0] == ")" or i[0] == "]" or i[0] == "[" or i[1] == ";" or len(
                            values.strip()) < 2):
                        flag = False

                    # if not flag:
                    values = values + str(" ") + i[0]

        if len(values.strip()) > 20:
            ls.append(values)
        return dic


#    1: Entities (entities this text is talking about)
    def get_entities(self):
        text_data = self.read_data()
        entities = self.pos_entities(text_data)
        print("<================= HKHR Text Entities: ===============> ")
        return entities



#    2: Generic relations extraction (using POS tagging, pls do not use readily available relations sextraction libraries
    def get_generic_relations_extraction(self):
        doc_complete = self.get_doc()

        # Based on the term freqency and scored got india have highest score. Taking as a default term here.
        most_scored_term = "India"
        all_pos_relations = []
        for sen_text_data in doc_complete:
            doc_relation = self.generic_pos_relation(sen_text_data, most_scored_term)
            for rel in doc_relation[most_scored_term]:
                egenric_entity_realtion = most_scored_term + str(",") + rel
                all_pos_relations.append(egenric_entity_realtion)

        print("<================ HKHR  Generic relations extraction ===============> ")
        return all_pos_relations

#    3: Concepts (important concepts this text is talking about)
    def text_concept_summary(self):
        doc_term_matrix, dictionary = self.generate_doc_term_matrix()
        # Creating the object for LDA model using gensim library
        Lda = gensim.models.ldamodel.LdaModel
        # Running and Training LDA model on the document term matrix
        ldamodel = Lda(doc_term_matrix, num_topics=3, id2word=dictionary, passes=500)

        ptopic = ldamodel.print_topics(num_topics=1, num_words=25)
        words = " "
        for tp in ptopic:
            pls_splt = tp[1].split("+")
            for scr in pls_splt:
                term = scr.split("*")[1]
                words = words + term + str(", ")

        # Results
        print("<============= HKHR  Text Concept Summary ===============> ")
        concept = "This documents is talking about :" + str(words)
        return concept