#Sarah Jundt and Shannon Lubetich
#AI project
#Spring 2014

import random


#number of sponsor groups
NUM_SPOGROS=30
#helper methods


#put the students into a dictionary where a student maps to its sponsor group
def studentMaps(assignment):
	i = 0
	toReturn = {}
	for spogro in assignment.values():
		for student in spogro:
			toReturn[student]=i
		i+=1
	return toReturn


#get the purity of a clustering given the assignment
def purity(clusters, assignment):
	studentAssignments = studentMaps(assignment)
	correct = 0
	total = 0
	#for each cluster
	for cluster in clusters:
		numsOfEachLabel = [0]*NUM_SPOGROS
		for student in cluster:
			#find its label
			label = studentAssignments[student]
			numsOfEachLabel[label]+=1
		#find the best label for this cluster
		bestLabel = numsOfEachLabel.index(max(numsOfEachLabel))
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
		if not (i in alreadyAssigned):
			if smallestDomain>len(domains[i]):
				smallestDomain=len(domains[i])
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
	#print smallToLarge
	return smallToLarge



#returns a dictionary of 1st student in roommate pair mapped to 
#a feature vector that is an average of their preferences
def averagePref(studentPairs, studentFeatures) :
	avgPref = {}
	for studentX in studentPairs.keys():
		studentY = studentPairs[studentX]
		xFea = studentFeatures[x]
		yFea = studentFeatures[y]
		avg = []
		for i in len(xFea) :
			avg[i] = float((xFea[i]+yFea[i]))/2
		avgPref[studentX] = avg
	return avgPref
