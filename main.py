#Sarah Jundt and Shannon Lubetich
#AI project
#Spring 2014


import getdata
import roommate
import spogro
import helper
import cluster
from copy import deepcopy


#MAIN FUNCTION

#get the student feature vectors as a dictionary
#DO PREPROCESSING -> PEOPLE AS FEATURE ARRAYS 
studentDict=getdata.getStudentValues()

#split them into male and female
maleStudentsFeatures = {}
femaleStudentsFeatures = {}
for i in studentDict.keys():
	if studentDict[i][0]=="M":
		maleStudentsFeatures[i]=studentDict[i]
	else:
		femaleStudentsFeatures[i]=studentDict[i]

#RUN AC-3 ON PEOPLE
#create the array of arc-consistent domains (possible roommates) for each student
domainsMale= roommate.arcConsistentDomains(maleStudentsFeatures)
domainsFemale = roommate.arcConsistentDomains(femaleStudentsFeatures)

#RUN BACKTRACKING_PAIRS ON PEOPLE -> ROOMMATES
#get the set of roommate pairs
malePairs= roommate.backtrackingPairs({}, domainsMale) #this is a dictionary of the roommate pairs!
femalePairs = roommate.backtrackingPairs({}, domainsFemale)
if(malePairs and femalePairs) :
	malePairs.update(femalePairs)
	pairs = malePairs
	# print pairs
	# print len(pairs)
	uniquePairs = roommate.uniquifyPairs(pairs)
	#print uniquePairs
	for i in range(1) :
		spogros = spogro.sortIntoSponsorGroups(uniquePairs,studentDict)

		#get the clustering of the students	
		clustering = cluster.kcluster(uniquePairs,studentDict,helper.NUM_SPOGROS)
		
		#get the purity
		purity = helper.purity(clustering,spogros)


		#PRINT OUTPUTS
		print "Pairing "+str(i)+":"
		print "The sponsor groups were created with "+str(purity)+" purity!"
		#puts students' roommate pairs into their sponsor groups
		spogrosWithAllStudents = deepcopy(spogros)
		for spogro in spogrosWithAllStudents.values():
	 		for student in uniquePairs.keys():
	 			if student in spogro:
	 				spogro.append(uniquePairs[student])
	 	print "Here are the sponsor groups (made by our algorithm): "
		print spogrosWithAllStudents
		lengths = [len(spogro) for spogro in spogrosWithAllStudents.values()]
		print "Maximum size spogro: "+str(max(lengths))
		print "Minimum size spogro: "+str(min(lengths))



else :
	if(malePairs) :
		print "Failed to find female roommate pairings"
	elif(femalePairs) :
		print "Failed to find male roommate pairings"
	else:
		print "Failed to find roommate pairs satisfying constraints"
	
	#RUN AC-3 ON ROOMMATE PAIRS
	#RUN REAL BACKTRACKING ON ROOMMATE PAIRS AS WE ASSIGN TO SPONSOR GROUPS