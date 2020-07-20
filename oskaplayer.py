import copy
from statistics import mean 
from Node import node
#main function
def oskaplayer(board, player, moves_ahead):
    first_player = player
    moves = [] 
    moves.append(board)
    p =""
    
    while(game_over(moves[len(moves)-1]) == False):
        if(game_over(moves[len(moves)-1])):
            break
        move = minimax(moves[len(moves)-1],player, moves_ahead, first_player) #gets back best move using minimax algorithm
        moves.append(move)
        if(player == "w"): #switches player
            player = "b"
        else:
            player = 'w'

    for m in moves: #once game is over prints out all the moves used
        print_board(m)
        print()

    determine_winner(moves[len(moves) - 1]) #prints out who one based on ending move

def minimax(board,player,moves_ahead, first_player): #creates nodes for start board and return best next move
    m = 0

    curr_node =  node(board,[],[],[],"MAX",True,True,False, -1) #creates parent node
   

    first_move = True
    while((curr_node.parent != []) or (first_move == True) ): #in this loop it creates each nodes children until reached to given depth (moves_ahead)

        first_move = False
        if(curr_node.level == "MIN"): #assigns player depending on level
            if(player == 'w'):
                p = 'b'
            else:
                p = 'w'
        else:
            if(player == 'w'):
                p = 'w'
            else:
                p = 'b'
       
        if(curr_node.level == "MAX"): #assigns level depending on parent node's level
                l = "MIN"
        else:
                l = "MAX"
        new_states = movegen(curr_node.state,player) #gets the new moves from current given move

        while(len(new_states) > 0): #creates children nodes
            state = new_states.pop(0)
            new_node = node(state,curr_node,[],[],l, False, False,False,-1)
            curr_node.children.append(new_node)

        for c in range(len(curr_node.children)):
            if(c != len(curr_node.children)-1):
                curr_node.children[c].right = curr_node.children[c+1]
        curr_children = copy.copy(curr_node.children)

        #assigns next node
        if(m+1 >= moves_ahead): #if depth is reached
            for i in curr_node.children: #leaves are found 
                i.visited = True
                i.isleaf =  True
            if(curr_node.right != []): #goes to the node on the right if exists
                curr_node = curr_node.right
                if(curr_node.visited == True): #finds node that wasnt visited
                    found = False
                    while(curr_node.visited == True):
                        if(curr_node.visited == False and curr_node != []):
                            found = True
                            curr_node = curr_node.right
                            curr_node.visited = True
                            break
                    if(found == False): #if not found goes back to the parent
                        curr_node = curr_node.parent
                else:
                    curr_node.visited = True
            else:
                if(curr_node.parent.isfirst == False): #if we are back at the top get out of the loop
                    curr_node = curr_node.parent
                else:
                    curr_node = curr_node.parent
                    break
        else: #if depth hasnt reached
    
            if(len(curr_children) > 0): #get first child if exists
                curr_node = curr_children.pop(0)
                curr_node.visited = True
            else: #if not go right
                if(curr_node.right != []):
                    curr_node = curr_node.right
                    curr_node.visited = True
                else:
                    if(curr_node.isfirst == True):
                        break
                    if(curr_node.parent.isfirst == False):
                        curr_node = curr_node.parent
                    else:
                        curr_node = curr_node.parent
                        break

        m+=1           
    
    return(get_best_move(curr_node,player, first_player,moves_ahead)) 

    
def board_evaluation(board, player): #return the score of each board given
    
    #calculates pieces left for each player
    piecesLeft_w = pieces_left(board, 'w')
    piecesLeft_b = pieces_left(board, 'b')
    
    #calculates distance for each player's pieces to the oppisote side
    distance_w = distance(board,'w')
    distance_b = distance(board, 'b')
    
    if(len(distance_w)<=0):
        distance_w.append(0)

    if(len(distance_b)<=0):
        distance_b.append(0)

    return ((piecesLeft_w - piecesLeft_b) + ((mean(distance_w)) - (mean(distance_b))))

#move generator function
def movegen(board, player):
    states = []
    #checks which player is given and calls function appropriate
    for r in range(len(board)):
        row = list(board[r])
        for c in range(len(row)):
            if((row[c] == 'w') and (player == 'w')):
                states += move_down(board,r,c)

    for i in range(len(board)-1, 0, -1):
        row = list(board[i])
        for j in range(len(row)):
            if((row[j] == 'b') and (player == 'b')):
                states += move_up(board,i,j)

   
    return states
#checks if game is over and returns boolean
def game_over(board):
    #check if there are any pieces left for either players
    p1 = pieces_left(board, 'w')
    p2 = pieces_left(board, 'b')
    if((p1 == 0) or (p2 == 0)):
        return True
    
    #checks if all distances of remaining pieces for all players are 0
    d1 = distance(board, 'w')
    d2 = distance(board, 'b')
    d1_p = 0
    d2_p = 0
    for i in d1:
        if(i == 0):
            d1_p+=1
    
    for j in d2:
        if(j == 0):
            d2_p+=1

    if((p1 == d1_p) or (p2 == d2_p)):
        return True
   
    return False

def determine_winner(board): 
    p1 = pieces_left(board,'w')
    p2 = pieces_left(board,'b')
    if(p1 == 0):
        print("Black player won!")
        return
    
    if(p2 == 0):
        print("White player won!")
        return
    
    d1 = distance(board, 'w')
    d2 = distance(board, 'b')

    d1_p = 0
    d2_p = 0
    for i in d1:
        if(i == 0):
            d1_p+=1
    
    for j in d2:
        if(j == 0):
            d2_p+=1
    
    if((d1_p == p1) and (d2_p == p2)): #if both players are at opposite side then check who has more pieces
        if(p1 > p2):
            print("White player won!")
            return
        if(p2 > p1):
            print("Black player won!")
            return
        if(p1 == p2):
            print("Its a draw!")
            return
    else:
        if(d1_p == p1):
            print("White player won!")
            return
        else:
           print("Black player won!")
           return 


#gets move with best board evaluation
def get_best_move(parent_node,player, first_player, moves_ahead):
    curr_node = parent_node
    m = 0
    p = ""
    has_leaves = False

    #checks if leaves exists at depth given
    for i in parent_node.children:
        if(len(i.children) > 0):
            has_leaves = True
    if(len(parent_node.children)> 1):
        if(has_leaves):
            while(curr_node.isleaf == False): #gets the first leaf node

                if(len(curr_node.children)> 0):
                    curr_node = curr_node.children[0]
                else:
                    if(curr_node.right != []):
                        if(len(curr_node.right.children)> 0):
                            curr_node = curr_node.right.children[0]
                        else:
                            curr_node = curr_node.right
                            if(curr_node.right != []):
                                while(len(curr_node.right.children)<= 0 or curr_node.right!= []):
                                    curr_node = curr_node.right
                                if(curr_node.right != []):
                                    curr_node = curr_node.children[0]
                                else:
                                    break
                            else:
                                break
        else:
            curr_node = parent_node.children[0]

        end = False
        while((curr_node.parent.right != []) or (end == False)): #assigns scores to leaves

            if(curr_node.level == "MIN"):
                if(player == 'w'):
                    p = 'b'
                else:
                    p = 'w'
            else:
                if(player == 'w'):
                    p = 'w'
                else:
                    p = 'b'
            curr_node.score = board_evaluation(curr_node.state,p)
            
            if(curr_node.right != []):
                curr_node = curr_node.right
            else:
                curr_node = curr_node.parent
                if(curr_node.right != []):
                    if(len(curr_node.right.children) > 0):
                        curr_node = curr_node.right.children[0]
                    else:
                        curr_node = curr_node.right
                        while(len(curr_node.right.children) <= 0):
                            if(curr_node.right == []):
                                end = True
                                break
                            curr_node = curr_node.right
                        if(end):
                            break
                        else:
                            curr_node = curr_node.children[0]
                else:
                    break
        curr_node = parent_node.children[0]
     
        m+=1
        while(m+1 != moves_ahead and has_leaves == True): #gets first leaf again
            if(len(curr_node.children)>0):
                curr_node = curr_node.children[0]
            else:
                if(curr_node.right != []):
                    while(curr_node.right != [] and len(curr_node.right.children)== 0):
                        curr_node = curr_node.right
                    if(len(curr_node.children)>0):
                        curr_node = curr_node.children[0]
                    else:
                        break
            m+=1
        
        while(curr_node.isfirst == False): #propogates the scores up
            curr_node.score = calculate_best_move(curr_node)
            if(curr_node.right != []):
                curr_node = curr_node.right
            else:
                curr_node = curr_node.parent

        curr_node.score = calculate_best_move(curr_node)
        for c in curr_node.children: #finds first node with the highest score
            if(c.score == curr_node.score):
                return c.state
    else:
        if(len(parent_node.children) == 0):
            return parent_node.state
        else:
            return (parent_node.children[0].state)


def calculate_best_move(curr_node): 
    moves = {}
    if(len(curr_node.children)>0):
        for c in curr_node.children:
            moves[c.score] = c.state
    else:
        moves[curr_node.score] = curr_node.state 

    if(curr_node.level == "MIN"): #sorts by lowest and returns lowest
        sorted(moves.keys())
        return list(moves.keys())[0]
    else:#sorts by highest and returns it
        sorted(moves, key=moves.get, reverse=True) 
        return list(moves.keys())[0]


#Helper methods
#returns how many pieces for that particular player is left WORKS
def pieces_left(board, player):
    pieces = 0
    for r in board:
        col = list(r)
        for c in col:
            if(c == player):
                pieces+=1

    return pieces

#returns list of distances between each piece of a given player to the end of the board
def distance(board, player):
    distances = []
    d = 0
    for r in range(len(board)):
        col = list(board[r])
        for c in range(len(col)):

            if(col[c] == player):
                if(player == 'w'):
                    d = count_down(board,r)
                    distances.append(d)
                else:
                    d = count_up(board,r)
                    distances.append(d)
    return distances
def count_down(board, row): #counts down from pieces to len(board)-1
    r = row
    d = 0
    while(r < len(board)-1):
        d+=1
        r+=1

    return d

def count_up(board, row): #counts up from pieces to 0
    r = row
    d = 0
    while(r > 0):
        d+=1
        r-=1

    return d


def move_down(board,row,col): #moves b down and returns all states possible
    new_states = []
    new_state = copy.deepcopy(board)
    new_state1 = copy.deepcopy(board)
    if(row != len(board)-1):
        if(col == 0): #deals with pieces at column 0 
            str1 = list(new_state[row+1])
            if(str1[col] == "-"):
                str1[col] = "w"
                new_state[row+1] = "".join(str1)
                str1 = list(new_state[row])
                str1[col] = "-"
                new_state[row] = "".join(str1)
                new_states.append(new_state)
            else:
                if(str1[col] == "b"):#deals with jump if possible
                    if(len(new_state1[row])>= len(new_state1[row+1])):
                        if(row+2 < len(board)):
                            str1 = list(new_state[row+2])
                            if(str1[col] == "-"):
                                str1[col] = "w"
                                new_state[row+2] = "".join(str1)
                                str1 = list(new_state[row+1])
                                str1[col] = "-"
                                new_state[row+1] = "".join(str1)
                                str1 = list(new_state[row])
                                str1[col] = "-"
                                new_state[row] = "".join(str1)
                                new_states.append(new_state)
                            else:
                                if(str1[col+1]== "-"):
                                    str1[col+1] = "w"
                                    new_state[row+2] = "".join(str1)
                                    str1 = list(new_state[row+1])
                                    str1[col] = "-"
                                    new_state[row+1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[col] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
            str1 = list(new_state1[row+1])
            if(len(new_state1[row])< len(new_state1[row+1])):
                if(str1[col+1] == "-"):
                    str1[col+1] = "w"
                    new_state1[row+1] = "".join(str1)
                    str1 = list(new_state1[row])
                    str1[col] = "-"
                    new_state1[row] = "".join(str1)
                    new_states.append(new_state1)
                else:
                    if(str1[col+1] == "b"):
                        if(row+2 < len(board)):
                            str1 = list(new_state1[row+2])
                            if(str1[col+2] == "-"):
                                str1[col+2] = "w"
                                new_state1[row+2] = "".join(str1)
                                str1 = list(new_state1[row+1])
                                str1[col+1] = "-"
                                new_state1[row+1] = "".join(str1)
                                str1 = list(new_state1[row])
                                str1[col] = "-"
                                new_state1[row] = "".join(str1)
                                new_states.append(new_state1)
                            else:
                                if(str1[col+2] == '-'):
                                    str1[col+2] = "w"
                                    new_state1[row+2] = "".join(str1)
                                    str1 = list(new_state1[row+1])
                                    str1[col+1] = "-"
                                    new_state1[row+1] = "".join(str1)
                                    str1 = list(new_state1[row])
                                    str1[col] = "-"
                                    new_state1[row] = "".join(str1)
                                    new_states.append(new_state1)
        str1 = list(board[row])
        if(col == len(board[row])-1): #deals with pieces at end of row
            str1 = list(new_state[row+1])
            if(str1[len(str1)-1] == "-"):
                str1[len(str1)-1] = "w"
                new_state[row+1] = "".join(str1)
                str1 = list(new_state[row])
                str1[col] = "-"
                new_state[row] = "".join(str1)
                new_states.append(new_state)
            if(len(new_state[row])< len(new_state[row+1])):
                 if(str1[len(str1)-2] == "-"):
                    str1[len(str1)-2] = "w"
                    new_state[row+1] = "".join(str1)
                    str1 = list(new_state[row])
                    str1[col] = "-"
                    new_state[row] = "".join(str1)
                    new_states.append(new_state)
            else:
                str1 = list(new_state[row+1])
                if(str1[len(str1)-1] == "b"):
                    if(len(new_state[row+1])  == 2):
                        if(row+2 < len(board)):
                            str1 = list(new_state[row+2])
                            if(str1[len(str1)-2] == "-"):
                                    str1[len(str1)-2] = "w"
                                    new_state[row+2] = "".join(str1)
                                    str1 = list(new_state[row+1])
                                    str1[len(str1)-1] = "-"
                                    new_state[row+1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[len(str1)-1] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
                    else:
                         if(row+2 < len(board)):
                            str1 = list(new_state[row+2])
                            if(str1[len(str1)-1] == "-"):
                                    str1[len(str1)-1] = "w"
                                    new_state[row+2] = "".join(str1)
                                    str1 = list(new_state[row+1])
                                    str1[len(str1)-1] = "-"
                                    new_state[row+1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[len(str1)-1] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
        
            
        if(col != 0 and col != len(board[row]) -1): #deals with pieces in the middle
            str1 = list(new_state[row+1])
            if(str1[col] == "-"):
                str1[col] = "w"
                new_state[row+1] = "".join(str1)
                str1 = list(new_state[row])
                str1[col] = "-"
                new_state[row] = "".join(str1)
                new_states.append(new_state)
            else:
                if(str1[col] == "b"):
                    if(row+2 < len(board)):
                            str1 = list(new_state[row+2])
                            if(len(new_state[row]) < len(new_state[row+1])):
                                if(str1[col+1] == "-"):
                                    str1[col+1] = "w"
                                    new_state[row+2] = "".join(str1)
                                    str1 = list(new_state[row+1])
                                    str1[col] = "-"
                                    new_state[row+1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[col] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
                            else:
                                if(str1[col+1] == "-"):
                                    str1[col+1] = "w"
                                    new_state[row+2] = "".join(str1)
                                    str1 = list(new_state[row+1])
                                    str1[col] = "-"
                                    new_state[row+1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[col] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
            str1 = list(new_state1[row+1])
            if(col +1 < len(str1)):
                if(str1[col+1] == "-"):
                    str1[col+1] = "w"
                    new_state1[row+1] = "".join(str1)
                    str1 = list(new_state1[row])
                    str1[col] = "-"
                    new_state1[row] = "".join(str1)
                    new_states.append(new_state1)
                else:
                    if(str1[col+1] == "b"):
                        if(row+2 < len(board)):
                                str1 = list(new_state1[row+2])
                                if(str1[col-1] == "-"):
                                    str1[col-1] = "w"
                                    new_state1[row+2] = "".join(str1)
                                    str1 = list(new_state1[row+1])
                                    str1[col-1] = "-"
                                    new_state1[row+1] = "".join(str1)
                                    str1 = list(new_state1[row])
                                    str1[col] = "-"
                                    new_state1[row] = "".join(str1)
                                    new_states.append(new_state1)

    return new_states


def move_up(board,row,col): #moves b piece up and returns all possible states
    new_states = []
    new_state = copy.deepcopy(board)
    new_state1 = copy.deepcopy(board)
    if(row != 0):
        if(col == 0): 
            str1 = list(new_state[row-1])
            if(str1[col] == "-"):
                str1[col] = "b"
                new_state[row-1] = "".join(str1)
                str1 = list(new_state[row])
                str1[col] = "-"
                new_state[row] = "".join(str1)
                new_states.append(new_state)
            else:
                if(str1[col] == "w"):
                    if(len(new_state1[row])>= len(new_state1[row-1])):
                        if(row-2 >= 0):
                            str1 = list(new_state[row-2])
                            if(str1[col] == "-"):
                                str1[col] = "b"
                                new_state[row-2] = "".join(str1)
                                str1 = list(new_state[row-1])
                                str1[col] = "-"
                                new_state[row-1] = "".join(str1)
                                str1 = list(new_state[row])
                                str1[col] = "-"
                                new_state[row] = "".join(str1)
                                new_states.append(new_state)
                            else:
                                if(str1[col+1]== "-"):
                                    str1[col+1] = "b"
                                    new_state[row-2] = "".join(str1)
                                    str1 = list(new_state[row-1])
                                    str1[col] = "-"
                                    new_state[row-1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[col] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
            str1 = list(new_state1[row-1])
            if(len(new_state1[row])< len(new_state1[row-1])):
                if(str1[col+1] == "-"):
                    str1[col+1] = "b"
                    new_state1[row-1] = "".join(str1)
                    str1 = list(new_state1[row])
                    str1[col] = "-"
                    new_state1[row] = "".join(str1)
                    new_states.append(new_state1)
                else:
                    if(str1[col+1] == "w"):
                        if(row-2 >= 0):
                            str1 = list(new_state1[row-2])
                            if(str1[col+2] == "-"):
                                str1[col+2] = "b"
                                new_state1[row-2] = "".join(str1)
                                str1 = list(new_state1[row-1])
                                str1[col+1] = "-"
                                new_state1[row-1] = "".join(str1)
                                str1 = list(new_state1[row])
                                str1[col] = "-"
                                new_state1[row] = "".join(str1)
                                new_states.append(new_state1)
                            else:
                                if(str1[col+2] == '-'):
                                    str1[col+2] = "b"
                                    new_state1[row-2] = "".join(str1)
                                    str1 = list(new_state1[row-1])
                                    str1[col+1] = "-"
                                    new_state1[row-1] = "".join(str1)
                                    str1 = list(new_state1[row])
                                    str1[col] = "-"
                                    new_state1[row] = "".join(str1)
                                    new_states.append(new_state1)
        str1 = list(board[row])
        if(col == len(board[row])-1): 
            str1 = list(new_state[row-1])
            if(str1[len(str1)-1] == "-"):
                str1[len(str1)-1] = "b"
                new_state[row-1] = "".join(str1)
                str1 = list(new_state[row])
                str1[col] = "-"
                new_state[row] = "".join(str1)
                new_states.append(new_state)
            if(len(new_state[row])< len(new_state[row-1])):
                 if(str1[len(str1)-2] == "-"):
                    str1[len(str1)-2] = "b"
                    new_state[row-1] = "".join(str1)
                    str1 = list(new_state[row])
                    str1[col] = "-"
                    new_state[row] = "".join(str1)
                    new_states.append(new_state)
            else:
                str1 = list(new_state[row-1])
                if(str1[len(str1)-1] == "w"):
                    if(len(new_state[row-1])  == 2):
                        if(row-2 >= 0):
                            str1 = list(new_state[row-2])
                            if(str1[len(str1)-2] == "-"):
                                    str1[len(str1)-2] = "b"
                                    new_state[row-2] = "".join(str1)
                                    str1 = list(new_state[row-1])
                                    str1[len(str1)-1] = "-"
                                    new_state[row-1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[len(str1)-1] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
                    else:
                         if(row-2 >= 0):
                            str1 = list(new_state[row-2])
                            if(str1[len(str1)-1] == "-"):
                                    str1[len(str1)-1] = "b"
                                    new_state[row-2] = "".join(str1)
                                    str1 = list(new_state[row-1])
                                    str1[len(str1)-1] = "-"
                                    new_state[row-1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[len(str1)-1] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
        
            
            
        if(col != 0 and col != len(board[row]) -1):
            str1 = list(new_state[row-1])
            if(str1[col] == "-"):
                str1[col] = "b"
                new_state[row-1] = "".join(str1)
                str1 = list(new_state[row])
                str1[col] = "-"
                new_state[row] = "".join(str1)
                new_states.append(new_state)
            else:
                if(str1[col] == "w"):
                    if(row-2 >= 0):
                            str1 = list(new_state[row-2])
                            if(len(new_state[row]) < len(new_state[row-1])):
                                if(str1[col+1] == "-"):
                                    str1[col+1] = "b"
                                    new_state[row-2] = "".join(str1)
                                    str1 = list(new_state[row-1])
                                    str1[col] = "-"
                                    new_state[row-1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[col] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
                            else:
                                if(str1[col+1] == "-"):
                                    str1[col+1] = "b"
                                    new_state[row-2] = "".join(str1)
                                    str1 = list(new_state[row-1])
                                    str1[col] = "-"
                                    new_state[row-1] = "".join(str1)
                                    str1 = list(new_state[row])
                                    str1[col] = "-"
                                    new_state[row] = "".join(str1)
                                    new_states.append(new_state)
            str1 = list(new_state1[row-1])
            if(col +1 < len(str1)):
                if(str1[col+1] == "-"):
                    str1[col+1] = "b"
                    new_state1[row-1] = "".join(str1)
                    str1 = list(new_state1[row])
                    str1[col] = "-"
                    new_state1[row] = "".join(str1)
                    new_states.append(new_state1)
                else:
                    if(str1[col+1] == "w"):
                        if(row-2 >= 0):
                                str1 = list(new_state1[row-2])
                                if(str1[col-1] == "-"):
                                    str1[col-1] = "b"
                                    new_state1[row-2] = "".join(str1)
                                    str1 = list(new_state1[row-1])
                                    str1[col-1] = "-"
                                    new_state1[row-1] = "".join(str1)
                                    str1 = list(new_state1[row])
                                    str1[col] = "-"
                                    new_state1[row] = "".join(str1)
                                    new_states.append(new_state1)


    return new_states
def print_board(board): #prints board in a organized way
    first_row = list(board[0])
    length_of_first = len(first_row)

    for i in range(length_of_first):
        print(" ---", end='')
    
    print()
    for i in range(len(board)):
        row = list(board[i])
        if(i != 0):
            if(len(board[i]) == 2):
                j = 2
            else:
                j = 1
            spaces = len(board[0])- len(board[i]) + j
            for j in range(spaces):
                print(" ", end='')
        for r in range(len(row)):
            print("| ",end='')
            print(row[r], end='')
            print(" ", end='')
            if(r == len(row)-1):
                print("| ",end='')
        print()
        if(i != 0):
            if(len(board[i]) == 2):
                j = 2
            else:
                j = 1
            spaces = len(board[0])- len(board[i]) + j
            for j in range(spaces):
                print(" ", end='')
        for i in range(len(row)):
            print(" ---", end='')

        print()

