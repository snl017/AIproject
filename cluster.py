#cluster.py
#Sarah Jundt and Shannon Lubetich
#AI Spring 2014
#Written by Shannon Lubetich

import random
import helper
import numpy

#k-means clustering algorithm for roommate pairs


def selectSeeds(studentPairs, K) :
	random.shuffle(studentPairs)
	seeds = studentPairs[:30]
	print seeds
	return seeds

#returns the index of the closest centroid
#NOTE: avgPairFeatures does NOT contain information about "F"/"M"
def closestCentroid(studentX, avgPairFeatures, centroids) :

	distances = [float("inf")]*len(centroids)
	#for each centroid
	for i in range(len(centroids)) :
		c = centroids[i]
		diff = []
		#get the distance to the centroid for each feature
		for j in range(len(avgPairFeatures[c])):
			diff.append(abs(avgPairFeatures[c][j]-avgPairFeatures[studentX][j]))
		#get the distance to the centroid, taking into account all features
		distances[i]=numpy.linalg.norm(diff)
	#return the index of the closest centroid
	return distances.index(min(distances))

#TODO: COMPUTE CENTROIDS!!!!!!!!!!!!
def computeCentroids(clusters,K):
	centroids = [-1]*K
	for i in range(len(clusters)) :
		#i am going to have to average all the things in the cluster,
		#but for now i'm just setting the centroid to be the first one
		centroids[i] = clusters[i][0]
	#check to make sure all went well
	if -1 in centroids:
		print "computeCentroids failed to compute a centroid!"
	return centroids



def kcluster(studentPairs, studentFeatures, K) :
	avgPairFeatures = helper.averagePref(studentPairs, studentFeatures)
	centroids = [-1]*K
	#initialize the list of lists
	clusters = [-1]*K
	for k in range(K):
		clusters[k]=[]

	seeds = selectSeeds(studentPairs.keys(), K)
	for i in range(K) :
		centroids[i] = seeds[i]
	#check to make sure all went well
	if -1 in centroids:
		print "kclustering did not appropriately add seeds as centroids"
	###stopping criteria, for now, just put 10 iterations

	##TODO: IMPLEMENT STOP CRITERIA
	i = 0
	while i < 10 :
		for k in range(K):
			clusters[k]=[]
		for student in studentPairs.keys() :
			#find the vector with the smallest distance from the centroid = jth cluster
			j = closestCentroid(student, avgPairFeatures, centroids)
			#now add this vector to the list of all vectors associated with this cluster
			clusters[j].append(student)
		for kk in range(K) :
			#recompute centroids
			centroids = computeCentroids(clusters,K)
		i += 1

	#return centroids? really? 
	return clusters




