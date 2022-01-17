#Alexander Gonzalez

import sys
import math
import collections
import copy
from random import randint

class point:
    id = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

class cluster:
    points = []
    centroid = point
    def __init__(self, iD):
        self.id = iD

def main():
    if len(sys.argv) != 3:
        print("ERROR: Not the right number of arguments. Must be 2 arguments")

    data_points = []
    clusters = []
    k = int(sys.argv[1])

    if k <= 1:
        print("ERROR: K must be greater than 1")
        return 1
    try:
        file = open(sys.argv[2], 'r')
        for line in file:
            fields = line.strip().split()
            p = point(int(fields[0]), int(fields[1]))
            data_points.append(p)
        file.close()
    except IOError:
        print("ERROR: File does not exist")
        return 1

    xmin = 100000000
    xmax = 0
    ymin = 100000000
    ymax = 0
    for i in range(len(data_points)):
        if xmin > data_points[i].x:
            xmin = data_points[i].x
        if ymin > data_points[i].y:
            ymin = data_points[i].y
        if xmax < data_points[i].x:
            xmax = data_points[i].x
        if ymax < data_points[i].y:
            ymax = data_points[i].y 

    for i in range(k):
        if i > 0:   
            c = cluster(i+1)
            p = point(randint(xmin, xmax), randint(ymin,ymax))
            c.centroid = p
            clusters.append(c)
            clusters[i].points = copy.deepcopy(clusters[i-1].points)
        else:
            c = cluster(i+1)
            p = point(data_points[i].x, data_points[i].y)
            c.centroid = p
            clusters.append(c)

    changed = True
    loop = 0
    old_centroids = []
    while changed:
        loop += 1

        #clears all points in cluster, therefore no duplicates after each iteration
        if(loop > 1):
            for i in range(len(clusters)):
                clusters[i].points.clear()
        #clears the list that keeps track of centroids of clusters for comparison later
        old_centroids.clear()

        #creates an temporary list of points for old_centroids to be later changed
        for i in range(len(clusters)):
            p = point(0,0)
            old_centroids.append(point)

        #sets the old_clusters list to have each clusters centroid
        for i in range(len(clusters)):
            old_centroids[i].x = clusters[i].centroid.x
            old_centroids[i].y = clusters[i].centroid.y
        
        #i goes through each data point to determine which cluster it belongs to
        for i in range(len(data_points)):
            distances = []  #list that stores the distance from each clusters centroid
            dist = float("inf") #variable to store the minimum distance
            index = 0   #index of the cluster the point is closest to
            print("\nPoint:", data_points[i].x, " ", data_points[i].y)
            #n iterates through each cluster, then uses the euclidean distance to find the closest centroid
            for n in range(len(clusters)):
                print("Cluster Point", n + 1 ,":", clusters[n].centroid.x, " " ,clusters[n].centroid.y)
                distance = math.sqrt((abs(data_points[i].x - clusters[n].centroid.x) ** 2) + 
                (abs(data_points[i].y - clusters[n].centroid.y) ** 2))
                distances.append(distance)
                print("Distance from cluster", n + 1, ":", distance)
            for x in range(len(distances)):
                if dist > distances[x]:
                    dist = distances[x]
                    index = x
            print("Cluster", index + 1, "updated.")
            
            #adds the data point to the cluster it is closest to
            data_points[i].id = index + 1
            p = point(data_points[i].x, data_points[i].y)
            p.id = index + 1
            clusters[index].points.append(p) #duplicating to all clusters
        
        print("\n")
        #calculates the new cluster centroid
        for i in range(len(clusters)):
            total_x = 0
            total_y = 0
            for k in range(len(clusters[i].points)):
                total_x += clusters[i].points[k].x
                total_y += clusters[i].points[k].y
            print("Number of points in cluster", i+1 , ":", len(clusters[i].points))
            if(len(clusters[i].points) > 0):
                clusters[i].centroid.x = int(total_x / len(clusters[i].points))
                clusters[i].centroid.y = int(total_y / len(clusters[i].points))
            else:
                p = data_points[randint(0,(len(data_points)-1))]
                clusters[i].centroid = p

        print("New centroids:")
        for i in range(len(clusters)):
            print("Cluster", i+1, "centroid:", clusters[i].centroid.x, " " , clusters[i].centroid.y)

        #compares old and new centroids to see if the centroids have changed
        for i in range(len(clusters)):
            if clusters[i].centroid.x == old_centroids[i].x and clusters[i].centroid.y == old_centroids[i].y:
                changed = False

    output = open("output.txt", 'w') #file to output to

    #writes output to file
    for i in range(len(clusters)):
        for k in range(len(clusters[i].points)):
            output.write(str(clusters[i].points[k].x) + "\t" + str(clusters[i].points[k].y) + "\t" + str(clusters[i].points[k].id) + "\n")

    output.close()
            
    print("\nK-means algorithm complete. Please find output in the output.txt file.")

if __name__ == "__main__":
    main()
