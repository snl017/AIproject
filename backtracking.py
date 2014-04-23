# RUN AC-3
# then RUN 



# function CSP-BACKTRACKING(assignment) returns a solution or failure 



NUM_STUDENTS=415




def heuristic(alreadyAssigned, domainsArray):
	smallestDomain = float("inf")
	toReturn = None
	for i in range(NUM_STUDENTS):
		if not (i in alreadyAssigned):
			if smallestDomain>len(domainsArray[i]):
				smallestDomain=len(domainsArray[i])
				toReturn =i

	return toReturn


	

#takes as param the domain as a list
def order(domain):
	#CHANGE NOTHING
	return domain

def domainRemove(nextStudent,roommatePossibility,domainsArray):
	#if domain remove works, return domainsArray.
	for index in range(NUM_STUDENTS):
		if nextStudent in domainsArray[index]:
			domainsArray[index].remove(nextStudent)
		if roommatePossibility in domainsArray[index]:
			domainsArray[index].remove(roommatePossibility)
		if len(domainsArray[index])==0:
			#if this domain is empty now, return None
			return None

	#return the satisfactory domainsArray with the roommate pair removed from all domains
	return domainsArray
	

#dictionary of assignments
#array of lists for domains
def backtracking(assignment,domainsArray):
	#  if assignment complete return assignment 
	if (len(assignment==NUM_STUDENTS)):
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


	



