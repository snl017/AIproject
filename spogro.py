
# coding: utf-8
#for some reason this was needed because I was getting a weird character thing? 
# apparently, it's something in the giant comment block detailing the question information, 
#but includeing this coding eliminates the error

##Sarah Jundt and Shannon Lubetich
##AI project
#Spring 2014
## Author: Sarah Jundt
## Puts students into Sponsor Groups based on roommate pairs

import helper
from copy import deepcopy





#max number of roommate pairs per sponsor group
MAX_PAIRS = 10 


"""
a. Is serious about studying and will make studying a priority of our room.*
b. Allows me to have visitors over as often as I’d like and doesn’t mind having people over in our room.**
c. Will be my friend who confides in me and likes to do a lot of things together.*
d. Doesn’t let school take over our entire lives, and knows how to have a good time.*
e. Shares responsibility for keeping our room neat.***
f. Respects my need for privacy and will allow me some time to myself.**
g. Respects my property and doesn’t borrow my things without asking.***
h. Has similar sleep habits (i.e. windows opened/closed, absolute quiet, no light, etc.)***

j. There are people who share backgrounds and cultures similar to my own.
k. People are aware of, sensitive to, and willing to discuss multicultural issues.


* = highPriority
** = midPriority
*** = lowPriority

"""

#returns true if pairs i and j CANNOT be in the same group
#returns false if pairs i and j CAN be in the same group
#constraints for sponsor group!
def notTogether(i,j,avgPref):
	#avgPref[i] is a list of 10 elts, indexed 0-9

	highPriority = [0, 2, 3]
	midPriority = [1, 5]
	lowPriority = [4, 6, 7]


	"""
	FUN STUFF
	there are only 29 pairs assigned when we use these constraints, 
	and yet it doesn't return None
	"""

	#prioiritize j & k because they haven't been looked at yet
	#difference must be within 3 points
	#
	#j
	if abs(avgPref[i][8] - avgPref[j][8]) > -1 :
		return True
	#
	#k
	if abs(avgPref[i][9] - avgPref[j][9]) > 8:
		return True

	#high priority 
	for q in highPriority :
		if abs(avgPref[i][q] - avgPref[j][q]) > 91 :
			return True

	#mid priority
	for q in midPriority :
		if abs(avgPref[i][q] - avgPref[j][q]) > 91 :
			return True

	#low priority
	for q in lowPriority :
		if abs(avgPref[i][q] - avgPref[j][q]) > 91 :
			return True

	#if none of these things happen, then people are similar and we're good! we can put these pairs together! 
	return False



#creates the constraint graph as a matrix where 1 means 
#that the students cannot be in the same spogro
def createConstraintGraph(studentPairs, studentFeatures):
	avgPref = helper.averagePref(studentPairs, studentFeatures)

	numRowsCols = 2*len(studentPairs.keys())
	csg = [[0]*numRowsCols for i in range (numRowsCols)]
	for i in studentPairs.keys():
		for j in studentPairs.keys():
			if (notTogether(i,j,avgPref)):
				csg[i][j]=1
				csg[j][i]=1
	return csg

#determines and returns whether the assignment is valid based on the constraint graph
#only checks to make sure the new assignment is consistent with all other assignments: 
#must call after each assignment
def assignmentValid(assignment,csg, newlyAssignedIndex, spogro, studentFeatures):
	peopleInSpoGro=assignment[spogro]
	#if spogro is too large:
	if len(peopleInSpoGro)>MAX_PAIRS:
		return False
	if len(peopleInSpoGro)==1:
		return True
	#counter for male students in spogro
	male = 0
	#count the number of males
	for student in peopleInSpoGro:
		if student!=newlyAssignedIndex:
			if studentFeatures[student][0]=="M":
				male+=1
			#if the newly assigned student clashes with anyone in their spogro, NO
			if csg[newlyAssignedIndex][student]==1:
				return False
	#percent of male students in spogro
	percentMale = float(male) /float(len(peopleInSpoGro)-1)
	#if we've assigned more than 2, keep genders balanced.

	if (len(peopleInSpoGro)>2):
		if ((percentMale>0.5 and studentFeatures[newlyAssignedIndex][0]=="M") or (percentMale<0.5 and studentFeatures[newlyAssignedIndex][0]=="F")):
			return False

	return True


#uses Forward-checking
#reduces the domains of some roommates according to csg & current assignment
#to speed backtracking
def inference(spogroNum, newstudent, domains,csg):
	for student in domains.keys():
		if csg[newstudent][student]==1 and spogroNum in domains[student]:
			domains[student].remove(spogroNum)
	return domains #return the new set of domains


#assignment is a dictionary
#domains is a dictionary
#csg is a matrix (list of lists) of whether the pairs can be matched.
#puts roommate pairs in sponsor groups
def backtrackingSpoGro(assignment, domains, csg, studentFeatures, assignedStudents):

	if len(assignedStudents)==len(domains.keys()):
		return assignment

	#  X select unassigned variable 
	# USE HEURISTIC
	nextPair = helper.heuristic(assignedStudents,domains)
	assignedStudents.append(nextPair)

	#select an ordering for the domain of X 
	orderedDomainValues = helper.orderSmallestSpogro(domains[nextPair],assignment)
	
	# #  for each value in D 
	for spogro in orderedDomainValues:
		#  add the pair to assignment 
		assignment[spogro].append(nextPair)
		#id the assignment is valid, recurse.
		if (assignmentValid(assignment,csg, nextPair, spogro,studentFeatures)):
			#newDomains = domains
			newDomains = inference(spogro, nextPair, domains, csg)
			result = backtrackingSpoGro(assignment,newDomains,csg, studentFeatures, assignedStudents)
			if result: #if this recursive assignment works!
				print "should return result"
				return result
		assignment[spogro].remove(nextPair)

	assignedStudents.remove(nextPair)

	return None
	
#sorts students into sponsor groups
#note: studentPairs is a dictionary from half the students to their roommates
def sortIntoSponsorGroups(studentPairs,studentFeatures):
	#creates a csg
	csg = createConstraintGraph(studentPairs,studentFeatures)
	domains = {}
	#gives every roommate pair the opportunity to be with every other roommate pair
	domainOfEach = range(helper.NUM_SPOGROS)
	for i in studentPairs.keys():
		domains[i]= deepcopy(domainOfEach)

	assignment = {}
	for i in range(helper.NUM_SPOGROS):
		assignment[i]=[]

	#backtracks
	result = backtrackingSpoGro(assignment, domains, csg, studentFeatures, [])

	return result


