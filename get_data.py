import os
import os.path
import re
import math
import random
count = 0

#19997 files total

topics = ["alt.atheism", "comp.graphics", "comp.os.ms-windows.misc", "comp.sys.ibm.pc.hardware", "comp.sys.mac.hardware", "comp.windows.x", "misc.forsale", "rec.autos", "rec.motorcycles", "rec.sport.baseball", "rec.sport.hockey", "sci.crypt" ,"sci.electronics", "sci.med", "sci.space", "soc.religion.christian", "talk.politics.guns", "talk.politics.mideast", "talk.politics.misc", "talk.religion.misc"]
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
				if a[-1] in topics:
					index = topics.index(a[-1])
					data2 = [data2,index]
					data1.append(data2)
	return data1

def tokenise(data):
	tok = []
	for i in data:
		chars = re.findall("i.e.|Dr.|Mr.|Mrs.|Inc.|Cir.|St.|Jr.|U.S.|N.A.S.A|text-align|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|www\.\w+\.\w+\.?\w+|\w+\.?\w+@\w+\.?\w+\.?\w+|\s[a-zA-Z]\.\s|[\w]+|\"\.|[\+\-()\"=;:*\.,\?!@#$%^&`~'|\\/<>]|\d+%|[0-9]+(?:st|nd|rd|th)",i[0])
		a = [chars,i[1]]
		tok.append(a)
	return tok

def get_unigram(tok_data):
	unigram={}
	for i in tok_data:
		for j in i[0]:
			if j.lower() not in unigram:
				unigram[j.lower()] = 1
			else:
				unigram[j.lower()] +=1
	return unigram

def cosine_similarity(query,doc):
	dot = 0.0
	for i in range(len(query)):
		dot += query[i]*doc[i]
	#dot = sum(p*q for p,q in zip(query, doc))
	q=0.0
	d=0.0
	for i in range(len(query)):
		q +=(query[i]*query[i])
		d +=(doc[i]*doc[i])
	q = math.sqrt(q)
	d = math.sqrt(d)
	if q*d == 0.0:
		return 0
	return dot/(q*d)


print "Getting data"
data = get_data()
total_len = len(data)
print "Tokenising"
tok_data = tokenise(data)
print "get unigram"
unigram = get_unigram(tok_data)
print "sorting"
res =[]
res = sorted(unigram, key=unigram.get, reverse=True)
res2=[]
for i in range(len(res)):
    res2.append(unigram[res[i]])

for i in range(len(res)):
	print res[i],res2[i]
#print tok_data[0]
#removing stop words

stp = []
for i in range(1000):
	stp.append(res[i])


data = []
print len(res)
res = res[500:]
res2 = res2[500:]
print len(res)
count = 0
for i in range(len(res)):
	if res2[i] == 1 or res2[i] == 2 or res2[i] == 3 or res2[i] == 4:
		count +=1
res = res[:-count]
res2 = res2[:-count]
print len(res)

print "Removing stop words"
for i in tok_data:
	data1 = []
	for j in i[0]:
		if j not in stp:
			data1.append(j)
	a = [data1,i[1]]
	data.append(a)
#print data[0]
print len(res)

tf = {}
print "Creating TF"
for i in range(len(res)):
	print i
	num = []
	posn = []
	final = []
	if res[i] not in tf:
		for j in range(len(data)):
			count = 0
			for k in data[j][0]:
				if k == res[i]:
					count +=1
			if count !=0:
				num.append(count)
				posn.append(j)
				final = [num,posn]
		if len(final) !=0 :
			tf[res[i]] = final

#print tf

idf = {}
print "Calculating IDF"
for i,j in tf.iteritems():	
	idf[i] = 1 + (math.log(total_len/(len(j[0])*1.0))/math.log(math.e))

#print idf

tfidf = {}
for i in tf:
	tfidf[i] = tf[i]
print "Calculating TFIDF"

for i ,j in tfidf.iteritems():
	a = []
	b = j[0]
	c = j[1]
	for k in range(len(j[0])):
		b[k] = (b[k] * idf[i])
	a.append(b)
	a.append(c)
	tfidf[i] = a
#
#print tfidf


tfidf_final = {}
for i in tfidf:
	a = []
	for j in range(total_len):
		a.append(0.0)
	tfidf_final[i] = a 
#print tfidf_final

for i in tfidf:
	a = tfidf_final[i]
	#print a
	#print len(i[1])
	for j in range(len(tfidf[i][1])):
		#print tfidf[i][0][j]
		#print tfidf[i][1][j]
		index = tfidf[i][1][j]
		value = tfidf[i][0][j]
		#print index
		#print value
		#a = tfidf_final[i]
		a[index] = value
	#print a
	tfidf_final[i] = a
#print tfidf['date']
#print tfidf_final['date']


#Testing
#kmeans
print len(tfidf_final)
score = []
for j in range(total_len):
	a = []
	for i in tfidf_final:
		a.append(tfidf_final[i][j])
	score.append(a)

print len(score)
print len(score[0])



centroid = []
while(len(centroid)!=20):
	a = random.randint(0,len(score))
	if a not in centroid:
		centroid.append(a)

points = [0] *len(score)
for i in range(len(centroid)):
	for j in range(len(score)):
		if centroid[i]!= j:
			a = cosine_similarity(score(centroid[i]),score(j))
			print a


"""
a = "./20_newsgroups/alt.atheism/49960"
fo = open(a ,'r')
data = fo.readlines()
for i in range(len(data)):
	data[i] = data[i].strip()
	print data[i]
	data[i] = re.sub(' +',' ',data[i])
	data[i] =  re.split(' ',data[i])
	print data[i]

i = 0
while i!=len(data):
	if len(data[i]) == 1:
		data.pop(i)
		i -= 1
	i +=1

k=0
n=len(data) 
while k<n:
	m=re.match(r'((\w+\-*\w+)+\-?)+\:',data[k][0])
	if m:
		data.pop(k)
		n-=1
		k-=1
	k+=1


for i in data:
	print i
#print data[0][1]
"""
"""
for i in data:
	if i[0] == " ":
		print i


"""