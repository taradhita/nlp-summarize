from tkinter import *
from tkinter.filedialog import askopenfilename
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from math import log
import operator
# My frame for form
class simpleform_ap(Tk):

    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.grid()

    def initialize(self):
        self.openButton = Button(self, text='Open File', command=self.open_file)
        self.openButton.grid(column=3,row=3)
        self.tokenButton = Button(self, text='Tokenisasi', command = self.tokenisasi)
        self.tokenButton.grid(column=1,row=2)
        self.stopwordButton = Button(self, text='Stopword', command=self.stopword)
        self.stopwordButton.grid(column=1,row=3)
        self.stemmingButton = Button(self, text='Stemming',command=self.stemming)
        self.stemmingButton.grid(column=1,row=4)
        self.sumButton = Button(self, text='Summarization', command=self.summarization)
        self.sumButton.grid(column=1,row=5)
        

    def open_file(self):
        self.r = open(askopenfilename())
        self.TextIn = Text(self, state = 'normal', width=80, height=20)
        self.TextIn.grid(column = 3, row=1)
        self.TextIn.insert(END,self.r.read())
        #print (self.r)
        

    def tokenisasi(self):
        frequency = {} 
        r_string = self.TextIn.get("1.0",END)
        tokens = word_tokenize(r_string)
        words = [word for word in tokens if re.findall("\w(?:[-\w]*\w)?",word)] 
        words = [w.lower() for w in words]
        self.TextOut = Text(self, state = 'normal', width=80, height=15)
        self.TextOut.grid(column = 3, row=6)
        self.TextOut.insert(END, "Amount of Type: "+ str(len(set(words))) +"\n")
        self.TextOut.insert(END, "Amount of Token: "+ str(len(words))+"\n")
        for word in words:
            count = frequency.get(word,0)
            frequency[word] = count + 1
         
        frequency_list = sorted(frequency, key=frequency.get, reverse=True)
     
        for words in frequency_list:
            self.TextOut.insert(END, words +" "+ str(frequency[words])+"\n")

    def stopword(self):
        frequency = {} 
        r_string = self.TextIn.get("1.0",END)
        tokens = word_tokenize(r_string)
        words = [word for word in tokens if re.findall("\w(?:[-\w]*\w)?",word)] 
        words = [w.lower() for w in words]
        stop_words = set(stopwords.words('english'))
        self.TextOut = Text(self, state = 'normal',width=80, height=15)
        self.TextOut.grid(column = 3, row=6)
        self.TextOut.insert(END, "Amount of Type: "+ str(len(set(words))) +"\n")
        self.TextOut.insert(END, "Amount of Token: "+ str(len(words))+"\n")
        for word in words:
            if word not in stop_words:
                count = frequency.get(word,0)
                frequency[word] = count + 1
         
        frequency_list = sorted(frequency, key=frequency.get, reverse=True)
     
        for words in frequency_list:
            self.TextOut.insert(END, words +" "+ str(frequency[words])+"\n")

    def stemming(self):
        r_string = self.TextIn.get("1.0",END)
        stemmer = SnowballStemmer("english")
        tokens = word_tokenize(r_string)
        words = [word for word in tokens if re.findall("\w(?:[-\w]*\w)?",word)] 
        words = [w.lower() for w in words]
        stop_words = set(stopwords.words('english'))
        self.TextOut = Text(self, state = 'normal',width=80, height=15)
        self.TextOut.grid(column = 3, row=6)
        for w in words:
            if w not in stop_words:
                stem_res = stemmer.stem(w)
                self.TextOut.insert(END, stem_res +"\n")

    def summarization(self):
        r_string = self.TextIn.get("1.0",END)
        paragraphs = r_string.splitlines()
        paragraph = [p for p in paragraphs if p.strip() != '']
        freqlist_tf=[]
        freqlist_idf=[]
        i = 0
        for p in paragraph:
            i += 1
            j=0
            sentences=sent_tokenize(p)
            for s in sentences:
                j+=1
                paragraphDict = {}
                sentenceDict= {}
                c = 0
                d = 0
                stop_words = set(stopwords.words('english'))
                word_par_tokens = word_tokenize(p)
                words_in_par = [word for word in word_par_tokens if re.findall("\w(?:[-\w]*\w)?",word)] 
                words_in_par = [w.lower() for w in words_in_par]
                for word in words_in_par:
                    c+=1
                    if word not in stop_words:
                        if word in paragraphDict:
                            paragraphDict[word]+=1
                        else:
                            paragraphDict[word]=1
                word_sent_tokens = word_tokenize(s)
                words = [word for word in word_sent_tokens if re.findall("\w(?:[-\w]*\w)?",word)] 
                words = [w.lower() for w in words]
                for word in words:
                    d+=1
                    if word not in stop_words:
                        if word in sentenceDict:
                            sentenceDict[word]+=1
                        else:
                            sentenceDict[word]=1
                temp_idf={'doc_id':i,'count':c, 'paragraphDict':paragraphDict}
                temp_tf={'doc_id':i,'count':d, 'sent_id':j, 'sent': s, 'paragraphDict':sentenceDict}
                freqlist_tf.append(temp_tf)
            freqlist_idf.append(temp_idf)
        #print (freqlist_idf)
        #print(freqlist_tf)
        TFlist=[]
        for tfdict in freqlist_tf:
            id = tfdict['doc_id']
            for k in tfdict['paragraphDict']:
                temp={'doc_id':id, 'sent_id':tfdict['sent_id'],'TFscore':tfdict['paragraphDict'][k],'key':k}
                TFlist.append(temp)
        #print(TFlist)
        IDFlist=[]
        counter=0
        for idfdict in freqlist_idf:
            counter+=1
            for k in idfdict['paragraphDict'].keys():
                count = sum([k in tempdict['paragraphDict']for tempdict in freqlist_idf])
                temp={'doc_id':idfdict['doc_id'], 'IDFscore':log(len(freqlist_idf)/count),'key':k}
                IDFlist.append(temp)
        #print(IDFlist)
        TFIDFlist=[]
        for j in IDFlist:
            for i in TFlist:
                if j['key']==i['key'] and j['doc_id']==i['doc_id']:
                    temp={'doc_id':j['doc_id'], 'TFIDFscore':i['TFscore']*j['IDFscore'], 'sent_id': i['sent_id'], 'key':i['key']}
                    TFIDFlist.append(temp)
        #print(TFIDFlist)
    
        sentscore_list=[]
        for doc in freqlist_tf:
            sent_score=0
            for i in range(0, len(TFIDFlist)):
        	    temp_dict = TFIDFlist[i]
        	    if doc['doc_id']==temp_dict['doc_id'] and doc['sent_id']==temp_dict['sent_id']:
        		    sent_score+=temp_dict['TFIDFscore']
            temp={'doc_id':doc['doc_id'], 'sent_score':sent_score,'sent':doc['sent']}
            sentscore_list.append(temp)
        sentscore_sorted=sorted(sentscore_list, key = lambda x:(x['sent_score']), reverse=True)
        #print (sentscore_sorted)
        self.TextOut1 = Text(self, state = 'normal',width=80, height=15)
        self.TextOut1.grid(column = 3, row=6)
        self.TextOut2 = Text(self, state = 'normal',width=80, height=15)
        self.TextOut2.grid(column = 4, row=6)
        self.TextOut3 = Text(self, state = 'normal',width=60, height=15)
        self.TextOut3.grid(column = 4, row=1)
        self.TextOut3.insert(END, "TF Score \n")
        for tf in TFlist:
            self.TextOut3.insert(END, tf['key'] + "(" +str(tf['TFscore'])+")" +"\n")
        self.TextOut3.insert(END, "\n IDF Score \n")
        for idf in IDFlist:
            self.TextOut3.insert(END, idf['key'] + "(" +str(idf['IDFscore'])+")" +"\n")
        self.TextOut3.insert(END, "\n TFIDF Score \n")
        for tfidf in TFIDFlist:
            self.TextOut3.insert(END, tfidf['key'] + "(" +str(tfidf['TFIDFscore'])+")" +"\n")
        for sort in sentscore_sorted:
            self.TextOut1.insert(END, sort['sent'] + "(" +str(sort['sent_score'])+")" +"\n")
        j=0
        for doc in range(0,3):
            self.TextOut2.insert(END, sentscore_sorted[j]['sent'] +"\n")
            j+=1        

def create_form():
    form = simpleform_ap(None)
    form.geometry("1400x700")
    form.title('Natural Language Processing')
    form.mainloop()

if __name__ == "__main__":
    create_form()
