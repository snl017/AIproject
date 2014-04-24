import getdata

#FAKE AC-3

#checks the constraints
#returns whether the pair can be roommates
#studentFeaturesArray is a dictionary
#x,y are indices of students
def pairAllowed(x,y,studentFeaturesArray):
	#THIS IS WHERE WE PUT CONSTRAINTS
	#e.g. if studentFeaturesArray[x]<3 & studentFeaturesArray[y]>6...
	#if we reach a constraint for which it doesn't work, return false.
	#otherwise return true.
	return True

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

#finds the next student to assign
#chooses the student with the smallest domain
def heuristic(alreadyAssigned, domains):
	smallestDomain = float("inf")
	toReturn = None
	for i in domains.keys():
		if not (i in alreadyAssigned):
			if smallestDomain>len(domains[i]):
				smallestDomain=len(domains[i])
				toReturn =i

	return toReturn
	

#takes as param the domain as a list
def order(domain):
	#change nothing. 
	return domain

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
	nextStudent = heuristic(assignment.keys(),domains)

	#  D select an ordering for the domain of X 
	orderedDomainValues = order(domains[nextStudent])
	
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



#MAIN FUNCTION

#get the student feature vectors as a dictionary
#DO PREPROCESSING -> PEOPLE AS FEATURE ARRAYS 
studentFeaturesArray=getdata.getStudentValues()
studentDict = {}
for i in range(len(studentFeaturesArray)):
	studentDict[i]=studentFeaturesArray[i]


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
domainsMale=arcConsistentDomains(maleStudentsFeatures)
domainsFemale = arcConsistentDomains(femaleStudentsFeatures)

#RUN BACKTRACKING_PAIRS ON PEOPLE -> ROOMMATES
#get the set of roommate pairs
malePairs= backtrackingPairs({}, domainsMale) #this is a dictionary of the roommate pairs!
femalePairs = backtrackingPairs({}, domainsFemale)
malePairs.update(femalePairs)
pairs = malePairs
print pairs
print len(pairs)


	
	
	
	
	#RUN AC-3 ON ROOMMATE PAIRS
	#RUN REAL BACKTRACKING ON ROOMMATE PAIRS AS WE ASSIGN TO SPONSOR GROUPS



