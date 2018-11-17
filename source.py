'''Every maze is zero-indexed in the API, current_location is [x, y]'''

import requests

def mazeConstructor(size):
'''Takes the size of a maze [width, height] and outputs a 2d array representing the maze,
    The maze is also surrounded by walls, making point (0, 0) in the original maze becomes (1, 1)
    where an 'x' represents an invalid or already visited location, and a '.' represents an unvisted point.
'''
    maze = []
    maze.append([])
    for i in range(size[0]+2):
        maze[0].append('x')
    for i in range(size[1]):
        maze.append(['x'])
        for j in range(size[0]):
            maze[i+1].append('.')
        maze[i+1].append('x')
    maze.append([])
    for i in range(size[0]+2):
        maze[size[1]+1].append('x')
    return maze


url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/'

getToken = 'session'
tokenReq = requests.post(url + getToken, data={'uid': '504907430'}) #Opens a new session
token = tokenReq.json()['token']


game = 'game?token=' + token

gameReq = requests.get(url+game)
levels = gameReq.json()['total_levels']
print("There are %i levels" %levels)

#The main game loop, will not stop until every level is finished
while levels:
    #print(gameReq.json()) For error checking, uncomment this line and any further commented out lines of code
    size = gameReq.json()['maze_size']
    #print(size)
    maze = mazeConstructor(size) #Build maze
    currLoc = gameReq.json()['current_location']
    currLoc[0]+=1
    currLoc[1]+=1
    moves = [] # Used as a stack to allow the code to backtrack as much as needed
    
    # This loop solves a specific maze
    while True:
        #print(currLoc)
        maze[currLoc[1]][currLoc[0]] = 'x' # Check off current location
        if maze[currLoc[1]-1][currLoc[0]] == '.': #Try to move up
            req = requests.post(url+game, data={'action': 'UP'})
            res = req.json()['result']
            if res == 'WALL':
                maze[currLoc[1]-1][currLoc[0]] = 'x'
            elif res == 'END':
                break
            elif res == 'SUCCESS':
                moves.append('UP')
                currLoc[1]-=1
                continue
        if maze[currLoc[1]][currLoc[0]+1] == '.': #Try to move right
            req = requests.post(url+game, data={'action': 'RIGHT'})
            res = req.json()['result']
            if res == 'WALL':
                maze[currLoc[1]][currLoc[0]+1] = 'x'
            elif res == 'END':
                break
            elif res == 'SUCCESS':
                moves.append('RIGHT')
                currLoc[0]+=1
                continue
        if maze[currLoc[1]+1][currLoc[0]] == '.': #Try to move down
            req = requests.post(url+game, data={'action': 'DOWN'})
            res = req.json()['result']
            if res == 'WALL':
                maze[currLoc[1]+1][currLoc[0]] = 'x'
            elif res == 'END':
                break
            elif res == 'SUCCESS':
                moves.append('DOWN')
                currLoc[1]+=1
                continue
        if maze[currLoc[1]][currLoc[0]-1] == '.': #Try to move left
            req = requests.post(url+game, data={'action': 'LEFT'})
            res = req.json()['result']
            if res == 'WALL':
                maze[currLoc[1]][currLoc[0]-1] = 'x'
            elif res == 'END':
                break
            elif res == 'SUCCESS':
                moves.append('LEFT')
                currLoc[0]-=1
                continue
        move = moves.pop() #Only reached if no movement possible, begins to backtrack until a possible move is found
        if move == 'UP':
            requests.post(url+game, data={'action': 'DOWN'})
            currLoc[1]+=1
        elif move == 'DOWN':
            requests.post(url+game, data={'action': 'UP'})
            currLoc[1]-=1
        elif move == 'LEFT':
            requests.post(url+game, data={'action': 'RIGHT'})
            currLoc[0]+=1
        elif move == 'RIGHT':
            requests.post(url+game, data={'action': 'LEFT'})
            currLoc[0]-=1
    
    levels -= 1 #Moves to next level
    print("Maze Solved")
    gameReq = requests.get(url+game)

#print(gameReq.json())
print("Mazes passed!!")

