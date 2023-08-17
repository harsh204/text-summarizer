import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
stopwords=list(STOP_WORDS)

def summarizer(rawtext):
    nlp=spacy.load("en_core_web_sm")
    doc=nlp(rawtext)
    tokens=[token.text for token in doc]
    word_frequency={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequency.keys():
                word_frequency[word.text]=1
            else:
                word_frequency[word.text]+=1


    max_freq=max(word_frequency.values())

    for word in word_frequency.keys():
        word_frequency[word]=word_frequency[word]/max_freq

    # print(word_frequency)

    sent_tokens=[sent for sent in doc.sents]


    sent_scores={}
    for sent in sent_tokens:
        for word in sent: 
            if word.text in word_frequency.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_frequency[word.text]
                else:
                    sent_scores[sent]+=word_frequency[word.text]
    # print(sent_scores)
    select_len=int(len(sent_tokens)*0.3)
    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    # print(summary)

    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    
    return summary,doc, len(rawtext.split(' ')), len(summary.split(' '))