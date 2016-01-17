from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import nltk
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")
corpus = ["This is very strange",
          "This is very nice"]
vectorizer = TfidfVectorizer(min_df=1)
X = vectorizer.fit_transform(corpus)
idf = vectorizer.idf_
print dict(zip(vectorizer.get_feature_names(), idf))
from sklearn.cluster import KMeans

topics = ["alt.atheism", "comp.graphics", "comp.os.ms-windows.misc", "comp.sys.ibm.pc.hardware", "comp.sys.mac.hardware", "comp.windows.x", "misc.forsale", "rec.autos", "rec.motorcycles", "rec.sport.baseball", "rec.sport.hockey", "sci.crypt" ,"sci.electronics", "sci.med", "sci.space", "soc.religion.christian", "talk.politics.guns", "talk.politics.mideast", "talk.politics.misc", "talk.religion.misc"]
topic = [["comp.graphics", "comp.os.ms-windows.misc", "comp.sys.ibm.pc.hardware", "comp.sys.mac.hardware", "comp.windows.x"],["rec.motorcycles", "rec.sport.baseball", "rec.sport.hockey"], ["sci.crypt" ,"sci.electronics", "sci.med", "sci.space"],["misc.forsale"],["talk.politics.misc","talk.politics.guns","talk.politics.mideast"],["talk.religion.misc","alt.atheism","soc.religion.christian"]]

def get_data():
	data1=[]
	for dirpath, dirnames, filenames in os.walk("."):
		for filename in [f for f in filenames]:
			if filename.isdigit() == True:
				a = os.path.join(dirpath, filename)
				fo = open(a ,'r')
				data = fo.readlines()
				for i in range(len(data)):
					data[i] = data[i].strip()
					data[i] = re.sub(' +',' ',data[i])
					data[i] = re.split(' ', data[i]) 			
				i = 0
				while i!=len(data):
					if len(data[i]) == 1:
						data.pop(i)
						i -= 1
					i +=1
			
				k=0
				n=len(data) 
				while k<n:
					if data[k][0][-1] == ":":
						data.pop(k)
						n -=1
						k -=1
					k +=1
				data2 = ""
				for i in data:
					for j in range(len(i)):
						data2 += str(i[j]) + " "
				a = re.split('/',dirpath)
				for i in range(len(topic)):
					if a[-1] in topic[i]:
						index = i
						#index = topics.index(a[-1])
						data2 = [data2,index]
						data1.append(data2)
				"""
				if a[-1] in topics:
					index = topics.index(a[-1])
					data2 = [data2,index]
					data1.append(data2)
				"""
	return data1



print "Getting data"
data = get_data()

#print data
data1=[]
index = []
for i in data:
	data1.append(i[0])
	index.append(i[1])

print "Removing stop words"
for i in data1:
	a = i.split()
	b = ""
	for j in a:
		j =  j.decode('utf-8','replace')
		#j = unicode(j, "utf-8")
		b +=j
	i = b
	i = text = ' '.join([word for word in i.split() if word not in cachedStopWords])


print "tfidf"

from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(analyzer='word', min_df = 0,  encoding = 'utf-8', decode_error = 'replace',stop_words = 'english')

tfidf_matrix =  tf.fit_transform(data1)
feature_names = tf.get_feature_names() 
print len(feature_names)
print tfidf_matrix
print "clustering"
km = KMeans(n_clusters=6, init='k-means++', max_iter=1000, n_init=1)

km.fit_predict(tfidf_matrix,y=None)

print km.labels_
print len(km.labels_)
a = [0] * 7
for i in km.labels_:
	a[i] +=1
print a

print "getting accuracy"
a =[0] *6
b = []
for i in range(len(km.labels_) - 1):
	if index[i] == index[i+1]:
		a[km.labels_[i]] +=1

	else:
		print a
		a.sort()
		k = a[5]*1.0
		b.append(k/1000)
		a = [0]*6
a = 0.0
for i in b:
	a +=
print a 




"""
for i in data1:
	a = nltk.word_tokenize(i)
	i = a
print data1
"""