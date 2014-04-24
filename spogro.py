import helper

def createConstraintGraph(studentPairs, studentFeatures):
	csg = [[0]*len(studentPairs.keys())]*len(studentPairs.keys())
	for i in studentPairs.keys():
		for j in studentPairs.keys():
			if (notTogether(i,studentPairs[i],j,studentPairs[j],studentFeatures)):
				csg[i][j]=1
				csg[j][i]=1
	return csg

def assignmentValid(assignment,csg,newlyAssignedIndex):
	for student in assignment.keys():
		if student!=newlyAssignedIndex and assignment[student]==assignment[newlyAssignedIndex]:
			if csg[newlyAssignedIndex][student]==1:
				return False
	return True


def inference(assignments,domains,csg):
	return domains #return the new set of domains


#assignment is a dictionary
#domains is a dictionary
#csg is a matrix (list of lists) of whether the pairs can be matched.
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
		if (assignmentValid(assignment,csg,nextPair)):
			newDomains = inference(assignment, domains, csg) #NEED TO WRITE. NO IDEA IF THIS IS WHAT WE SHOULD PASS
			result = backtrackingSpoGro(assignment,newDomains,csg)
			if result: #if this recursive assignment works!
				return result
		del assignment[nextPair]

	return None
	

def sortIntoSponsorGroups(studentPairs):
	csg = createConstraintGraph(studentPairs)
	domains = {}
	domainOfEach = [x in range(len(studentPairs))]
	for i in range(len(studentPairs.keys())):
		domains[i]= domainOfEach
	result = backtrackingSpoGro({}, domains, csg)
	print result
	


}
