import getdata
import roommate
#import spogro


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
	print pairs
	print len(pairs)
	uniquePairs = roommate.uniquifyPairs(pairs)
	print uniquePairs
	print len(uniquePairs)
else :
	if(malePairs) :
		print "Failed to find female roommate pairings"
	if(femalePairs) :
		print "Failed to find male roommate pairings"
	else:
		print "Failed to find roommate pairs satisfying constraints"
	
	#RUN AC-3 ON ROOMMATE PAIRS
	#RUN REAL BACKTRACKING ON ROOMMATE PAIRS AS WE ASSIGN TO SPONSOR GROUPS