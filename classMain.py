#
#
# classMain for running on class
#
#
#
#4 spogros of 4-6 people
#

import classGetdata
import roommate
import classSpogro
import helper
from copy import deepcopy

(studentNames, studentDict) = classGetdata.getStudentValues()

domains = roommate.arcConsistentDomains(studentDict)

pairs= roommate.backtrackingPairs({}, domains)
if pairs :
	uniquePairs = roommate.uniquifyPairs(pairs)
	spogros = classSpogro.sortIntoSponsorGroups(uniquePairs,studentDict)
	if spogros :
 		print "Here are the sponsor groups (made by our algorithm): "
		for sg in spogros.keys() :
			print "Sponsor Group #" + str(sg) 
			for stud in spogros[sg] :
				print str(studentNames[stud]) + " and " + str(studentNames[pairs[stud]])
	else :
		print "no spogros"
else :
	print "failed to find pairs"
