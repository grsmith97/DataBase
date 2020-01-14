def maxDocID(documents):
	maxID = -1
	for line in documents:
		mD = line
		if 'DocID:' in line:
			mD = mD.split('DocID:')
			mD = mD[1].split(' ')
			hold = int(mD[0])
			if hold > maxID:
				maxID = hold		
	return maxID + 1

def ConditionHelper(condition, line):
	string = line
	line = line.split() 
	for cond in condition:
		if '>=' in cond:
			cond = cond.split('>=')
			if cond[0] not in string:
				return False
			for field in line:
				if cond[0] in field:
					field = field.split(':')
					if not (field[1] >= cond[1]):
						return False
		elif '<=' in cond:
			cond = cond.split('<=')
			if cond[0] not in string:
				return False
			for field in line:
				if cond[0] in field:
					field = field.split(':')
					if not (field[1] <= cond[1]):
						return False
		elif '>' in cond:
			cond = cond.split('>')
			if cond[0] not in string:
				return False
			for field in line:
				if cond[0] in field:
					field = field.split(':')
					if not (field[1] > cond[1]):
						return False
		elif '<' in cond:
			cond = cond.split('<')
			if cond[0] not in string:
				return False
			for field in line:
				if cond[0] in field:
					field = field.split(':')
					if not (field[1] < cond[1]):
						return False
		elif '=' in cond:
			cond = cond.split('=')
			if cond[0] not in string:
				return False
			for field in line:
				if cond[0] in field:
					field = field.split(':')
					if not (field[1] == cond[1]):
						return False
	return True

def queryFunc(condition, field, documents):
	if not field:
		if not condition:
			for line in documents:
				line = line.split("DocID:")
				if line[1].find(" ") == -1:
					print line[0] + '\n'
				else:
					a = line[1].split(" ", 1)
					line = line[0] + a[1]
					print line
			return
		else:
			for line in documents: #lots of bugs here
				if ConditionHelper(condition, line) == True:
					line = line.split("DocID:")
					if line[1].find(" ") == -1:
						print line[0] + '\n'
					else:
						a = line[1].split(" ", 1)
						line = line[0] + a[1]
						print line
			return
	condList = []
	vals = []
	condition = condition.split(',')
	length = len(list(condition))
	field = field.split(',')
	amt = len(list(field))
	a = 0
	length = len(list(condList))

	if not condition:
		for line in documents:
			while a < amt:
				if field[a] in line:
					line = line.split(field[a] + ":")
					line = line[1].split(' ')
					line[0] = line[0].strip('\n\r')
					vals.append(line[0])
					line = specific
				elif field[a] not in line:
					vals.append("NA")
				a += 1
	for line in documents:
		if ConditionHelper(condition, line) == True:
			a = 0
			specific = line
			while a < amt:
				if field[a] in line:
					line = line.split(field[a] + ":")
					line = line[1].split(' ')
					line[0] = line[0].strip('\n\r')
					vals.append(line[0])
					line = specific
				elif field[a] not in line:
					vals.append("NA")
				a += 1					
	vlength = len(list(vals))
	v = 0
	while v < vlength:
		x = 0
		while x < amt:
			print "{}:{}".format(field[x], vals[v]),
			if x == amt - 1:
				print '\n'
			x += 1
			v += 1

def insert(a, documents):
	aID = -1
	b = a
	nline = ''
	if 'DocID:' in a:
		a = a.split('DocID:')
		a = a[1].split(' ')
		aID = a[0]
		for line in documents:
			if "DocID:{}".format(aID) in line:
				print "Duplicate DocID error!\n"
				break
			else:
				documents.append(b)
				print b,'\n'
				break
	else:
		docID = maxDocID(documents)
		nline = "DocID:{}".format(docID)
		nline = nline + ' '
		nline = nline + b
		documents.append(nline)
		print "DocID:{}".format(docID), b
		print 'The document will be inserted into the database and will be available for subsequent queries and functions.\n'

def processInsert(a):
	a = a.split("(", 1)
	a = a[1].split(")", 1)
	addLine = a[0]
	return addLine

def count(field, unique, documents):
	counter = 0
	ucounter = 0
	vals = []
	uList = []
	if unique == '0':
		for line in documents:
			if field in line:
				counter += 1
		print "count_{}:{}\n".format(field, counter)
	if unique == '1':
		for line in documents:
			if field in line:
				line = line.split(field + ":")
				line = line[1].split(' ')
				line[0] = line[0].strip('\n')
				vals.append(line[0])
				for x in vals:
					if x not in uList:
						uList.append(x)
				ucounter  = len(list(uList))
		print "count_{}:{}\n".format(field, ucounter)


def processString(a): #cleans the input query
	a = a.split("[", 1)
	a = a[1].split("]", 1)
	conditions = a[0]
	a = a[1].split("[")
	a = a[1].split("]")
	fields = a[0]
	return [conditions, fields]

def queryError():
    print "query semantic error\n"

def main(): 
	import re
	data = open("data.txt","r")
	documents = data.readlines()
	n = 0
	for each in documents:
		each.strip("\r\n")
	query = open("query.txt","r")
	queries = query.readlines()
	for each in queries:
		each.strip("\r\n")
		if each.startswith("final"):
			r = each.split(".", 1)
			a = r[1]
			if a.startswith("query"):
				a = processString(a)
				queryFunc(a[0], a[1], documents)
			elif a.startswith("count"):
				a = processString(a)
				count(a[0], a[1], documents)
			elif a.startswith("insert"):
				a =processInsert(a)
				insert(a, documents)
			else:
				queryError()
		else:
			queryError()

if __name__== "__main__":
	main()