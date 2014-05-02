#Sarah Jundt and Shannon Lubetich
#AI project
#Spring 2014

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


#write different order method to order sponsor groups with FEWER members to be selected first
def orderSmallestSpogro(domain, sponsorGroups):
	#this is going to be difficult because we actually have no idea what the sizes are till the very end. 
	#when we translate the mapping of person to sponsor group
	#to resulting spogro# to the members of that sponsor group
	#so maybe we should have something that tracks the current size? 


	#so i think this works but we should talk about it
	
	spoGroNumList = sponsorGroups.keys()

	sizeSpogros = [len(x) for x in sponsorGroups.values()]

	smallToLarge = [x for (y,x) in sorted(zip(sizeSpogros, spoGroNumList))]
	print smallToLarge



	return smallToLarge