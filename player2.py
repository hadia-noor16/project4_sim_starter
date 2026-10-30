from __future__ import annotations
from consts import Board, Color, Edge, NUM_NODES


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim
    """

    @staticmethod
    def get_move(board: Board) -> Edge:
        """
        Return a possible move for the second player (blue) that follows the optimal strategy laid out in the handout,
        given the input board state. If multiple moves are viable, this method can return any of them.
        """
        #raise NotImplementedError

        miniboard=Player2.get_miniboard(board)

        allowed_moves=Player2.get_allowed_moves(Color.P2,miniboard)

        #print("Allowed P2 moves:", allowed_moves)


        if len(allowed_moves)==1:
            return allowed_moves[0]

        # get maximal allowed moves for P2

        p2_sets=Player2.get_maximal_allowed_sets(Color.P2,miniboard)

        #print("P2 maximal sets:", p2_sets)

        counts={}   #dictionary to keep track of maximum moves count

        for move in allowed_moves:
            counts[move]=0           # keep every move count=0 in the beginning

            for allowed_set in p2_sets:
                if move in allowed_set:
                    counts[move]+=1

        max_p2_moves= max(counts.values())    # get the biggest count

        # get moves with that max count

        best_moves=[]

        for move in allowed_moves:
            if counts[move]==max_p2_moves:
                best_moves.append(move)

        if len(best_moves)==1:   # if there is only one best move, return that
           # print("ACTUAL P2 move:", best_moves[0])
            return best_moves[0]

        #Otherwise use P1 maximal allowed moves to compare and break the tie

        p1_sets=Player2.get_maximal_allowed_sets(Color.P1,miniboard)

        p1_allowed_sets={}

        for move in best_moves:
            p1_allowed_sets[move]=0

            for allowed_set in p1_sets:
                if move in allowed_set:
                    p1_allowed_sets[move] += 1

        max_p1_count=max(p1_allowed_sets.values())

        for move in best_moves:
            if p1_allowed_sets[move] == max_p1_count:
                #print("ACTUAL P2 move:", move)
                return move


    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        required_nodes=set()   # sets don't contain duplicates, so (0,2) and (2,4) yields {0,2,4}
        remaining_nodes=set()

        for i in range(NUM_NODES):
            for j in range(i+1,NUM_NODES):
                if board[i][j] == Color.P1 or board[i][j] == Color.P2:  #if the edge is colored by P1 or P2, include those edges for sure
                    required_nodes.add(i)
                    required_nodes.add(j)


        all_nodes=set(range(NUM_NODES))   #{0,1,2,3,4,5}
        remaining_nodes=all_nodes - required_nodes   # ex {1,3,5}

# now we are trying to see what other node we can add to our minimal board along with required nodes
        from itertools import combinations

        for size in range(0, len(remaining_nodes) + 1):   # size 0,1,2,3
            for extra_nodes in combinations(remaining_nodes, size):  #{{1,3,5}, 1} for size=1
                candidate_nodes=required_nodes.union(extra_nodes)  # this will make combination of required_nodes and extra node, one by one (size starts from 0)
                                                                 #Ex required nodes=0,2,4
                                                                #candidate_nodes will be required nodes only in the beginning as size=0
                flag=True                                   # For now, assume this candidate is valid/complete

                for i in candidate_nodes:           # looping through candidate nodes {0,2,4,1} for example
                    for j in candidate_nodes:
                        if board[i][j] == Color.NONE and i!=j:   # if the edge from two nodes is not colored, and both nodes are not same like 1,1
                            flag=False                           # set flag=false
                            break

                    if not flag:                              #if flag is false, break
                        break

                if flag:                             # if above condition satisfies, then proceed with making candidate board from these nodes
                    candidate_board=[]

                    for i in range(NUM_NODES):   # goes row by row through the 6×6 board, for each row, rows starts empty
                        rows=[]
                        for j in range(NUM_NODES):  #go through each column
                            if i in candidate_nodes and j in candidate_nodes:   #if i and j both exists in candidate nodes already
                                rows.append(board[i][j])   # keep the original board and copy the board into rows[].
                            else:
                                rows.append(Color.NONE)    # mark those edge as non-colored and append in rows[]
                        candidate_board.append(rows)       # add in candidate board

                    allowed=Player2.get_allowed_moves(Color.P2,candidate_board)  #get allowed moves from func, but with new minimal board as argument, what moves can P2 safely make based on this minimal board

                    if len(allowed)>0:   #if there are 1 or more moves, return any
                        return candidate_board   #this candidate board is passed


        return None

        #raise NotImplementedError

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """
        valid_sets=set()
        allowed_moves=Player2.get_allowed_moves(player,board)  # call all allowed moves from function.
        from itertools import combinations

        for size in range(1, len(allowed_moves) +1):
            for combo in combinations(allowed_moves, size):
                is_allowed = True
                for i, j in combo:
                    for k in range(NUM_NODES):
                        if k==i or k==j:       # if k==i or j, we would look for another k (continue), otherwise 2 nodes cannot make a triangle
                            continue

                        jk = (min(j, k), max(j, k))
                        ik = (min(i, k), max(i, k))
                        edge1 = board[i][j] == player or (i, j) in combo    #if edge is colored by player, or the edge already exists in combo
                        edge2 = board[j][k] == player or jk in combo
                        edge3 = board[i][k] == player or ik in combo

                        if edge1 and edge2 and edge3:   #if all three edges are colored by that player
                            is_allowed = False
                            break
                    if not is_allowed:
                        break
                if is_allowed:
                    valid_sets.add(frozenset(combo))

        if len(valid_sets) == 0:
            return set()

        max_size = max(len(s) for s in valid_sets)

        maximal_sets = set()

        for s in valid_sets:
            if len(s) == max_size:
                maximal_sets.add(s)

        return maximal_sets

        return max(valid_sets)
                #return frozenset([edge1,edge2,edge3])

        #raise NotImplementedError

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.

        """

        allowed_moves = []

        for i in range(NUM_NODES):
            for j in range(i+1, NUM_NODES):
                if board[i][j] == Color.UNCOLORED:    #if node is uncolored
                    is_allowed=True                   # flag = true
                    for k in range(NUM_NODES):        # k in board, third node of the triangle
                        if board[i][k] == player and board[j][k] == player: #if i,k or j,k is already colored by player
                            is_allowed=False          # flag=false

                    if is_allowed:                    # if flag= false
                        allowed_moves.append((i, j))   # add that edge to allowed moves
        return allowed_moves



        raise NotImplementedError
