


# RUN AC-3


# function CSP-BACKTRACKING(assignment) returns a solution or failure 
# THIS RUNS FAKE BACKTRACKING ON THE STUDENTS TO HAVE THEM PUT IN ROOMMATE PAIRS




#finds the next student to assign
#chooses the student with the smallest domain
def heuristic(alreadyAssigned, domainsArray):
	smallestDomain = float("inf")
	toReturn = None
	for i in range(len(domainsArray)):
		if not (i in alreadyAssigned):
			if smallestDomain>len(domainsArray[i]):
				smallestDomain=len(domainsArray[i])
				toReturn =i

	return toReturn
	

#takes as param the domain as a list
def order(domain):
	#change nothing. 
	return domain

#remove students that have been assigned 
#if this assignment leaves someone with nothing in their domain, return NONE
def domainRemove(student1,student2,domainsArray):
	#if domain remove works, return domainsArray.
	for index in range(len(domainsArray)):
		if student1 in domainsArray[index]:
			domainsArray[index].remove(student1)
		if student2 in domainsArray[index]:
			domainsArray[index].remove(student2)
		if len(domainsArray[index])==0:
			#if this domain is empty now, return None
			return None

	#return the satisfactory domainsArray with the roommate pair removed from all domains
	return domainsArray
	

#param: assignment: dictionary of assignments
#param: domainsArray: array of lists for domains
#Recursive algorithm assigns roommate pairs
#returns None if no assignment can be found (failure)

def backtrackingPairs(assignment,domainsArray):
	#  if assignment complete return assignment 
	if (len(assignment==len(domainsArray))):
		return assignment

	#  X select unassigned variable 
	nextStudent = heuristic(assignment.keys(),heuristic)
	#  D select an ordering for the domain of X 
	orderedDomainValues = order(domainsArray[nextStudent])
	
	#  for each value in D 
	for roommatePossibility in orderedDomainValues:
		#  add the pair to assignment 
		assignment[nextStudent]=roommatePossibility
		assignment[roommatePossibility]=nextStudent
		#remove the roommates from everyone else's domain
		newDomainsArray = domainRemove()
		if newDomainsArray:
			#go recursively.
			#  result CSP-BACKTRACKING(assignment) 
			result = backtracking(assignment,newDomainsArray)
			if result: #if result isn't failure
				return result

	#if we have no roommate assignment that will work in our domain, return null (failure)
	return None


	#DO PREPROCESSING -> PEOPLE AS FEATURE ARRAYS 
	#RUN AC-# ON PEOPLE
	#RUN BACKTRACKING_PAIRS (above, not really backtracking) ON PEOPLE -> ROOMMATES
	
	#RUN AC-# ON ROOMMATE PAIRS
	#RUN REAL BACKTRACKING ON ROOMMATE PAIRS AS WE ASSIGN TO SPONSOR GROUPS



