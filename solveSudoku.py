# Author: Joe Polin
# Course: CIS 521 (Artificial Intelligence)
# Assignment: Homework 3, part 1 (Due 3/4/14)
# Description: Use AC3 to solve simple Sudoku puzzles (provided)

import sys
import copy
import time

def charToNum(c):
    '''Convert quoted numbers to nums and *'s to 0's'''
    if c == '*':
        return 0
    else:
        return int(c)

def numToChar(n):
    '''Convert number to char or space'''
    if n == 0:
        return ' '
    else:
        return str(n)

def parseInput(input_vect):
    '''Parse input to program'''
    if len(sys.argv)==1:
        print 'Please provide file name of board.'
        return -1
    # Open file
    try:
        f = open(sys.argv[1])
        lines = f.readlines()
        f.close()
        grid = [[[charToNum(num)] for num in row.rstrip('\n')] for row in lines]
    except IOError:
        print "Could not import file properly."
        return -1
    return grid

def dispBoardDef(board):
    '''Display board using default format'''
    if board is None:
        print 'No Solution'
        return
    for r in board:
        row_string = ''
        for c in r:
            if c == 0:
                row_string += '*'
                continue
            row_string += str(c[0])
        print row_string

def dispBoard(board):
    '''Display board nicely'''
    if board is None:
        print 'No Solution'
        return
    # Print
    s = '|%s %s %s | %s %s %s | %s %s %s |'
    hline = '------------------------'
    print hline
    for i,r in enumerate(board):
        rc = []
        for c in r:
            if len(c) > 1:
                rc += 'x'
            else:
                rc += numToChar(c[0])
        print s % tuple(rc)
        if i % 3 == 2:
            print hline

def buildDomain(board):
    '''Takes in board with numbers and 0's and builds 9x9 grid with domain for each square'''
    domain = copy.deepcopy(board)
    all_num = [x for x in range(1,10)] 
    for r,row in enumerate(board):
        for c,element in enumerate(row):
            if element==[0]:
                domain[r][c] = copy.copy(all_num)
            else:
                domain[r][c] = element
    return domain 

def AC3(domain):
    '''Apply AC3 CSP strategy to domain.'''
   # Build a 4D matrix where each entry i a 9x9 binary board
    arcs_mat = [[getRelated(r,c) for r in range(0,9)] for c in range(0, 9)]
    arcs_list = mat2list(arcs_mat)
    # Iterate through arcs_list until it is empty
    while len(arcs_list) > 0:
        # Take top arc and remove it
        arc = arcs_list[0]
        arcs_list = arcs_list[1:]
        # o_ means origin, d_ means destination
        orow = arc[0][0]
        ocol = arc[0][1]
        drow = arc[1][0]
        dcol = arc[1][1]
        odom = domain[orow][ocol]
        ddom = domain[drow][dcol]
        # Can only rule soemthing out if destination is a single #
        if len(odom) == 1 or len(ddom) > 1:
            continue
        dval = ddom[0]
        if dval in odom:
            # Remove it from the domain
            domain[orow][ocol].remove(dval)
            # Add all associated arcs back to queue if it's now 1 element
            new_arcs = getRelated(orow, ocol)
            new_arcs = [[dest, orig] for [orig, dest] in new_arcs]
            for ar in new_arcs:
                if ar not in arcs_list:
                    arcs_list += [ar]
    return domain
# Check if all domains are down to 1 number
#    for row in domain:
#        for element in row:
#            if len(element) > 1:
#                return domain   
#    # When we reach here, there should be one number per domain
#    return [[domain[i][j] for j,c in enumerate(row)] for i,row in enumerate(domain)]

def mat2list(mat):
    final_list = []
    for r in mat:
        for c in r:
            for e in c:
             final_list += [e]
    return final_list

def getRelated(r,c):
    '''Return list of list of tuples'''
    related = []
    cur = (r,c)
    for n in range(0,9):
        # Get all in same row
        if c != n:
            related += [[cur, (r, n)]]
        # Get all in same column
        if r != n:
            related += [[cur, (n, c)]]
    # Get all in same block
    row_start = (int(r)/3) * 3
    col_start = (int(c)/3) * 3
    for row in range(row_start, row_start+3):
        for col in range(col_start, col_start+3):
            if row != r and col != c:
                related += [[cur, (row, col)]]
    return related

def verifyBoard(board):
    if board is None:
        return False
    # Check rows
    all_num = [x for x in range(1,9)]
    for ir, row in enumerate(board):
        for n in all_num:
            if [n] not in row:
    #            print 'Error in row consistency in row ' + str(ir) + ' (no ' + str(n) + ')'
                return False
    # Check columns
    for col in range(0,8):
        column = []
        for row in board:
            column += [row[col]]
        for n in all_num:
            if [n] not in column:
     #           print 'Error in column consistency.'
                return False
    # Check 3x3 squares
    for h in range(0,2):
        for v in range(0,2):
            box_nums = []
            for hi in range(3*h,3*h+3):
                for vi in range(3*v, 3*v+3):
                    box_nums += [board[vi][hi]]
            for n in all_num:
                if [n] not in box_nums:
      #              print 'Error in box consistency.'
                    return False
    return True

def processOfElimination(input_domain):
    '''Make sure each number only appears once per column, row, or box--at most'''
    occurrences = [[],[],[],[],[],[],[],[],[]]        
    domain = copy.deepcopy(input_domain)
    # Perform AC-3 check
    board = AC3(domain) # board is refined domain, fyi
    # First check rows
    for r,row in enumerate(board):
        occs = copy.deepcopy(occurrences)
        for c, col in enumerate(row):
            for d in col:
                occs[d-1]+=[(c,100)]
        # Check if any numbers only occurred once
        for val, oc in enumerate(occs):
            if len(oc) == 1:
                # Remove all other numbers from domain
                col_i = oc[0][0]
                board[r][col_i] = [val+1]
    # Now check columns
    for ci in xrange(0,9):
        occs = copy.deepcopy(occurrences)
        for ri in xrange(0,9):
            for d in board[ri][ci]:
                occs[d-1]+=[(ri,100)]
        for val, oc in enumerate(occs):
            if len(oc) == 1:
                row_i = oc[0][0]
                board[row_i][ci] = [val + 1]
    # Now do the sub-grids
    for subgrid_row in xrange(0,3):
        for subgrid_col in xrange(0,3):
            occs = copy.deepcopy(occurrences)
            for ri in xrange(3*subgrid_row, 3*subgrid_row + 3):
                for ci in xrange(3*subgrid_col, 3*subgrid_col + 3):
                    for d in board[ri][ci]:
                        occs[d-1] += [(ri,ci)]
            for val, oc in enumerate(occs):
                if len(oc) == 1:
                    rit = oc[0][0]
                    cit = oc[0][1]
                    board[rit][cit] = [val+1]
    # Check whether any changes were made. If so, do this again
    if input_domain == board:
        return board
    else:
        return processOfElimination(board)

def solveSudoku(domains):
    '''First tries logic, then guesses.'''
    logic_domain = processOfElimination(domains)
    # See if we got it just with logic
    if verifyBoard(logic_domain):
        return logic_domain
    # Find most constrained domain that is more than 1 item
    min_poss_val = 10
    for ri, r in enumerate(logic_domain):
        for ci, c in enumerate(r):
            if len(c) == 1:
                continue
            elif len(c) < min_poss_val:
                row_i = ri
                col_i = ci
                min_poss_val = len(c)
    # If no values to change, we're at the end of a branch
    if min_poss_val == 10:
        return False
    # Now try a value for that (should do least-constraining at some point)
    for new_val in logic_domain[row_i][col_i]:
        new_domain = copy.deepcopy(logic_domain)
        new_domain[row_i][col_i] = [new_val]
        result = solveSudoku(new_domain)
        if result is not False:
            return result
    return False
    
if __name__ == '__main__':
    pretty = True # False puts in default form
    # Open file and import
    init_board = parseInput(sys.argv)
    if init_board == -1:
        sys.exit()
    print 'Initial board:'
    if pretty:
        dispBoard(init_board)
    else:
        dispBoardDef(init_board)
   
    board = buildDomain(init_board)
  
    final_board = solveSudoku(board)
    print 'Final Board:'
    if pretty:
        dispBoard(final_board)
    else:
        dispBoardDef(final_board)
    boardStatus = verifyBoard(final_board)
    print 'Board is valid:' + str(boardStatus)
   
