#Sarah Jundt and Shannon Lubetich
#AI project
#Spring 2014


import getdata
import roommate
import spogro
import helper
import cluster
from copy import deepcopy

NUM_RUNS = 300


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


totalPurity = 0
successfulRuns = 0
averageAnalysesSpogro = []
averageAnalysesTotal = []
for runNum in range(NUM_RUNS):
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
		#print"Roommate pairs:"
		#print pairs
		# print len(pairs)
		uniquePairs = roommate.uniquifyPairs(pairs)

		#get the clustering of the students	
		clustering = cluster.kcluster(uniquePairs,studentDict,helper.NUM_SPOGROS)
		allStudentsClustering = deepcopy(clustering)

		for cluster1 in allStudentsClustering:
			for student in uniquePairs.keys():
				if student in cluster1:
					cluster1.append(uniquePairs[student])
		#print "Clustering for run"+str(runNum)
		#print allStudentsClustering
		#print uniquePairs

		# #use for testing (by just replacing uniquePairs with uniquePairsTEST below)
		# uniquePairsTEST = {}
		# for i in range(3) :
		# 	stud = uniquePairs.keys()[i]
		# 	uniquePairsTEST[stud] = uniquePairs[stud]


		spogros = spogro.sortIntoSponsorGroups(uniquePairs,studentDict)

		#if sponsor groups could not be assigned
		#if not spogros :
		#	print "Students were not sorted into sponsor groups in run "+str(runNum)
		#else:
		if spogros: 
			successfulRuns+=1

			#get the purity
			purity = helper.purity(clustering,spogros)
			totalPurity +=purity

			# #PRINT OUTPUTS
			# #print "Run "+str(runNum)+":"
			# #print "The sponsor groups were created with "+str(purity)+" purity!"
			# #puts students' roommate pairs into their sponsor groups
			# spogrosWithAllStudents = deepcopy(spogros)
			# for sponsorgro in spogrosWithAllStudents.values():
		 # 		for student in uniquePairs.keys():
		 # 			if student in sponsorgro:
		 # 				sponsorgro.append(uniquePairs[student])

		 # 	#print "Here are the sponsor groups (made by our algorithm): "
			# #print spogrosWithAllStudents
			# #lengths = [len(spogro1) for spogro1 in spogrosWithAllStudents.values()]
			# #print "Maximum size spogro: "+str(max(lengths))
			# #print "Minimum size spogro: "+str(min(lengths))
			averageFeatures = helper.averagePref(uniquePairs,studentDict)
			averageAnalyses = helper.analyze(averageFeatures, clustering, spogros, purity)
			averageAnalysesSpogro.append(averageAnalyses[0])
			averageAnalysesTotal.append(averageAnalyses[1])

	# else :
	# 	if(malePairs) :
	# 		print "Failed to find female roommate pairings for run "+str(runNum)
	# 	elif(femalePairs) :
	# 		print "Failed to find male roommate pairings for run "+str(runNum)
	# 	else:
	# 		print "Failed to find roommate pairs satisfying constraints for run "+str(runNum)
	
print "Successful Runs: "+str(successfulRuns)+"/"+str(NUM_RUNS)
print "Average Purity: "+str(totalPurity/float(successfulRuns))
print "Average analysis:"
averagesSpogro = helper.average(averageAnalysesSpogro)
averagesTotal = helper.average(averageAnalysesTotal)
print "Average distance over all runs from students to spogro centroids:"
print averagesSpogro
print "Average distance over all runs from students to average for all students:"
print averagesTotal
	#RUN AC-3 ON ROOMMATE PAIRS
	#RUN REAL BACKTRACKING ON ROOMMATE PAIRS AS WE ASSIGN TO SPONSOR GROUPS