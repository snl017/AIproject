import random


#helper methods



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
	#randomly shuffle the possible domains of students and return
	random.shuffle(domain)
	return domain