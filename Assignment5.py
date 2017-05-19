import sys
import time
import math
import random
import copy
linelength = 0

#Peter McPadden
#AI Assignment 5

#things we need: DFS to check for connected components, wrap this with a checkvalid function
#a swapedge method that finds all edges for each district, picks a random one or more district edges and swaps em
#inside swapedge we need edge detector: criteria: start with things that have only one neighbor, then with 2, then with 3, if something has 4 in dist neighbors it cant be an edge,
#2 in dist neighbors is probably an edge, but if theres a line of 3, then it won't be
#all of these need to be wrapped in a generate new, which will call swapedge, then call isvalid, and if valid then we're done, else we need to fix. have it return which districts
#are invalid. either use the last valid graph and remake, or do the hard work of fixing it.
#valid dist sizes should be +- 1 from the evenly divided size
#worth doing - if first new graph is valid, try another switch, if not stop, if we run into subsequent illegal graph we switch it off


#construct graph: takes in text file, gets row length and column length, uses each config as I want it to for the nodes.
#things are neighbors with everything at +1x and +1y unless at len or height limit.
#make sure to include back edges. it may be worth just putting coords inside the edges, not the nodes themselves. who knows on that. its probably faster

#after that we end up with our SA function - this is the easy part, will require tuning probably.

class Stack:
    def __init__(self):
        self.data = []

    def push(self, integer):
        self.data.append(integer)

    def checkSize(self):
        return len(self.data)

    def pop(self):
        if (len(self.data) == 0):
            return "Stack empty."
        else:
            return self.data.pop()

#if need queue use a deque: from collections import deque?


class Node:
    # your code goes here
    def __init__(self, dist, x, y, party):
        self.dist = dist
        self.xcoord = x
        self.ycoord = y
        self.party = party
        self.visited = False

    def getcoords(self):
        return [self.xcoord, self.ycoord]




class Graph:
    def __init__(self):
        # graph will be of form {(vertex name, solved, dist, heuristic, f): [(edge, length), (edge, length)]
        # kinda complex and i should've used nodes but I was running out of time and didnt switch
        # this SHOULD be designed so that heuristic doesnt get messed with in dijkstra and solved doesnt as well.
        self.vertices = {}

    # gets me the whole tuple given the vertex value
    def getnodebycoords(self, x, y):
        for node in self.vertices:
            if ((node.xcoord == x) and (node.ycoord == y)):
                return node

        else:
            print "FindVertexFail"
            #do stuff

    def addVertex(self, x, y, party, dist):
        # check if value already exists
        nexists = False
        for node in self.vertices:
            #if node already exists
            if node.party == party and node.xcoord == x and node.ycoord == y and node.dist == dist:
                nexists = True
        #if our node exists we dont want to re-add it. in theory this should never happen and im wasting cycles
        if nexists == True:
            print "node already exists"
        else:
            mynode = Node(dist, x, y, party)
            self.vertices[mynode] = []


    def addEdge(self, x1, y1, x2, y2):
        for node in self.vertices:
            if (node.xcoord == x1 and node.ycoord == y1):
                for node2 in self.vertices:
                    if (node2.xcoord == x2 and node2.ycoord == y2):
                        # addedge
                        thing = self.vertices[node]
                        thing.append(node2)
                        # print "Edge from", value1, "to", value2, "added."
                        thing = self.vertices[node2]
                        thing.append(node)
                    # print "Edge from", value2, "to", value1, "added."
                    else:
                        pass

    def getadjacent(self, node):
        return self.vertices[node]

    def getadjacentindist(self, node):
        noderet = []
        for node2 in self.vertices[node]:
            if node2.dist == node.dist:
                noderet.append(node2)
        return noderet

    def getdist(self, dist):
        noderet = []
        for node in self.vertices:
            if node.dist == dist:
                noderet.append(node)
        return noderet

    def getdistsize(self, dist):
        return len(self.getdist(dist))

    def isboundary(self, node):
        bound = False
        for mynode in self.getadjacent(node):
            if mynode.dist != node.dist:
                bound = True
        return bound

    def getadjdist(self, node):
        for node2 in self.getadjacent(node):
            if node2.dist != node.dist:
                return node2.dist

    def printgraph(self):
        for node in self.vertices:
            print node.xcoord, node.ycoord, node.dist, node.party


#DFS(vertex)
 #   vertex.visited = true
  #  for each v in vertex.adjacent
   #      if(!v.visited)
    #         v.parent = vertex
     #        print(v.key)
      #       DFS(v)

def dfs(graph, node, visitedarr):
    node.visited = True
    visitedarr.append(node)
    for node2 in graph.getadjacentindist(node):
        if node2.visited == False:
            dfs(graph, node2, visitedarr)

def dfsinit(graph, x, y):
    visitedarr = []
    #reset visited, we can search multiple times
    for node in graph.vertices:
        node.visited = False
    node = graph.getnodebycoords(x, y)
    dfs(graph, node, visitedarr)
    return visitedarr

def pickanodefromdist(g, dist):
    nodes = g.getdist(dist)
    return nodes[random.randint(0,linelength-2)]

def pickaboundfromdist(g, dist):
    edge = False
    while edge == False:
        node = pickanodefromdist(g, dist)
        if g.isboundary(node):
            edge = True
    return node

def isvalidgraph(g):
    global linelength
    dist = 1
    valid = True
    while dist <= linelength:
        node = pickanodefromdist(g, dist)
        visited = dfsinit(g, node.xcoord, node.ycoord)
        if g.getdistsize(dist) != len(visited) or g.getdistsize(dist) != linelength:
            valid = False
            break
        else:
            dist = dist +1
    return valid

#ALWAYS CALL THIS WITH DIST == 1
def swapdist(g, dist):
    #start with a dist
    boundary = pickaboundfromdist(g, dist)
    #print "something"
    #get an edge node from dist
    #switch that node to another district
    newdist = g.getadjdist(boundary)
    #print "newdist is", newdist
    boundary.dist = newdist
    #do the same thing with next dist  and so on until we swap to original dist
    #basically if we set dist 1 as our first one, and switch a node to dist 2, then dist 2 has 11 (assuming size 10), 1 has 9, and will have 9 for a while
    #2 swaps with 3, now 2 is down to 10, 3 up to 11. 3 can swap back with 2 back and forth all it wants, but 1 is the first dist and still has 9
    #once something that will have 11 swaps with 1, we end up with valid districts everything happily has 10 again

    #we call top level with dist = 1, then we recurse with new dists. once we get back to
    if newdist == 1:
        return
    else:
        swapdist(g, newdist)


def score(g):
    global linelength
    rs = 0
    count = 0
    #count total pop and pop R's
    for nodes in g.vertices:
        if nodes.party == "R":
            rs = rs +1
        count = count + 1
        #get proportion
    proportionrs = float(float(rs)/float(count))
    #proportionds = 1-proportionrs
    dist = 1
    rcount = 0
    dcount = 0
    #loop through districts, count number of rs and ds per dist
    while dist <= linelength:
        rs = 0
        ds = 0
        for nodes in g.vertices:
            if nodes.dist == dist:
                if nodes.party == "R":
                    rs = rs + 1
                else:
                    ds = ds + 1
        #if rs outnumber ds or vice versa increment count of r dists and d dists, ignore if tied
        if ds > rs:
            dcount = dcount + 1
        elif rs > ds:
            rcount = rcount + 1
        else:
            pass
        dist = dist + 1
        #get proportion of r dists to total dists
    proprdist = float(float(rcount)/float(linelength))
    #we want our score to increase if our numbers are close to representative so we divide by difference in proportions. if really close number will be huge, if different could be as low as -50
    if (proportionrs - proprdist) == 0:
        score = float('inf')
    else:
        score = math.fabs(1/(proportionrs - proprdist))
    #return all of this together so we dont duplicate work
    return [score, proportionrs, rcount, dcount]

    #SimulatedAnnealing:
    #    s = s0 //generate an initial solution
    #    T = Tmax //set the initial temperature
    #    Tmin = .00001 //minimum temp for the algorithm, tunable parameter
    #    alpha = 0.9   //temperature adjustment, tunable parameter
    #     while T > Tmin:
    #        while !equilibrium:
    #           s' = random neighbor of s
    #           dE = f(s') - f(s)  //evaluate the fitness of state s and s'
    #           if dE < 0:  //assumes we want to minimize fitness, would be dE > 0 if we were maximizing fitness
    #               s = s'  //accept neighbor solution
    #           else
    #            //accept s' with probability e(-dE/kT)
    #        T = T * alpha
     #   return s

def simanneal(g):
    count = 0
    s = g #starting soln is g, its passed in
    T = 10000
    Tmin = .00001
    alpha = 0.95
    k = 1000
    while T > Tmin:
        #make a copy of s to hang on to
        f = copy.deepcopy(s)
        valid = False
        #now successively copy f, and do swaps. if we end up with an invalid soln, we just recopy f
        while valid == False:
            sprime = copy.deepcopy(f)
            swapdist(sprime, 1)
            if isvalidgraph(sprime):
                valid = True
        #now we need to score
        de = score(sprime)[0] - score(s)[0]
        if de > 0:
            s = sprime
            count = count + 1
        else:
            p = math.pow(math.e, (de/(k*T)))
            if p > random.random():
                s = sprime
            count = count + 1
        T = T * alpha
    #make deepcopy and call swapdist on that in here
    #and check validity, if it fails, try again until we get a valid graph. it sometimes fails, but more often than not works out alright
    #follow her psuedocode, print results
    finalscore = score(s)
    return [s, count, finalscore[0], finalscore[1], finalscore[2], finalscore[3]]


def constructgraph(filename):
    #flow will be take in file, get line length, initialize x and y vars. use nested while loop to access each node
    #each node will have its party and nodes associated. dunno how we'll assign districts filename will be an argv
    g = Graph()
    a = open(filename, 'r')
    y = 1
    for line in a:
        global linelength
        linelength = int(math.ceil(float(len(line))/2))
        x = 1
        for character in line:
            if character == "R" or character == "D":
            #if x<=4 then our dist is odd numbered
                if x<=(linelength/2):
                    if y%2 == 0:
                        dist = y-1
                    else:
                        dist = y
                else:
                    if y%2 == 0:
                        dist = y
                    else:
                        dist = y+1
            #mynode = Node(dist, x, y, character)
                g.addVertex(x, y, character, dist)
                x = x + 1
                #g.printgraph()
        y = y+1
    for node in g.vertices:
    #if x coord is at max length, we cant add an edge to a nonexistent node
        if node.xcoord==linelength:
        #this line takes care of bottom right corner
            if node.ycoord==linelength:
                pass
        #this takes care of right edge of graph
            else:
                g.addEdge(node.xcoord, node.ycoord, node.xcoord, (node.ycoord+1))
                g.addEdge(node.xcoord, node.ycoord, (node.xcoord-1), (node.ycoord + 1))
        elif node.ycoord == linelength:
        #again takes care of bottom right
            if node.xcoord == linelength:
                pass
            #takes care of bottom row
            else:
                g.addEdge(node.xcoord, node.ycoord, (node.xcoord+1), node.ycoord)
                #anything else we just go with the standard bottom and down
        elif node.xcoord == 1:
            if node.ycoord == linelength:
                #ignore, we've already dealt with bottom row, no need to do anything new here
                pass
            else:
                g.addEdge(node.xcoord, node.ycoord, (node.xcoord + 1), node.ycoord) #right
                g.addEdge(node.xcoord, node.ycoord, node.xcoord, (node.ycoord + 1)) #down
                g.addEdge(node.xcoord, node.ycoord, (node.xcoord + 1), (node.ycoord + 1)) #diag down right

        else:
            g.addEdge(node.xcoord, node.ycoord, (node.xcoord+1), node.ycoord)
            g.addEdge(node.xcoord, node.ycoord, node.xcoord, (node.ycoord+1))
            g.addEdge(node.xcoord, node.ycoord, (node.xcoord + 1), (node.ycoord +1))
            g.addEdge(node.xcoord, node.ycoord, (node.xcoord-1), (node.ycoord + 1))
#need to do separate for y coord with valid x coord
#and otherwise we add edge to x+1 and y+1
    return g

def output(thing):
    global linelength
    graph = thing[0]
    proprspop = thing[3]
    rcount = thing[4]
    dcount = thing[5]
    iterations = thing[1]
    rpercent = int(proprspop*100)
    dpercent = 100 - rpercent

    print"Party division in population: "
    print"**************************************"
    print"R:", rpercent, "%"
    print"D:", dpercent, "%"
    print"**************************************"
    print"Number of districts with a majority for each party: "
    print"**************************************"
    print"R:", rcount
    print"D:", dcount
    print"**************************************"
    print"Locations assigned to each district:"
    print"**************************************"
    dist = 1
    while dist <= linelength:
        nodes = []
        for node in graph.getdist(dist):
            nodes.append((node.xcoord, node.ycoord))
        mystring = "District"+ str(dist)+ ":"+ str(nodes)
        mystring = mystring.replace("]", "")
        mystring = mystring.replace("[", "")
        print mystring

        dist = dist + 1
    print"**************************************"
    print"**************************************"
    print"Algorithm Applied: Simulated Annealing"
    print"**************************************"
    print"**************************************"
    print "Number of search states explored:", iterations
    print"**************************************"
    return

        #print int(math.ceil(float(len(line))/2)) #this prints length of line

g = constructgraph(sys.argv[1])
thing = simanneal(g)
output(thing)
#node = g.getnodebycoords(2, 2)

#adj = g.getadjacent(node)
#for item in adj:
 #   print item.xcoord, item.ycoord, item.dist, item.party, item.visited
#size = g.getdistsize(1)
#print size

#print g.isboundary(node)
#visitedarr = dfsinit(g, 1, 1)

#node = g.getnodebycoords(5,3)
#node.dist = 1
#print len(visitedarr)
#print g.getdistsize(1)
#print isvalidgraph(g)
#f = copy.deepcopy(g)
#print type(f)
#swapdist(f, 1)
#print type(f)
#print type(g)
#print isvalidgraph(f)

#constructgraph("smallState.txt")

