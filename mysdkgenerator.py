import random as rd
import numpy as np

def Sgrid_li_and_col_verification(grid:np.ndarray, return_info:bool=False):
    """Verify if the lines and column are valid for a sudoku grid

    Args:
        grid (np.ndarray): the grid to verify
        return_info (bool): return all the infos. Default set to False

    Returns:
        bool: True if test is valid, False if not. Default return
        list[bool, int,list[list[int]]]: [bool if test is valid, error value, list of coordinates[row, column]]
    """
    state=True
    for i,t in zip([m for m in range(np.shape(grid)[0])],[l for l in range(np.shape(grid)[1])]):
        line = grid[i]
        column = grid[0:np.shape(grid)[1], t]
        value1, count1 = np.unique(line, return_counts=True)
        value2, count2 = np.unique(column, return_counts=True)
        for val1,coun1 in zip(value1,count1):
            if val1<=9 and val1>=1 and coun1 > 1:
                indexlist=[[i, np.where(line==val1)[0][q]] for q in range(np.shape(np.where(line==val1)[0])[0])]
                state=False
                if return_info==True:
                    return [state, val1, indexlist]
        for val2,coun2 in zip(value2,count2):
            if val2>=1 and val2<= 9 and coun2 > 1:
                indexlist=[[np.where(column==val2)[0][h],t] for h in range(np.shape(np.where(column==val2)[0])[0])]
                state = False
                if return_info==True:
                    return [state, val2, indexlist]
    return state

def Sgrid_all_regions_verification(grid:np.ndarray, return_info:bool=False):
    """Verify if the grid's regions are valid

    Args:
        grid (np.ndarray): the grid to verify
        return_info (bool): return all the infos. Default set to False
    Returns:
        bool: True if the regions are valid, False if the regions aren't
        list[bool, int, int, list[list[int]]]: [bool if test is valid, region, value, list of coordinates[row,column]]
    """
    state = True
    #Regions treatment
    r=0
    for line in range(0,7,3):
        for column in range(0,7,3):
            r+=1
            region=grid[line:line+3,column:column+3].reshape(-1)
            value,count=np.unique(region, return_counts=True)
            for v,c in zip(value,count):
                if v<=9 and v>=1 and c>1:
                    indexlist=[[line+(np.where(region==v)[0][g]//3), column+np.where(region==v)[0][g]%3] for g in range(np.shape(np.where(region==v)[0])[0])]
                    state=False
                    if return_info==True:
                        return [state, v, indexlist]
                    break
    return state

def generate_empty()->np.ndarray:
    """Generate an 9x9 empty grid

    Returns:
        np.ndarray: an empty grid
    """
    grid=np.zeros((9,9), dtype=np.int8)
    return grid

def line_possibility(grid:np.ndarray, return_forbidden:bool=False)->list[list[int]]:
    """Check values possibility in each line of the grid

    Args:
        grid (np.ndarray): the grid we are checking
        return_forbidden (bool): If set to True, return the forbidden values list. Default to False
    Returns:
        list[list[int]]: the matrix of number possibility in each line (length of line = 9)
        list[int]: the forbidden values list
    """
    #Init list for forbidden values
    forbiddenL=[[]for i in range(9)]
    #Creating the matrix of number possibility
    num_possibility=[[i for i in range(1,10)] for t in range(9)]
#Modifying it by looking at the grid
    #Searching for non null values
    grid_non_null_coordL = [[np.where(grid!=0)[0][d], np.where(grid!=0)[1][d]] for d in range(np.shape(np.where(grid!=0)[0])[0])]
    #Stocking non null values in a list
    valuesL=[grid[coordinate[0], coordinate[1]] for coordinate in grid_non_null_coordL]
    #Deleting values in matrix
    for coord, value in zip(grid_non_null_coordL, valuesL):
        if value not in forbiddenL[coord[0]]:
            forbiddenL[coord[0]].append(value)
        if value in num_possibility[coord[0]]:
            num_possibility[coord[0]].remove(value)
    #If user wants the forbidden value list
    if return_forbidden == True:
        return forbiddenL
    return num_possibility

def column_possibility(grid:np.ndarray, return_forbidden:bool=False)->list[list[int]]:
    """Check values possibility in each columns of the grid

    Args:
        grid (np.ndarray): the grid we are checking
        return_forbidden (bool): If set to True, return the forbidden values list. Default to False
    Returns:
        list[list[int]]: the matrix of number possibility in each column, a line in this list is a column in grid (lenght of a line = 9)
        list[int]: the forbidden values list
    """
    #Init list of forbidden values
    forbiddenL=[[] for i in range(9)]
    #Creating the matrix of number possibility
    num_possibility=[[i for i in range(1,10)] for t in range(9)]
#Modifying it by looking at the grid
    #Searching for non null values
    grid_non_null_coordL = [[np.where(grid!=0)[0][d], np.where(grid!=0)[1][d]] for d in range(np.shape(np.where(grid!=0)[0])[0])]
    #Stocking non null values in a list
    valuesL=[grid[coordinate[0], coordinate[1]] for coordinate in grid_non_null_coordL]
    #Deleting values in matrix
    for coord, value in zip(grid_non_null_coordL, valuesL):
        if value not in forbiddenL[coord[1]]:
            forbiddenL[coord[1]].append(value)
        if value in num_possibility[coord[1]]:
            num_possibility[coord[1]].remove(value)
    if return_forbidden == True:
        return forbiddenL
    return num_possibility

def region_possibility(grid:np.ndarray, return_forbidden:bool=False)->list[list[int]]:
    """Check values possibility in each regions of the grid

    Args:
        grid (np.ndarray): the grid we are checking
        return_forbidden (bool): If set to True, return the forbidden values list. Default to False

    Returns:
        list[list[int]]: matrix of region, each line of this matrix is a region of the grid, (lenght of a line = 9)
        list[int]: forbidden values list
    """
    #Init a list of forbidden value
    forbiddenL=[[] for i in range(9)]
    #Creating the matrix of number possibility
    num_possibility=[[i for i in range(1,10)] for t in range(9)]
#Modifying it by looking at the grid
    #Searching by regions
    r = 0 #region variable to set the line in the final matrix
    for l in range(0,7,3):
        for c in range(0,7,3):
            #Slicing into regions
            region=grid[l:l+3, c:c+3]
            #Checking for non null value in each regions
            non_null_in_regionL = [[np.where(region!=0)[0][s], np.where(region!=0)[1][s]] for s in range(np.shape(np.where(region!=0)[0])[0])]
            #Stocking non null values in region into a list
            valuesL=[region[coord[0], coord[1]] for coord in non_null_in_regionL]
            for value in valuesL:
                if value not in forbiddenL[r]:
                    forbiddenL[r].append(value)
                if value in num_possibility[r]:
                    num_possibility[r].remove(value)
            r+=1
    if return_forbidden == True:
        return forbiddenL
    return num_possibility

def coords_columns(grid:np.ndarray, coord:tuple[int])->list[tuple[int]]:
    """Gives every coordinates in value's column that is available

    Args:
        grid (np.ndarray): the grid we are checking
        coord_col (int): the column coordinate of the value in grid

    Returns:
        list[tuple[int]]: every coordinates in column that is available
    """
    #The list of available coordinate in column from the position in grid
    coordsl=[(np.where(grid[0:, coord[1]]==0)[0][i], coord[1]) for i in range(np.shape(np.where(grid[0:,coord[1]]==0)[0])[0])]
    return coordsl

def coords_lines(grid:np.ndarray, coord_li:int)->list[tuple[int]]:
    """Gives every coordinates in value's line that is available

    Args:
        grid (np.ndarray): the grid we are checking
        coord_li (int): the line coordinate of the value in grid

    Returns:
        list[tuple[int]]: every coordinates in line that is available
    """
    #The list of available coordinate in line from the position in grid
    coordsl=[(coord_li, np.where(grid[coord_li]==0)[0][i]) for i in range(np.shape(np.where(grid[coord_li]==0)[0])[0])]
    return coordsl

def coords_reg(grid:np.ndarray, coord:tuple[int])->list[tuple[int]]:
    """Gives every coordinates in region that is available

    Args:
        grid (np.ndarray): the grid we are checking
        coords (tuple[int]): coordinate of the value in grid

    Returns:
        list[tuple[int]]: every coordinates in region that is available
    """
    #Unpack the coord
    x,y=coord
    #Init the list of return
    coordsL=[]
    #Slicing the grid into regions
    for l in range(0,7,3):
        for c in range(0,7,3):
            region = grid[l:l+3, c:c+3]
            #Checking if the value is in the region
            if (coord[0]>= l and coord[0] <= l+2) and (coord[1] >= c and coord[1] <= c+2):
                #Stocking every coordinates in region that is available 
                coordsL=[(l+np.where(region==0)[0][w], (c+np.where(region==0)[1][w])) for w in range(np.shape(np.where(region==0)[0])[0])]
    return coordsL

def reg_coord(coord:tuple[int])->int:
    """Gives the region of the value coord

    Args:
        coord (list[int]): coordinate of the value

    Returns:
        int: the region number (upleft is 0, upcenter is 1, upright is 2,...)
    """
    #unpacking the coord
    x,y=coord
    #init the region value
    r=0
    #Slicing the grid
    for line in range(0,7,3):
        for column in range(0,7,3):
            if ((line+2)>= x and x>=line) and ((column+2)>=y and y>=column-1):
                return r
            r+=1

def global_available_coords(grid:np.ndarray)->list[tuple[int]]:
    """See for global available coords in grid

    Args:
        grid (np.ndarray): the grid we are searching for blank

    Returns:
        list[tuple[int]]: every available coords
    """
    #The list of every available coords
    coordsl=[(np.where(grid==0)[0][i], np.where(grid==0)[1][i]) for i in range(np.shape(np.where(grid==0)[0])[0])]
    return coordsl

def available_coords(grid:np.ndarray, coord:tuple[int,int])->list[tuple[int]]:
    """Gives every available coord from value position in grid vertically, horizontally and in region

    Args:
        grid (np.ndarray): the grid we are checking
        coord (tuple[int]): the coord of the value

    Returns:
        list[tuple[int]]: every available coord from value coord
    """
    sumlist= coords_lines(grid, coord[0]) + coords_columns(grid, coord) + coords_reg(grid, coord)
    #List treatment to remove every doubles in list
    all=[]
    for coordinate in sumlist:
        if coordinate not in all:
            all.append(coordinate)
    return all

def available_value(grid:np.ndarray, coord:tuple[int])->list[int]:
    """Gives all the available value in coord

    Args:
        grid (np.ndarray): the grid we are checking
        coord (tuple[int]): the coordinate of the insertion

    Returns:
        list[int]: every value available
    """
    #Init the generic available values
    available_valuesL=[i for i in range(1,10)]
    #Init all the forbidden values list
    line_forbidden=line_possibility(grid, return_forbidden=True)[coord[0]]
    column_forbidden=column_possibility(grid, return_forbidden=True)[coord[1]]
    region_forbidden=region_possibility(grid, return_forbidden=True)[reg_coord(coord)]
    #Sumarise all the forbidden lists
    all_forbidden=line_forbidden+column_forbidden+region_forbidden
    #Init the definitive list of forbidden value
    definitive_all_forbidden=[]
    #Adding items into it
    for item in all_forbidden:
        if item not in definitive_all_forbidden:
            definitive_all_forbidden.append(item)
    #Removing Forbidden values from generic availabe values
    for value in definitive_all_forbidden:
        if value in available_valuesL:
            available_valuesL.remove(value)
    available_valuesL.sort()
    return available_valuesL

def grid_valid(grid:np.ndarray)->bool:
    """Telling if the grid is valid or not

    Args:
        grid (np.ndarray): the grid we are verifying

    Returns:
        bool: True if it's valid and False if not.
    """
    if np.shape(np.where(grid==0)[0])[0]==0 and Sgrid_all_regions_verification(grid)==True and Sgrid_li_and_col_verification(grid)==True:
        return True
    else:
        return False

def init_fill_algorithm(grid:np.ndarray)->np.ndarray:
    """Init a Sudoku Grid Filling
    Args:
        grid (np.ndarray): the grid to init
    
    Returns:
        np.ndarray: a grid ready to be filled
    """
    global Lpath
    global Lvalues
    global empty_cells
    #Init a path list where coordinate played will be stocked
    Lpath=[(rd.randint(0,8),rd.randint(0,8))]
    #Init a value list where the value injected will be stocked
    Lvalues=[1]
    #Init a list that contain every empty cells of the grid
    empty_cells=global_available_coords(grid)
#INIT THE ALGORITHM
    #Injecting the value from Lvalues in grid at position from Lpath
    grid[Lpath[0][0], Lpath[0][1]]=Lvalues[0]
    return grid

def fill_algorithm(grid:np.ndarray)->np.ndarray:
    """Fill a grid to become a Sudoku Grid
    (I found the filling algorithm by watching a video about it from the Youtube channel Clarity Media)

    Args:
        grid (np.ndarray): _description_

    Returns:
        np.ndarray: _description_
    """
    global Lpath
    global Lvalues
#EXECUTE THE ALGORITHM
    #Until the grid is filled
    while len(empty_cells)!=0:
        #Checking if there is available coords at current position for conventional movement
        if len(available_coords(grid, Lpath[-1]))!=0:
            #Choosing a new position from currrent position
            choice_pos=rd.choice(available_coords(grid, Lpath[-1]))
            #Checking if the available value of choice_pos is not empty
            if len(available_value(grid, choice_pos))==0:
                #Adding the blocked coordinate to the path
                Lpath.append(choice_pos)
                #Adding 0 to the Lvalues so we can treat it during Back Tracking
                Lvalues.append(0)
                #Break the loop, an error was encountered
                break
            else:
                #Choosing value to inject as the minimum of available value
                choice_value=available_value(grid, choice_pos)[0]
                #Inject the value in the grid
                grid[choice_pos[0], choice_pos[1]]=choice_value
                #Updating the history lists
                Lpath.append(choice_pos)
                Lvalues.append(choice_value)
        #If there is not, set a new random available location in grid for next position and injecting a value in it
        #else:
        #    choice_pos=rd.choice(empty_cells)
        #    if len(available_value(grid, choice_pos))==0:
        #        Lpath.append(choice_pos)
        #        Lvalues.append(0)
        #        break
        #    else:
        #        choice_value=available_value(grid,choice_pos)[0]
        #        grid[choice_pos[0], choice_pos[1]]=choice_value
        #        Lpath.append(choice_pos)
        #        Lvalues.append(choice_value)
    return grid

def blocking_id(grid:np.ndarray):
    """Identify the value that blocks the filling algorithm

    Args:
        grid (np.ndarray): the blocked grid
    """
    global Lpath
    global Lvalues
#Value that must be in the cell
    #take the shorter len of available value for region possibility, column possibility and row possibility
    #init a variable containing the needed value
    region_needed=None
    column_needed=None
    line_needed=None
    if len(region_possibility(grid)[reg_coord(Lpath[-1])])<len(column_possibility(grid)[Lpath[-1][1]]) and len(region_possibility(grid)[reg_coord(Lpath[-1])])<len(line_possibility(grid)[Lpath[-1][0]]):
        region_needed=region_possibility(grid)[reg_coord(Lpath[-1])][0]
    elif len(column_possibility(grid)[Lpath[-1][1]])<len(region_possibility(grid)[reg_coord(Lpath[-1])]) and len(column_possibility(grid)[Lpath[-1][1]])<len(line_possibility(grid)[Lpath[-1][0]]):
        column_needed=column_possibility(grid)[Lpath[-1][1]][0]
    elif len(line_possibility(grid)[Lpath[-1][1]])<len(region_possibility(grid)[reg_coord(Lpath[-1])]) and len(line_possibility(grid)[Lpath[-1][1]])<len(column_possibility(grid)[Lpath[-1][1]]):
        line_needed=line_possibility(grid)[Lpath[-1][0]][0]
    return column_needed, line_needed, region_needed

def backtracking_coord_search(grid:np.ndarray):
    """Modify the path and value history list to prepare for backtracking.
    Find the decision position by setting dead position (position where there is no possible decision) to 0.    
    Args:
        grid (np.ndarray): the grid that we'll analyze
    """
    global Lpath
    global Lvalues
#Searching for a position that can unlock the situation
    #Browse the History lists from the index of value before 0 to the start of the list (i is the pointer)
    for i in range(Lvalues.index(0)-1,-1,-1):
        #Setting its value in grid to 0 for the test
        grid[Lpath[i][0], Lpath[i][1]]=0
        #Checking if there's more than 1 available value in this position
        if len(available_value(grid, Lpath[i]))>1:
            #No restoring the value in grid because its better for the backtrackign attempt
            break
        else:
            #Set its value to 0 in history
            Lvalues[i]=0
            #A position was found stop searching part and go for the attempt

def backtracking_value_search(grid:np.ndarray):
    """Find a value at a specific position found from backtracking_coord_search function that can unlock the situation
    Args:
        grid (np.ndarray): the grid we are analyzing
    """
    global Lpath
    global Lvalues
    #Set the basic index of the position found (Position is always before a 0 in Lvalues)
    index=Lvalues.index(0)-1
    #Set a available value list for this position to set the loop of attempting
    av_value=available_value(grid, Lpath[index])
#Loop of attempting at this position
    while len(av_value)!=0:
    #init the attempt
        #Set a value for the selected position from backtracking_search function
        print(Lpath[index])
        print(av_value)
        value=av_value[0]
        print(value)
        #update in grid
        grid[Lpath[index][0], Lpath[index][1]]=value
        #update in history
        Lvalues[index]=value
        #fill the grid following the path
        for coordinate in Lpath[index+1:]:
            #Checking if there is no available values, it's not the right value to unlock
            if len(available_value(grid, coordinate))==0:
                #erasing the progress
                for i in range(index+1,Lpath.index(coordinate)):
                    #in history 
                    Lvalues[i]=0
                    #in grid
                    grid[Lpath[i][0], Lpath[i][1]]=0
                #update av_value
                av_value.pop(0)
                #Stop filling and try for another value in decision position
                break
            else:
                #Set the choice of value
                choice_value=available_value(grid, coordinate)[0]
                #Set the position value to the minimal available value
                grid[coordinate[0], coordinate[1]]=choice_value
                #Updating Lvalues
                Lvalues[Lpath.index(coordinate)]=choice_value
                print(coordinate)
                print(choice_value)
                print(grid)
                print(Lpath)
                print(Lvalues)
        #Checking if there is null value in Lvalues and stop the loop if solution has been found
        if 0 not in Lvalues:
            break
    #If all the values has been tested and the last injection is still impossible
    if Lvalues[-1]==0:
        #set the decision position and every position after as dead positions
        for i in range(index,len(Lvalues)):
            #In History
            Lvalues[i]=0
            #In Grid
            grid[Lpath[i][0], Lpath[i][1]]=0

def generateSDK():
    """Generate a Sudoku Grid Solution
    """
    grid=generate_empty()
    init_fill_algorithm(grid)
    while grid_valid(grid)!=True:
        fill_algorithm(grid)
        while Lvalues[-1]==0:
            backtracking_coord_search(grid)
            backtracking_value_search(grid)
        print(grid)
        print(Lpath)
        print(len(Lpath))
        print(Lvalues)
        print(len(Lvalues))
    return grid

#Function Test Zone
grid = generate_empty()
init_fill_algorithm(grid)
fill_algorithm(grid)
#while 0 in Lvalues:
#    backtracking_coord_search(grid)
#    backtracking_value_search(grid)
#fill_algorithm(grid)
print(grid)
print(Lpath)
print(len(Lpath))
print(Lvalues)
print(len(Lvalues))
print(grid_valid(grid))
print(blocking_id(grid))
#Grid Verification Test Area
#grid= np.array([
#  [3, 9, 1, 2, 8, 6, 5, 7, 4],
#  [4, 8, 7, 3, 5, 9, 1, 2, 6],
#  [6, 5, 2, 7, 1, 4, 8, 3, 9],
#  [8, 7, 5, 4, 3, 1, 6, 9, 2],
#  [2, 1, 3, 9, 6, 7, 4, 8, 5],
#  [9, 6, 4, 5, 2, 8, 7, 1, 3],
#  [1, 4, 9, 6, 7, 3, 2, 5, 8],
#  [5, 3, 8, 1, 4, 2, 9, 6, 7],
#  [7, 2, 6, 8, 9, 5, 3, 4, 1]
#], dtype=np.int8)
#print(grid_valid(grid))
#print(Sgrid_all_regions_verification(grid, return_info=True))
#print(Sgrid_li_and_col_verification(grid, return_info=True))