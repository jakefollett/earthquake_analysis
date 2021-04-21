

import doctest
import csv
import math
import random
from turtle import *

    

def readFile(fname):
    '''(fname: str) -> dict

    This function will take the file name and
    return the dictionary that has latitude and
    longitude in a list and the dictionary that contains
    the magnitudes
    '''
    with open(fname, encoding='utf8') as dataFile:
        csvReader = csv.reader(dataFile)
        titles = next(csvReader)
        dataDict = {}
        dataDictMag = {}
        key = 0

        for line in csvReader:
            key += 1
            lat = float(line[1])
            long = float(line[2])
            mag = float(line[4])
            dataDict[key] = [long, lat]
            dataDictMag[key] = mag # so we can use this dict in eqDraw
    return dataDict, dataDictMag

#print(readFile('p7b-equakes50f.csv'))
            
def eucliD(point1, point2):
    '''(point1: list, point2: list) -> float

    this function will take 2 points that are list that are
    float values and return float value using for loop to
    calculate the distance between the two also you can
    calculate at any dimensions

    >>> eucliD([5,6], [1,3])
    5.0
    >>> eucliD([100, 3, 8, 20], [20.345, 10.2, 4.2, -30.4])
    94.6116220397896
    >>> eucliD([], [])
    0.0
    '''
    total = 0
    for ind in range(len(point1)):
        diff = (point1[ind] - point2[ind]) ** 2
        total += diff
    distance = math.sqrt(total)
    return distance

#print(eucliD([], []))

def createCentroids(k, dataDict):
    '''(k: int, dataDict: dict) -> list

    This function will take k which is the number
    of centroids that we want and dataDict the dictionary
    that we created from readFile function and return the
    list of centroids. We will use module random to use randint
    to get random centroids and we will do this for k times make
    sure if there's not any duplicates in centroids
    '''
    li_centroids = []
    li_keys = []
    count = 0

    while count < k: # use while loop because you don't know exactly how many times you want to iterate
        aKey = random.randint(1, len(dataDict))
        if aKey not in li_keys:
            li_centroids.append(dataDict[aKey])
            li_keys.append(aKey)
            count += 1
    return li_centroids


#print(createCentroids(5, readFile('p7b-equakes50f.csv')))
    
def createClusters(k, centroids, dataDict, repeats):
    '''(k: int, centroids: list, dataDict: dict, repeats: int) -> list
    
    This function will take k which is how many centroids you want
    and centroids list of centroids and dataDict from readFile function
    and repeats how many time you want to repeat. In my case I don't have
    to use repeat because I use while loop to end the program.
    In this fuction we create a list of clusters by calculating the data point
    and each centroids and whichever one that was the closest will get appended
    in the same index after that take the average with in each clusters and that
    will be our new centroids and repeat this process until previousCluster is equal to
    the clusters
    '''
    previousClusters = []
    for i in range(k):
        previousClusters.append([])
    aPass = 1
    continueOrNot = True
    
    while continueOrNot:
        print(f'{aPass:>20} cycle')

        clusters = []
        for i in range(k):
            clusters.append([])

        for aKey in dataDict:
            distances = []
            for clusterIndex in range(k):
                distance = eucliD(dataDict[aKey], centroids[clusterIndex])
                distances.append(distance)

            minDist = min(distances)
            index = distances.index(minDist)

            clusters[index].append(aKey)

        if clusters != previousClusters:
            previousClusters = clusters
        else:
            continueOrNot = False


        dimensions = len(dataDict[1])

        for clusterIndex in range(k): # sum all the clusters in each index
            sums = [0] * dimensions
            for cluster in clusters[clusterIndex]:
                dataPoint = dataDict[cluster]
                for ind in range(len(dataPoint)):
                    sums[ind] += dataPoint[ind]

            for ind in range(len(sums)): # get the average from the sum
                clusterLen = len(clusters[clusterIndex])
                if clusterLen != 0:
                    sums[ind] = sums[ind] / clusterLen

            centroids[clusterIndex] = sums

        '''
        for c in clusters:
            print('CLUSTER')
            for key in c:
                print(dataDict[key], end = ' ')
            print()
        '''

        aPass += 1

    return clusters


def eqDraw(k, eqDict, eqDictMag, eqClusters):
    '''(k: int, eqDict: dict, eqDictMag: dict, eqClusters: list) -> None

    this function will plot the dots with a defferent colors
    for each clusters on the world map using the latitude and
    longitude numbers
    '''

    speed('fastest')
    bgpic('world_map_1800_900.gif')
    screensize(1800, 900)

    wFact = (screensize()[0]/2) / 180
    hFact = (screensize()[1]/2) / 90

    hideturtle()
    penup()

    colorlist = ['red', 'green', 'blue', 'orange', 'yellow', 'purple']

    for clusterIndex in range(k):
        color(colorlist[clusterIndex])
        for aKey in eqClusters[clusterIndex]:
            long = eqDict[aKey][0]
            lat = eqDict[aKey][1]
            goto(long * wFact, lat * hFact)
            if eqDictMag[aKey] > 7.5: # change the size of the dot depending on the magnitude size
                size = 35
            elif eqDictMag[aKey] > 6:
                size = 15
            elif eqDictMag[aKey] > 4:
                size = 8
            elif eqDictMag[aKey] > 2:
                size = 5
            elif eqDictMag[aKey] > 0:
                size = 3

            dot(size)
            
            
    #exitonclick()
    return

def visualizeQuakes(dataFile):
    '''(dataFile: str) -> None
    
    This function will assign variable for each function
    readFile, createCentroids, createClusters and call
    eqDraw using those variables from each function
    '''
    k = 6
    dataDict = readFile(dataFile)[0]
    centroids = createCentroids(k, dataDict)
    clusters = createClusters(k, centroids, dataDict, 7)
    dataDictMag = readFile(dataFile)[1]
    tracer(0, 0) 
    eqDraw(k, dataDict, dataDictMag, clusters)
    update() # updeate when all the plotting is done
    return

def main():
    '''
    call visualizeQuakes to visualize all the eqrthquake locations
    with magnitude
    '''
    dataFile = 'world_equakes.csv'
    visualizeQuakes(dataFile)
    
main()
print(doctest.testmod())
    
#createClusters(5, createCentroids(5, readFile('earthquake.csv')), readFile('earthquake.csv'), 3)

                
                
                
                
            

        
        






















        
