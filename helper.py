#Sarah Jundt and Shannon Lubetich
#AI project
#Spring 2014

import random
import numpy


#number of sponsor groups
NUM_SPOGROS=30
#number of students
NUM_STUDENTS = 414
#helper methods

def computeAverageForList(avgPairFeatures,cluster):
	num_featuresOfList = len(avgPairFeatures[0])
	#average all things in the cluster
	sums = numpy.array([0]*num_featuresOfList) #length of number of elements
	averagesToReturn = [0]*num_featuresOfList

	#for each student, add their values.
	for studentX in cluster:
		xFeatures = avgPairFeatures[studentX]
		sums = sums + numpy.array(xFeatures)
	for j in range(num_featuresOfList):
		averagesToReturn[j] = round(float(sums[j])/len(cluster),3)
	#return the averages
	return averagesToReturn


#ANALYZES THE OUTPUT
#note: clustering & spogros are incomplete. student features is actually averages.
def analyze(studentFeaturesForPair, clustering, spogros, purity):
	num_features = len(studentFeaturesForPair)
	toPrintSpogroList = []
	print "Purity: "+str(purity)
	print "Sponsor Group:"
	lengths = [len(spogro1) for spogro1 in spogros.values()]
	print "Maximum size spogro: "+str(max(lengths)*2)
	print "Minimum size spogro: "+str(min(lengths)*2)
	#find average feature set for each spogro. 
	for i in spogros.keys():
		studentAverages = computeAverageForList(studentFeaturesForPair,spogros[i])
		for x in studentAverages:
			if x<=2 or x>=9:
				print "For Sponsor Group "+str(i)+", of size "+str(len(spogros[i])) +". Averages: "
				print computeAverageForList(studentFeaturesForPair,spogros[i])
				toPrintSpogroList.append(i)

	print "Clusters:"
	lengths = [len(cluster) for cluster in clustering]
	print "Maximum size cluster: "+str(max(lengths)*2)
	print "Minimum size spogro: "+str(min(lengths)*2)
	for i in range(len(clustering)) :
		majorityLabelForCluster = majorityLabel(clustering[i], spogros)
		if majorityLabelForCluster in toPrintSpogroList:
			print "For Cluster with Majority Label "+str(majorityLabel(clustering[i],spogros))+", of size "+str(len(clustering[i]) )+" Averages: "
			print computeAverageForList(studentFeaturesForPair,clustering[i])





#put the students into a dictionary where a student maps to its sponsor group
def studentMaps(assignment):
	i = 0
	toReturn = {}
	numStudents = 0
	for spogro in assignment.values():
		for student in spogro:
			toReturn[student]=i
			numStudents += 1
		i+=1
	#print "STUDENTS NUM: " + str(numStudents)
	return toReturn

def majorityLabel(cluster,assignment):
	numsOfEachLabel = [0]*NUM_SPOGROS
	studentAssignments = studentMaps(assignment)
	for student in cluster:
		#find its label
		label = studentAssignments[student]
		numsOfEachLabel[label]+=1
	#find the best label for this cluster
	return numsOfEachLabel.index(max(numsOfEachLabel))


#get the purity of a clustering given the assignment
def purity(clusters, assignment):
	studentAssignments = studentMaps(assignment)
	correct = 0
	total = 0
	#for each cluster
	for cluster in clusters:
		bestLabel = majorityLabel(cluster, assignment)
		#find the number of students in this cluster for which the label is correct
		for student in cluster:
			total +=1
			if bestLabel==studentAssignments[student]:
				correct+=1
	#return the purity of the clustering as a whole
	return float(correct)/float(total)


#finds the next student to assign
#chooses the student with the smallest domain
def heuristic(alreadyAssigned, domains):
	smallestDomain = float("inf")
	toReturn = None
	for i in domains.keys():
		length = len(domains[i])
		if not (i in alreadyAssigned):
			if smallestDomain>length:
				smallestDomain=length
				toReturn =i

	return toReturn
	

#takes as param the domain as a list
def order(domain):
	#randomly shuffle the possible domains of students and return
	random.shuffle(domain)
	return domain


#write different order method to order sponsor groups with FEWER members to be selected first
def orderSmallestSpogro(domain, sponsorGroups):
	#this is going to be difficult because we actually have no idea what the sizes are till the very end. 
	#when we translate the mapping of person to sponsor group
	#to resulting spogro# to the members of that sponsor group
	#so maybe we should have something that tracks the current size? 


	#so i think this works but we should talk about it

	spoGroNumList = sponsorGroups.keys()

	sizeSpogros = [len(x) for x in sponsorGroups.values()]

	smallToLarge = [x for (y,x) in sorted(zip(sizeSpogros, spoGroNumList))]
	toReturn = []
	for elt in smallToLarge : 
		if elt in domain : 
			toReturn.append(elt) 
	return toReturn



#returns a dictionary of 1st student in roommate pair mapped to 
#a feature vector that is an average of their preferences
#returns average preferences of the roommate pair WITHOUT information about their sex/gender
def averagePref(studentPairs, studentFeatures) :
	avgPref = {}
	for studentX in studentPairs.keys():
		studentY = studentPairs[studentX]
		xFea = studentFeatures[studentX]
		yFea = studentFeatures[studentY]
		avg = []
		#REMOVE THE GENDER/SEX.
		#KEEP ONLY NUMERIC VALUES
		for i in range(len(xFea)) :
			if i>0:
				avg.append(float((xFea[i]+yFea[i]))/2)
		#set the average preferences of the student in studentFeatures
		avgPref[studentX] = avg

	return avgPref

	##OLD CODE
	# avgPref = {}
	# for studentX in studentPairs.keys():
	# 	studentY = studentPairs[studentX]
	# 	xFea = studentFeatures[studentX]
	# 	yFea = studentFeatures[studentY]
	# 	avg = [-1]*len(xFea)
	# 	#keep the gender/sex: no need to average
	# 	# avg[0]=xFea[0]
	# 	# avg[1]=xFea[1]
	# 	#for all the other features, average them
	# 	for i in range(len(xFea)) :
	# 		if i>1:
	# 			avg[i] = float((xFea[i]+yFea[i]))/2
	# 	#check for errors in assignment
	# 	if -1 in avg:
	# 		print "ERROR: averagePref did not assign a value" 
	# 	#set the average preferences of the student in studentFeatures
	# 	avgPref[studentX] = avg

	# return avgPref
