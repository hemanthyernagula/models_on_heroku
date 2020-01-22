import re
import pickle
import numpy as np
from scipy.sparse import hstack
from sklearn.linear_model import  LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer

normal_mwl        =pickle.load(open('models_on_heroku/data/pkls/mtp/normal_mwl.pkl','rb'))
normal_qm         =pickle.load(open('models_on_heroku/data/pkls/mtp/normal_qm.pkl','rb'))
normal_em         =pickle.load(open('models_on_heroku/data/pkls/mtp/normal_em.pkl','rb'))
normal_np         =pickle.load(open('models_on_heroku/data/pkls/mtp/normal_np.pkl','rb'))
normal_nw         =pickle.load(open('models_on_heroku/data/pkls/mtp/normal_nw.pkl','rb'))
normal_char       =pickle.load(open('models_on_heroku/data/pkls/mtp/normal_char.pkl','rb'))
tfidf_sent_vector =pickle.load(open('models_on_heroku/data/pkls/mtp/tfidf_sent_vector.pkl','rb'))
bow_sent_vector   =pickle.load(open('models_on_heroku/data/pkls/mtp/bow_sent_vector.pkl','rb'))
stop_words        =pickle.load(open('models_on_heroku/data/pkls/mtp/stop_words.pkl','rb'))
model             =pickle.load(open('models_on_heroku/data/pkls/mtp/model.pkl','rb'))


def  clean(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r"won't", "will not", sentence)
    sentence = re.sub(r"can\'t", "can not", sentence)
    sentence = re.sub(r"\'ve", " have", sentence)
    sentence = re.sub(r"\'m", " am", sentence)
    sentence = re.sub(r"\'s", " is", sentence)
    sentence = re.sub(r"\'d", " would", sentence)
    sentence = re.sub(r"\'ll", " will", sentence)
    sentence = re.sub(r"\'t", " not", sentence)
    sentence = re.sub(r"n\'t", " not", sentence)
    sentence = re.sub(r"\'re", " are", sentence)
    sentence=re.sub(r'\\r',' ',sentence)
    sentence=re.sub(r'\\n',' ',sentence)
    sentence=re.sub(r'\\b',' ',sentence)
    sentence = re.sub('[^A-Za-z0-9]+', ' ', sentence)
    sentence=re.sub(r'nannan','',sentence)
    
    sent=[]
    for word in sentence.split():
        if (word not in stop_words) and (word.isalpha()):
            sent.append(word)
    sentence=' '.join(sent)
    return sentence

def test_your_data(sent):
        
        
        no_words = len(sent.split())
        no_chars = len(sent)
        number_presence = 0
        exc_presence    = 0
        quest_presence  = 0
        mean_word_len   = 0
        for i in sent.split():
            if i.isdigit():
                number_presence += 1
        for i in sent:
            if i == '!':
                exc_presence += 1
            elif i == '?':
                quest_presence += 1
        word_lens  = []
        for i in sent.split():
            word_lens.append(len(i))
        mean_word_len  = np.mean(word_lens)
        
        cl_sent = clean(sent)
        mwl = normal_mwl.transform(np.array(mean_word_len).reshape(-1,1))
        qm  = normal_qm.transform(np.array(quest_presence).reshape(-1,1))
        em  = normal_em.transform(np.array(exc_presence).reshape(-1,1))
        np_  = normal_np.transform(np.array(number_presence).reshape(-1,1))
        nw  = normal_nw.transform(np.array(no_words).reshape(-1,1))
        nc  = normal_nw.transform(np.array(no_chars).reshape(-1,1))
        tfidf_= tfidf_sent_vector.transform([cl_sent])
        bow_  = bow_sent_vector.transform([cl_sent])
        final_vect = hstack((bow_,tfidf_,nw,np_,em,qm,mwl,nc)).tocsr()
        pred = model.predict(final_vect)
        # print('\n'*50,model,'\n'*50)
        return pred[0]
   
if __name__=="__main__":
    query = input('Enter your review:')
    print(test_your_data(query))