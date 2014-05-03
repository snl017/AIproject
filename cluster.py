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
	print "these are seeds: " + str(seeds)
	return seeds

#returns the index of the closest centroid
#NOTE: avgPairFeatures does NOT contain information about "F"/"M"
def closestCentroid(studentX, avgPairFeatures, centroids) :

	distances = [float("inf")]*len(centroids)
	#for each centroid
	for i in range(len(centroids)) :
		c = centroids[i]
		#if not(0 in c):
			#print "c is" + str(c)
		diff = []
		#get the distance to the centroid for each feature
		#the c is represented as a list of preferences
		for j in range(len(c)):
			diff.append(abs(c[j]-avgPairFeatures[studentX][j]))
		#get the distance to the centroid, taking into account all features
		distances[i]=numpy.linalg.norm(diff)
	#return the index of the closest centroid
	return distances.index(min(distances))

#TODO: COMPUTE CENTROIDS!!!!!!!!!!!!
def computeCentroids(clusters,K,avgPairFeatures):
	centroids = [-1]*K
	num_features = len(avgPairFeatures[0])
	for i in range(len(clusters)) :
		#i am going to have to average all the things in the cluster,
		#but for now i'm just setting the centroid to be the first one

		#average all things in the cluster
		sums = numpy.array([0]*num_features) #length of number of elements
		averages = [0]*num_features

		#for each student, add their values.
		for studentX in clusters[i]:
			xFeatures = avgPairFeatures[studentX]
			sums = sums + numpy.array(xFeatures)
		for j in range(num_features):
			averages[j] = float(sums[j])/len(clusters[i])

		centroids[i] = averages



		# #average all things in the cluster.
		# sumForCluster =[0]*len(clusters[i][0])
		# #for each student in the cluster:
		# for j in range(len(clusters[i])):
		# 	#average the features
		# 	for k in range(len(sumForCluster)):
		# 		sumForCluster[k] += clusters[i][j] 
		# averageForCluster = [0]*len(clusters[i][0])
		# for k in range(len(averageForCluster):
		# 	sumForCluster[k]= sumForCluster[k]/float(len(clusters[i]))





		#centroids[i] = clusters[i][0]
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
		centroids[i] = avgPairFeatures[seeds[i]]
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
			centroids = computeCentroids(clusters,K,avgPairFeatures)
		i += 1

	print "these are the centroids of our clusters: "
	print centroids

	for clust in clusters :
		print 2*len(clust)

	return clusters




