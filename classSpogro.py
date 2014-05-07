#classSpogro.py

import helper
from copy import deepcopy
import time





#max number of roommate pairs per sponsor group
MAX_PAIRS = 3
#minimum number of roommate pairs per spogro
MIN_PAIRS = 2

NUM_SPOGROS = 4

NUM_STUDENTS = 20


#returns true if pairs i and j CANNOT be in the same group
#returns false if pairs i and j CAN be in the same group
#constraints for sponsor group!
def notTogether(i,j,avgPref):
	#avgPref[i] is a list of 10 elts, indexed 0-9

	highPriority = [0, 2, 3]
	midPriority = [1, 5]
	lowPriority = [4, 6, 7]


	#prioiritize j & k because they haven't been looked at yet
	#difference must be within 3 points
	#
	#j
	if abs(avgPref[i][8] - avgPref[j][8]) > 3 :
		return True
	#
	#k
	if abs(avgPref[i][9] - avgPref[j][9]) > 3:
		return True

	#high priority 
	for q in highPriority :
		#fails if make difference smaller with current numbers
		if abs(avgPref[i][q] - avgPref[j][q]) > 4 :
			return True

	#mid priority
	for q in midPriority :
		if abs(avgPref[i][q] - avgPref[j][q]) > 6 :
			return True

	#low priority
	for q in lowPriority :
		if abs(avgPref[i][q] - avgPref[j][q]) > 7 :
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
	#check if min pairs
	if len(peopleInSpoGro)>MIN_PAIRS:
		needToBeAddedCount = 0
		totalAssigned = 0
		for spogro in assignment.keys():
			spogroLength = len(assignment[spogro])
			totalAssigned+=spogroLength
			if spogroLength<MIN_PAIRS:
				needToBeAddedCount+=(MIN_PAIRS - spogroLength)
		if (NUM_STUDENTS/2 -totalAssigned)<needToBeAddedCount:
			return False

	for student in peopleInSpoGro:
		if student!=newlyAssignedIndex:
			#if the newly assigned student clashes with anyone in their spogro, NO
			if csg[newlyAssignedIndex][student]==1:
				return False


	return True


#uses Forward-checking
#reduces the domains of some roommates according to csg & current assignment
#to speed backtracking
def inference(spogroNum, newstudent, domains,csg):
	for student in domains.keys():
		if csg[newstudent][student]==1 :
			if spogroNum in domains[student]:
				domains[student].remove(spogroNum)
	return domains #return the new set of domains


#assignment is a dictionary
#domains is a dictionary
#csg is a matrix (list of lists) of whether the pairs can be matched.
#puts roommate pairs in sponsor groups
def backtrackingSpoGro(assignment, domains, csg, studentFeatures, assignedStudents, timeout):

	if len(assignedStudents)==len(domains.keys()):
		return assignment

	if time.time()>timeout:
		return None

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
		#print assignment
		#id the assignment is valid, recurse.
		if (assignmentValid(assignment,csg, nextPair, spogro,studentFeatures)):
			#print "is valid"
			#newDomains = domains
			newDomains = inference(spogro, nextPair, domains, csg)
			result = backtrackingSpoGro(assignment,newDomains,csg, studentFeatures, assignedStudents,timeout)
			if result: #if this recursive assignment works!
				return result
		assignment[spogro].remove(nextPair)

	assignedStudents.remove(nextPair)

	return None
	
#sorts students into sponsor groups
#note: studentPairs is a dictionary from half the students to their roommates
def sortIntoSponsorGroups(studentPairs,studentFeatures):
	timeout = time.time()+30
	#creates a csg
	csg = createConstraintGraph(studentPairs,studentFeatures)
	domains = {}
	#gives every roommate pair the opportunity to be with every other roommate pair
	domainOfEach = range(NUM_SPOGROS)
	for i in studentPairs.keys():
		domains[i]= deepcopy(domainOfEach)

	assignment = {}
	for i in range(NUM_SPOGROS):
		assignment[i]=[]

	#backtracks
	result = backtrackingSpoGro(assignment, domains, csg, studentFeatures, [],timeout)

	return result