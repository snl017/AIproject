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

def closestCentroid(studentX, avgPairFeatures, centroids) :
	distances = []
	for c in len(centroids) :
		distances[c] = numpy.linalg.norm(centroids[x] - avgPairFeatures[x])
	print distances

def computeCentroids(clusters) :
	for i in range(len(clusters)) :
		#i am going to have to average all the things in the cluster,
		#but for now i'm just setting the centroid to be the first one
		centroids[i] = clusters[i][0]
	return centroids



def kcluster(studentPairs, studentFeatures, K) :
	avgPairFeatures = helper.averagePref(studentPairs, studentFeatures)
	centroids = []
	clusters = []
	seeds = selectSeeds(studentPairs, K)
	for i in range(K) :
		centroids[i] = seeds[i]
	###stopping criteria, for now, just put 10 iterations
	i = 0
	while i < 10 :
		for k in range(K) :
			clusters[k] = []
			for student in studentPairs.keys() :
				#find the vector with the smallest distance from the centroid = jth cluster
				j = closestCentroid(student, avgPairFeatures, centroids)
				#now add this vector to the list of all vectors associated with this cluster
				clusters[j] = clusters[j].append(student)
		for kk in range(K) :
			#recompute centroids
			centroids = computeCentroids(clusters)
		i += 1
	#return centroids? really? 
	return centroids



