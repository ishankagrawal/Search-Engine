

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Sengine:
    def __init__(self):
        self.vocab = {}
        self.doclist = {}
        self.dociter = 1
        self.freq = {}
    
    def buildindex(self,dir):
        #vocab = {word:docid(sorted)}
       
        #doclist  = {filename:docid}
     

        t = os.listdir(dir)
        for filename in t:
               

                if filename.endswith('txt'):
                    docid = "id" + str(self.dociter)
                    self.doclist[docid] = filename
                    
                    self.dociter +=1
                    f = open(filename,"r")
                    for line in f:
                        temp = list(line.split())
                        for word in temp:
                            if(word in self.vocab.keys()):
       
                                    
                                self.vocab[word].append(docid)
                                self.vocab[word].sort()
                            else:
                                self.vocab[word] = [docid]
                                    
        return self.vocab


    def search(self,q,vocab):
        final_list = []
      
        res = []
        list_to_merge=[]
        for word in q:
           
            
            if(word in vocab.keys()):
                
                list_to_merge.append(vocab[word])
        if(len(list_to_merge)==0):
            return []
        m = min(map(len,list_to_merge))
        for i in list_to_merge:
            if(len(i)==m):
                for j in list_to_merge:
                    i = self.merge(i,j)
                    
                return i
    def merge(self,l1,l2):
        x = len(l1)
        y = len(l2)
        res = []
        p,q=0,0
        while(p<x and q<y):
            if(l1[p] == l2[q]):
                res.append(l1[p])
                p+=1
                q+=1
            elif(l1[p]>l2[q]):
                q+=1
            else:
                p+=1
        return res

q=input("Enter the search query")

q = q.split()
s = Sengine()
vocab = s.buildindex(dname)
res = s.search(q,vocab)
print("The search result is")
for i in res:
    print(s.doclist[i])



