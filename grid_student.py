import sys              # used for file reading
from settings import *  # use a separate file for all the constant settings

import math
import numpy

# the class we will use to store the map, and make calls to path finding
class Grid:
    # set up all the default values for the frid and read in the map from a given file
    def __init__(self, filename):
        # 2D list that will hold all of the grid tile information
        self.__grid = []
        self.__load_data(filename)
        self.__width, self.__height = len(self.__grid), len(self.__grid[0])
        self.__conn = [[[0 for j in range(self.__height)] for i in range(self.__width)] for k in range(MAX_SIZE+1)]
        self._legal_m = [[[0 for j in range(self.__height)] for i in range(self.__width)] for k in range(MAX_SIZE+1)]


        self.connectiveSector()
        for i in range(1, len(self._legal_m)):
            for j in range(len(self._legal_m[i])):
                 for k in range(len(self._legal_m[i][j])):
                      self.legal_movement((j,k),i)
        # list =[n,n1,n2]
        # node = self.remove_min_from(list)
        # print("fshkdafhs", node.state)
        # for i in list:
        #     print (i.state)
        # print(self.AStar_Search((13,25),(4,40),1))

        # for i in self.expand((Node((4,40)))):
        #     print(i.state)
        # for i in range(len(self.__conn)):
        #     for j in range(len(self.__conn[i])):
        #         for k in range(len(self.__conn[i][j])):
        #             print(self.__conn[i][j][k], end=" " )
        #         print()
        #     print()

    # loads the grid data from a given file name
    def __load_data(self, filename):
        # turn each line in the map file into a list of integers
        temp_grid = [list(map(int,line.strip())) for line in open(filename, 'r')]
        # transpose the input since we read it in as (y, x)
        self.__grid = [list(i) for i in zip(*temp_grid)]


    # return the cost of a given action
    # note: this only works for actions in our LEGAL_ACTIONS defined set (8 directions)
    def __get_action_cost(self, action):
        return CARDINAL_COST if (action[0] == 0 or action[1] == 0) else DIAGONAL_COST

    # returns the tile type of a given position
    def get(self, tile): return self.__grid[tile[0]][tile[1]]
    def width(self):     return self.__width
    def height(self):    return self.__height

    # check if two tile are same
    def same_tile(self, s, f): return self.get(s) == self.get(f)
    #return the sector integers of a give positon
    def get_sector(self,pos,size): return self.__conn[size][pos[0]][pos[1]]
    #assign a sector integers to a give positon
    def set_sector(self, pos,size,numSect): self.__conn[size][pos[0]][pos[1]] = numSect


    def legal_movement(self,start,size):
        LEGAL_ACT = [(0, -1), (0,  1), (-1,  0),(1,  0),
                    (-1,  1), (1,  1),(-1, -1), (1, -1)]

        m = [(0, -1),(-1,  0),(1,  0),(0,  1)]
        dcheck = False
        self._legal_m[size][start[0]][start[1]]= set()
        for action in LEGAL_ACT:
            next_move = (start[0]+ action[0], start[1]+action[1])
            if next_move[0] >= 0 and next_move[1] >= 0 and next_move[0]< self.width() and next_move[1]< self.height():
                if self.same_tile(next_move, start):
                    # up right diagonal
                        if action[0] == -1 and action[1] == -1:
                            #walkable when up and left are available
                            if m[0] in self._legal_m[size][start[0]][start[1]] and m[1] in self._legal_m[size][start[0]][start[1]]:
                                self._legal_m[size][start[0]][start[1]].add(action)
                    # up left diagonal
                        elif action[0] == 1 and action[1] == -1:
                            #walkable when up and right are available
                            if m[0] in self._legal_m[size][start[0]][start[1]] and m[2] in self._legal_m[size][start[0]][start[1]]:
                                self._legal_m[size][start[0]][start[1]].add(action)
                    #  down right diagonal
                        elif action[0] == -1 and action[1] == 1:
                           #walkable when left and down are available
                            if m[1] in self._legal_m[size][start[0]][start[1]] and m[3] in self._legal_m[size][start[0]][start[1]]:
                                self._legal_m[size][start[0]][start[1]].add(action)
                    # down left diagonal
                        elif action[0] == 1 and action[1] == 1:
                            # walkable when down and right are available
                            if m[2] in self._legal_m[size][start[0]][start[1]] and m[3] in self._legal_m[size][start[0]][start[1]]:
                                self._legal_m[size][start[0]][start[1]].add(action)
                        else:
                            self._legal_m[size][start[0]][start[1]].add(action)


    # check all other tile for current tile surface when size >2
    def corner_match(self, start,size):
        for i in range(size):
            for j in range(size):
                tile = (start[0]+i, start[1]+j)
                if tile[0] < self.__width and tile[1] < self.__height:
                    if self.same_tile(start,tile) == False:
                        # print("false tile: ",tile)
                        return False
                else: return False

        return True

    def corner_path_match(self, start, size):
        for i in range(size):
            for j in range(size):
                tile = (start[0]+i, start[1]+j)
                if tile[0] < self.__width and tile[1] < self.__height:
                    if self.same_tile(start,tile) == False:
                        # print("false tile: ",tile)
                        return False
                else: return False

        return True

    # breath first search to flood fill the connective area among all tile
    def bfs(self,start,size,numSect):
        movement = [(0, -1),(-1,  0),(1,  0),(0,  1)] # 4 directional movement
        visited = set()
        q = []
        q.append(start)
        while q:
            current = q.pop(0)
            # when tile size is bigger than 1, do additional check for the tile surface
            if size > 1:
                if self.corner_match(current, size):
                    self.set_sector(current,size,numSect)
                else: continue
            # check if is visited
            if current not in visited:
                visited.add(current)
                for move in movement:
                    next_move = (current[0]+move[0],current[1]+move[1])
                    if next_move[0] >= 0 and next_move[1] >= 0 and next_move[0]< self.width() and next_move[1]< self.height():
                        print("movement:",next_move)
                        if size > 1:
                            # make sure all tile are same before append the move to queue
                            if self.same_tile(next_move,current):
                                if self.corner_path_match(next_move,size):
                                    if self.get_sector(next_move,size)== 0:
                                        q.append(next_move)
                                        self.set_sector(next_move,size,numSect)
                        else:
                            # size 1 action
                            if self.same_tile(next_move,current):
                                if self.get_sector(next_move,size)== 0:
                                    #print("valid move", next_move)
                                    q.append(next_move)
                                    self.set_sector(next_move,size,numSect)


    # flood fill the entire map and assign sector with different integers
    def connectiveSector(self):
        numSect = 1
        for s in range(1,len(self.__conn)):
            for j in range(len(self.__conn[s])):
                for k in range(len(self.__conn[s][j])):
                    if self.get_sector((j,k),s)!= 0: continue
                    self.bfs((j,k),s,numSect)
                    numSect = numSect + 1
            numSect=1
        # Student TODO: Implement this function
        # returns true of an object of a given size can navigate from start to goal
    def is_connected(self, start, goal, size):
        if (size > 1):
            # start and goal must be same type
            if not self.same_tile(start,goal): return False
            # if start sector is 0, mean is not walkable
            if self.get_sector(start,size) == 0: return False
            # make sure start and goal have the same sector
            if self.get_sector(start,size) == self.get_sector(goal,size):return True
            else: return False
        else:
            # start and goal must be same type
            if not self.same_tile(start,goal): return False
            # if start sector is 0, mean is not walkable
            if self.get_sector(start,size) == 0: return False
            # make sure start and goal have the same sector
            if self.get_sector(start,size) == self.get_sector(goal,size):return True
            else: return False

    def remove_min_from(self, openlist):
    	minNode = openlist[0]
    	check = minNode.state
    	index=0
    	for i in range(1,len(openlist)):
    		if not minNode.__lt__(openlist[i]):
    			 index = i
    	return openlist.pop(index)

    def reconstruct_path(self, node):
        path = []
        while node.parent != None:
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path

    def expand(self, node,size):
        q=[]
        state = node.state
        for action in self._legal_m[size][state[0]][state[1]]:
            child = (state[0]+action[0], state[1]+action[1])
            if (child[0] >= 0) and (child[1]>=0) and (child[0] < self.width()) and (child[1]<self.height()):
                if (size > 1):
                    if self.is_connected(state, child, size) == True:
                        if self.corner_path_match(child, size) == True:
                            n = Node(child)
                            print(child)
                            n.action = action
                            n.parent = node
                            n.g = node.g + self.__get_action_cost(action)
                            q.append(n) 
                        else: continue
                else:
                    if self.is_connected(state, child, size) ==True:
                        n = Node(child)
                        n.action = action
                        n.parent = node
                        n.g = node.g + self.__get_action_cost(action)
                        #print(self.__get_action_cost(action))
                        q.append(n)  # it should append n not next
                    else: continue
            else: continue
        return q


    def AStar_Search(self, start, goal, size):
        closed = set()
        openlist = [Node(start)]
        while (len(openlist) > 0):
           # print("size:",len(openlist), len(closed))
            node = self.remove_min_from(openlist)
           # print("size2:",len(openlist), len(closed))
            if (node.state == goal):return self.reconstruct_path(node), closed
            if (node.state not in closed):
                closed.add(node.state)
               # print(closed);
                for child in self.expand(node,size):
                    if child.state in closed: continue
                    child.f = child.g + self.estimate_cost(start, goal)
                    openlist.append(child)
        return []#, set()

    def estimate_cost(self, start, goal):
        diag1 = abs(start[0] - goal[0])
        diag2 = abs(start[1] - goal[1])

        # Diagonal
        return (1 * (diag1 + diag2) + (math.sqrt(2) - 2 * 1) * min(diag1, diag2)) * 100
        #Euclidian Distance
        #return math.sqrt(diag1 * diag1 + diag2 * diag2)
        #return (math.sqrt((start[0]-start[1])**2 + (goal[0] - goal[1])**2))*10

    def get_path(self, start, end, size):
        path = []
        if self.is_connected(start,end,size) == False:
            return path, 0, set()
        else:
            path, closed = self.AStar_Search(start, end, size)
            return path, sum(map(self.__get_action_cost, path)), closed

#Optimizations later (LOL)
class AStar:

	def add_to_open(node):
		return []

	def remove_min_from_open():
		return []

	def is_in_open():
		return []

	def is_in_closed():
		return []


class Node:
    def __init__(self, tile):
        self.state = tile
        self.action = (0, 0)
        self.g = 0
        self.f = 0
        self.parent = None

    def __lt__(self,other):
        return self.f < other.f
