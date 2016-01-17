import csv
import math
import random
import os
import re

#dataset = list(csv.reader(open('bank-full.csv', "rb")))
#print dataset

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
	return data1


def tokenise(data):
	tok = []
	for i in data:
		chars = re.findall("i.e.|Dr.|Mr.|Mrs.|Inc.|Cir.|St.|Jr.|U.S.|N.A.S.A|text-align|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|www\.\w+\.\w+\.?\w+|\w+\.?\w+@\w+\.?\w+\.?\w+|\s[a-zA-Z]\.\s|[\w]+|\"\.|[\+\-()\"=;:*\.,\?!@#$%^&`~'|\\/<>]|\d+%|[0-9]+(?:st|nd|rd|th)",i[0])
		a = [chars,i[1]]
		tok.append(a)
	return tok

def prop_noun(token):
	m=re.match(r'[A-Z]\w+\.?',token)
	return m

def get_unigram(tok_data):
	unigram={}
	for i in tok_data:
		for j in i[0]:
			if j.lower() not in unigram:
				unigram[j.lower()] = 1
			else:
				unigram[j.lower()] +=1
	return unigram



def naive_bayes(test,test_index,train,train_index):
#print dataset
	class_count = [0.0] *6
	for i in range(len(train)):
		class_count[train_index[i]] +=1.0
	total = 0
	for i in class_count:
		total += i

	print class_count
	#print count_class1
	print total

#--training---
	print "Training"

	prob = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]

	#print prob
	for i in range(len(train)):
		index =  train_index[i]
		for j in train[i]:
			if j not in prob[index]:
				if prop_noun(j) == 0:
					prob[index][j] = 1
				else:
					prob[index][j] = 1
			else:
				if prop_noun(j) == 0:
					s = prob[index][j]
					s +=1
					prob[index][j] = s
				else:
					s = prob[index][j]
					s +=1
					prob[index][j] = s



	#print prob
	print 
	for i in range(len(prob)):
		for j in prob[i]:
			#print prob[i][j],class_count[i],i
			prob[i][j] = prob[i][j]/class_count[i]
			#print prob[i][j]
			#prob[i][j] = math.log(prob[i][j])
	#print prob
	print total
	for i in range(len(class_count)):
		class_count[i] = class_count[i]/total
	print class_count
	for i in prob:
		print len(i)

#------------------testing--------------------
	print "Testing"
	print len(test)
	count = 0
	for i in range(len(test)):
		p = [1.0] *6
		for j in test[i]:
			for k in range(6):
				if j in prob[k]:
					p[k] *= prob[k][j]
		for j in range(len(p)):
			p[j] *= class_count[j] 
		#print p

		a =  p.index(min(p))
		if a == test_index[i]:
			count +=1.0
	print count
	print count/len(test)


#----main

print "Getting data"
data = get_data()
print "Tokenizing"
tok_data = tokenise(data)

print "Boosting"
for i in tok_data:
	j = 0
	while(j!=len(i[0])):
		#print i[j]
		if prop_noun(i[0][j]) == 1:
			i[0].insert(j,i[0][j])
			j +=1
			i[0].insert(j,i[0][j])
			j +=1
		j +=1


print "converting to lower"
for i in tok_data:
	for j in i[0]:
		j = j.lower()
		#print j

print "get unigram"
unigram = get_unigram(tok_data)
print "sorting"
res =[]
res = sorted(unigram, key=unigram.get, reverse=True)
res2=[]
for i in range(len(res)):
    res2.append(unigram[res[i]])


#print tok_data[0]
#removing stop words
stp = []
for i in range(5000):
	stp.append(res[i])


data = []
print len(res)
res = res[5000:]
res2 = res2[5000:]
print len(res)
count = 0
for i in range(len(res)):
	if res2[i] == 1 or res2[i] == 2 or res2[i] == 3 or res2[i] == 4 or res2[i] == 4:
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



print "Splitting Data"
data1=[]
index = []
for i in data:
	data1.append(i[0])
	index.append(i[1])




#80% train 20%testing
te = []
while len(te) != 4000:
	a = random.randint(0,19997)
	if a not in te:
		te.append(a)

test = []
test_index= []
train = []
train_index = []

for i in range(len(data1)):
	if i in te:
		test.append(data1[i])
		test_index.append(index[i])
	else:
		train.append(data1[i])
		train_index.append(index[i])

print len(test),len (test_index)
print len(train), len(train_index)

naive_bayes(test,test_index,train,train_index)

