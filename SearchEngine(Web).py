import requests
from bs4 import BeautifulSoup
from collections import deque
import os

class Document:
    def __init__(self):
        self.length = 0
        self.wordlist = {}

    def doclength(self):
        return self.length

    def docfreq(self,word):
        if(word in self.wordlist):
            return self.wordlist[word]
        return 0

    def add(self,words):
        self.length+=len(words.split())
        for word in words.split():
            if(word in self.wordlist):
                self.wordlist[word]+=1
            else:
                self.wordlist[word] = 0

class Sengine:
    
    def __init__(self,doclist):
        self.vocab = {}
        self.doclist = doclist
        self.dociter = 1
        self.freq = {}



    
    def qfreq(self,word,q):
        res = 0;
        for w in q:
            if(w==word):
                res+=1
        return res
    
            
        
    def rank(self,q,vocab,doclist):
        res = {}
        for docid in doclist:
            res[docid] = 1
        v = len(vocab)
        for docid in doclist:
            for word in q:
                fiq = self.qfreq(word,q)
                fij = doclist[docid].docfreq(word)
                dj = doclist[docid].length
                res[docid]*=((0.5+fij)/((0.5*v)+dj))**fiq
        
        return res
                
        
        


        
    def buildindex(self,doclist):

        for docid in doclist:

                        temp = list(doclist[docid].wordlist.keys())
                        for word in temp:
                            if(word in self.vocab.keys()):
       
                                    
                                if(docid not in self.vocab[word]):
                                    self.vocab[word].append(docid)
                                    self.vocab[word].sort()
                            else:
                                self.vocab[word] = [docid]
                    

                               
        return self.vocab

    def search(self,q,vocab):
        
      
        temp = s.rank(q,vocab,self.doclist)
        
        res = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1])}
        list_to_merge=[]
        if(res[list(res.keys())[0]]==1):
            return []
                
        
        return list(res.keys())[::-1]

class Crawler:
    def __init__(self,seed_urls):
        self.seed_urls = seed_urls
        self.doclist = {}
        self.sitelist = {}
        self.vis = {}
        self.pagelimit = 50
    def generateDocList(self):
        url_queue = deque()
        
        for url in self.seed_urls:
            url_queue.append(url)

        i=0
        while(not url_queue or i<self.pagelimit):
            i+=1
            print(i)
            self.doclist["id" + str(i)] = Document()
            self.sitelist["id" + str(i)] = ""

            cur_url = str(url_queue.popleft())


            r = requests.get(cur_url)

            soup = BeautifulSoup(r.content,'html5lib')

            cur_anchors = soup.find_all('a')
            self.sitelist["id" + str(i)] = cur_url;
            self.vis[cur_url] = ""

            for anchor in cur_anchors:
                thisurl = anchor.get('href')
                if(thisurl==None):
                    thisurl = cur_url
                elif(thisurl[0:2]=="//"):
                    thisurl = cur_url
                elif(thisurl[0]=='/'):
                    thisurl  = cur_url+thisurl.strip('/')

                elif(thisurl=="javascript:void(0)" or thisurl=="javascript:void(0);"):
                    thisurl = cur_url
                if(thisurl not in self.vis):
                    url_queue.append(thisurl)
                self.doclist["id" + str(i)].add(str(anchor.string))
            for h1 in soup.find_all('h1'):
                self.doclist["id" + str(i)].add(str(h1.string))
            for h2 in soup.find_all('h2'):
                self.doclist["id" + str(i)].add(str(h2.string))
            for h3 in soup.find_all('h3'):
                self.doclist["id" + str(i)].add(str(h3.string))
            for h4 in soup.find_all('h4'):
                self.doclist["id" + str(i)].add(str(h4.string))
            for td in soup.find_all('td'):
                self.doclist["id" + str(i)].add(str(td.string))
            for p in soup.find_all('p'):
                self.doclist["id" + str(i)].add(str(p.string))
            for b in soup.find_all('button'):
                self.doclist["id" + str(i)].add(str(b.string))

        return self.doclist


cr = Crawler(["http://www.w3schools.com/"])
print("Loading web Data... please wait till " + str(cr.pagelimit))
doclist = cr.generateDocList()


s = Sengine(doclist)  
q = list(input("Enter the search query \n").split())
print("Searching please wait..")
vocab = s.buildindex(doclist)
res = s.search(q,vocab)


if(len(res) == 0):
    print("Sorry No result found")
else:
    j=0
    print("Top 10 search result in ranked order are")
    for docid in res:
        if(j<10):
            print(cr.sitelist[docid])
            j+=1
        
        
        
    








