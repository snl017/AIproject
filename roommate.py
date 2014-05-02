#Sarah Jundt and Shannon Lubetich
#AI project
#Spring 2014

# pairs roommates based on 8 features rating importance of certain roommate qualities
# 0 = not important to 9 = very important


import getdata
import helper

#FAKE AC-3

#checks the constraints
#returns whether the pair can be roommates
#studentFeatures is a dictionary
#x,y are indices of students
def pairAllowed(x,y,studentFeatures):
	#THIS IS WHERE WE PUT CONSTRAINTS
	#e.g. if studentFeaturesArray[x]<3 & studentFeaturesArray[y]>6...
	#if we reach a constraint for which it doesn't work, return false.
	#otherwise return true.
	#
	#We will see how different the variables are, narrowing down till it fails, 
	# and then going one up
	for featureIdx in range(1,len(studentFeatures[x])) :
		if abs(studentFeatures[x][featureIdx] - studentFeatures[y][featureIdx]) >= 7 :
			return False
	return True
	#FINDINGS:
	#when ranked values must have a difference smaller than 6, females get paired and males do NOT
	#when ranked values must have a difference smaller than 7, matches can be found for all

# Gets the (arc-consistent) domains for each of the students
# student features array is a dictionary
def arcConsistentDomains(studentFeaturesArray):
	#arcs that have already been checked: tuples (i,j) and (j,i)
	domains = {}
	for i in studentFeaturesArray.keys():
		#the domain of this student
		iDomain = []
		#for each other student, check if they could be roommates
		for j in studentFeaturesArray.keys():
			if (i!=j):
				if pairAllowed(i,j,studentFeaturesArray):
					iDomain.append(j)
		#add the domain
		domains[i] = iDomain
	return domains



# THIS RUNS FAKE BACKTRACKING ON THE STUDENTS TO HAVE THEM PUT IN ROOMMATE PAIRS


#remove students that have been assigned 
#if this assignment leaves someone with nothing in their domain, return NONE
def domainRemove(student1,student2,domains,alreadyAssigned):
	#if domain remove works, return domainsArray.
	for index in domains.keys():
		#if the student already has a roommate, don't worry about changing its domain
		if not (index in alreadyAssigned):
			if student1 in domains[index]:
				domains[index].remove(student1)
			if student2 in domains[index]:
				domains[index].remove(student2)
			if len(domains[index])==0:
				#if this domain is empty now, return None
				return None

	#return the satisfactory domainsArray with the roommate pair removed from all domains
	return domains
	

#param: assignment: dictionary of assignments
#param: domainsArray: array of lists for domains
#Recursive algorithm assigns roommate pairs
#returns None if no assignment can be found (failure)

def backtrackingPairs(assignment,domains):
	#  if assignment complete return assignment 
	if (len(assignment)==len(domains.keys())):
		return assignment

	#  X select unassigned variable 
	#USE HEURISTIC
	nextStudent = helper.heuristic(assignment.keys(),domains)

	#  D select an ordering for the domain of X 
	orderedDomainValues = helper.order(domains[nextStudent])
	
	#  for each value in D 
	for roommatePossibility in orderedDomainValues:
		#  add the pair to assignment 
		assignment[nextStudent]=roommatePossibility
		assignment[roommatePossibility]=nextStudent
		#remove the roommates from everyone else's domain
		newDomains = domainRemove(nextStudent,roommatePossibility,domains,assignment.keys())
		if newDomains:
			#go recursively.
			#  result CSP-BACKTRACKING(assignment) 
			result = backtrackingPairs(assignment,newDomains)
			if result: #if result isn't failure
				return result

	#if we have no roommate assignment that will work in our domain, return None (failure)
	return None



#this helper function takes in full dictionary of mapping every single student to their roommate pair
#it returns a dictionary of the student with the lower id number of a student pair mapped to their roommate
#this roommate then has no entry in the returned dictionary
def uniquifyPairs(dictionary) :
	studentKeys = dictionary.keys()
	for key in studentKeys :
		otherStudentToDelete = dictionary[key]
		del dictionary[otherStudentToDelete]
		studentKeys.remove(otherStudentToDelete)
	return dictionary







