import sys
from sys import argv
from heapq import heappush, heappop


def UCS(graph, s, goal, heuristic):
    # define dummy variables for use
    nodesQ = []
    visited_nodes = {}
    prev_nodes = {}

    # using heap for mainitng a queue
    heappush(nodesQ, (0, s, None, 0))
    for nodes in graph:
        visited_nodes[nodes] = False
        prev_nodes[nodes] = None
    # print("\nNODES: ",nodes)
    i = 1
    count = 0
    temp = 0
    c_node_h_val = 0
    d_track = 0
    # mark all visited and previous nodes False and None
    while len(nodesQ) != 0:
        # print("NODESQ: ",nodesQ)
        # pop the least cost node from heap and analyse it
        # print ("\nFringe at Loop#: ",i)
        # print (nodesQ)
        i = i + 1
        l2 = []
        for i in nodesQ:
            l2.append(i[0])
            l2.sort()
            l4 = []
        for i in l2:
            for j in nodesQ:
                if (i == j[0]):
                    l4.append(j)
        nodesQ = l4

        d_track = d_track + 1
        # print("\n fringe:",d_track,"\n nodesq: ",nodesQ)
        count = count + 1
        total_cost, current_node, prev_node, link_cost = heappop(nodesQ)
        if visited_nodes[current_node] == False:
            visited_nodes[current_node] = True
            prev_nodes[current_node] = []
            # print("prev _node",prev_node)
            # print("\n prev",link_cost)
            # print("\n current",current_node)
            prev_nodes[current_node].append(prev_node)
            prev_nodes[current_node].append(link_cost)
            # if heuristic != "":
            # 	for rec in heuristic:
            # 		if(rec[0].find(current_node)!=-1):
            # 			temp=rec[1]
            # 			print(temp)
            # 			break

            # if goal return the total route
            if current_node == goal:
                final = []
                while current_node != s:
                    temp = []
                    temp.append(current_node)
                    for i in prev_nodes[current_node]:
                        temp.append(i)
                    final.append(temp)
                    current_node = prev_nodes[current_node][0]
                final.reverse()
                d_track = d_track + 1
                # retrn total cost and final path
                return total_cost, count, final
            # else explore neighbours
            for neighbors, ncost in graph[current_node].items():
                # if visited_nodes[neighbors] == False:
                if heuristic != "":
                    for rec in heuristic:
                        if ((rec[0].find(current_node) != -1) & (d_track > 1)):
                            # print("current: ABC ",rec,"",d_track)
                            c_node_h_val = rec[1]
                        if (rec[0].find(neighbors) != -1):
                            temp = rec[1]
                        # print("rec check: ",rec)
                    #	break
                # print(neighbors)
                this_link_cost = ncost
                new_cost = total_cost + ncost + int(temp) - int(c_node_h_val)
                # print("****$%",new_cost+int(temp))
                heappush(nodesQ, (new_cost, neighbors, current_node, ncost))
            # d_track=d_track+1
    # return none if no path found

    return count
    pass


def main():
    # checking arguments for processing
    flag = False
    filedata1 = ""
    try:
        filename = sys.argv[1]
        Source = sys.argv[2]
        Destination = sys.argv[3]
    except IndexError:
        print ('\n***Insufficient argument***\n')
        return
    # open file and make data ready for analysis
    try:
        hueristicfile = sys.argv[4]
        flag = True
        file = open(hueristicfile, 'r')
        filedata1 = file.readlines()
        # print("ff",filedata1)
        # make a dictionary of graph
        filedata1 = [x.strip().split() for x in filedata1]
        # print("ff",filedata1)
        if filedata1[-1:][0][0] == 'END':
            filedata1.pop()
    # print(filedata1, "filesdatat1")

    except IndexError:
        pass

    file = open(filename, 'r')
    filedata = file.readlines()
    # print("mm",filedata)
    # make a dictionary of graph
    filedata = [x.strip().split() for x in filedata]
    #print("ff",filedata)
    if filedata[-1:][0][0] == 'END':
        filedata.pop()

    # empty graph
    G = {}
    for rec in filedata:
        src = rec[0]
        dest = rec[1]
        cst = rec[2]
        if src not in G:
            G[src] = {}
        if dest not in G:
            G[dest] = {}
        # create src and dest nodes with its length from input file
        #G[src][dest] = int(cst)
        #G[dest][src] = int(cst)
        G[src][dest] = int(cst)
        G[dest][src] = int(cst)

    # call the UCS function
    result = UCS(G, Source, Destination, filedata1)

    if isinstance(result, int):
        print ("\nnodes expanded:", result, "\ndistance: infinity\nroute:\nnone\n")
    else:
        print ("\nnodes expanded:", result[1], "\ndistance:", result[0], "km\nroute:")
        for line in result[2]:
            print ("%s to %s, %s km" % (line[1], line[0], line[2]))
        print ("")

    pass


main()
