import helper

## Author: Sarah Jundt
## Puts students into Sponsor Groups based on roommate pairs


#number of sponsor groups
NUM_SPOGROS=30
#max number of roommate pairs per sponsor group
MAX_PAIRS = 10 

#returns whether these four students can be put in the same sponsor group
#constraints for sponsor group!
def notTogether(i,j,k,m,studentFeatures):
	return False



#creates the constraint graph as a matrix where 1 means 
#that the students cannot be in the same spogro
def createConstraintGraph(studentPairs, studentFeatures):
	csg = [[0]*(2*len(studentPairs.keys()))]*(2*len(studentPairs.keys()))
	for i in studentPairs.keys():
		for j in studentPairs.keys():
			if (notTogether(i,studentPairs[i],j,studentPairs[j],studentFeatures)):
				csg[i][j]=1
				csg[j][i]=1
	return csg

#determines and returns whether the assignment is valid based on the constraint graph
#only checks to make sure the new assignment is consistent with all other assignments: 
#must call after each assignment
def assignmentValid(assignment,csg,newlyAssignedIndex):
	peopleInSpoGro=[x for x in assignment.values() if x==assignment[newlyAssignedIndex]]
	if len(peopleInSpoGro)>MAX_PAIRS:
		return False
	for student in assignment.keys():
		if student!=newlyAssignedIndex and assignment[student]==assignment[newlyAssignedIndex]:
			if csg[newlyAssignedIndex][student]==1:
				return False
	return True


#uses some inference (forward-checking someday?)
#reduces the domains of some roommates according to csg & current assignment
#to speed backtracking
def inference(assignments,domains,csg):
	return domains #return the new set of domains


#assignment is a dictionary
#domains is a dictionary
#csg is a matrix (list of lists) of whether the pairs can be matched.
#puts roommate pairs in sponsor groups
def backtrackingSpoGro(assignment, domains, csg):
	if len(assignment)==len(domains.keys()):
		return assignment

	#  X select unassigned variable 
	# USE HEURISTIC
	nextPair = helper.heuristic(assignment.keys(),domains)


	#select an ordering for the domain of X 
	orderedDomainValues = helper.order(domains[nextPair])
	
	
	# #  for each value in D 
	for spogro in orderedDomainValues:
		#  add the pair to assignment 
		assignment[nextPair]=spogro
		# print spogro
		if (assignmentValid(assignment,csg,nextPair)):
			newDomains = inference(assignment, domains, csg) #NEED TO WRITE. NO IDEA IF THIS IS WHAT WE SHOULD PASS
			result = backtrackingSpoGro(assignment,newDomains,csg)
			if result: #if this recursive assignment works!
				return result
		del assignment[nextPair]

	return None
	
#sorts students into sponsor groups
#note: studentPairs is a dictionary from half the students to their roommates
def sortIntoSponsorGroups(studentPairs,studentFeatures):
	#creates a csg
	csg = createConstraintGraph(studentPairs,studentFeatures)
	domains = {}
	#gives every roommate pair the opportunity to be with every other roommate pair
	domainOfEach = range(NUM_SPOGROS)
	for i in studentPairs.keys():
		domains[i]= domainOfEach

	#backtracks
	result = backtrackingSpoGro({}, domains, csg)
	
	#puts students into lists based on their sponsor group
	toReturn = {}
	for i in range(NUM_SPOGROS):
		toReturn[i]=[]
	
	for person in result.keys():
		spogro= toReturn[result[person]]
		spogro.append(person)
		spogro.append(studentPairs[person])
		
		toReturn[result[person]]=spogro

	#returns a dictionary of sponsor group number to the students in that sponsor group
	return toReturn
	


