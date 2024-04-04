from mysdkfunc import *
import numpy as np
import sudoku as sdk

#Global Variables

def get_values_coord(grid:list)->list[tuple[int]]:
    """Gives the clues coordinate in the grid

    Args:
        grid (list): the grid in a maniable format that we are scanning

    Returns:
        list[tuple[int]]: list of coordinates (line, column)
    """
    #init a void list
    coordList=[]
    #Searching for int value in the maniable grid
    for line in grid:
        for element in line:
            if type(element)==int:
                #add position in coordinate list
                coordList.append((grid.index(line), line.index(element)))
    return coordList

def inject(grid:np.ndarray, coordinate:tuple[int], value:int):
    """inject a value inside of the handled grid

    Args:
        grid (list): handled grid
        coordinate (tuple[int]): the coordinate of injection
        value (int): the value to inject
    """
    #Debugging part 
    assert coordinate not in get_values_coord(grid)
    #Injecting the value inside of the grid
    grid[coordinate[0], coordinate[1]]=np.uint8(value)

def erase(grid:np.ndarray, coordinate:tuple[int]):
    """Erase the content of a cell

    Args:
        grid (np.ndarray): the play grid
        coordinate (tuple[int]): the position of the user where he want to erase
    """
    grid[coordinate[0], coordinate[1]]=np.uint8(0)

def convert_sdk_to_np(grid:sdk.Sudoku)->np.ndarray:
    """Convert a object of type sdk.Sudoku to a np.ndarray

    Args:
        grid (sdk.Sudoku): the grid in sdk.Sudoku

    Returns:
        np.ndarray: the converted grid
    """
    #create an array of zeros
    npgrid=np.zeros((9,9), dtype=np.uint8)
    #Convert the grid to a list using board method
    grid=grid.board
    #getting givens coordinate from the grid and store them in the array created
    for coordinate in get_values_coord(grid):
        npgrid[coordinate[0], coordinate[1]]=grid[coordinate[0]][coordinate[1]]
    return npgrid

def default_coord_showL(coordinates:tuple[int])->list[tuple[int]]:
    """Gives all the default coord in same region, line, column as the position helping for user

    Args:
        coordinates (tuple[int]): the position in grid

    Returns:
        list[tuple[int]]: the list with all the coordinates that is default
    """
    #An empty grid for coords finding
    egrid=np.zeros((9,9), dtype=np.int8)
    #injecting value != 0 at the same position as the u_pos in the "empty" grid
    inject(egrid, coordinates, 1)
    #using the coords_line, coords_reg, coords_columns function, recover every available coordinates in the same line and storing it in a list
    coordlist=coords_columns(egrid, coordinates)+coords_lines(egrid, coordinates[0])+coords_reg(egrid, coordinates)
    return coordlist

def get_error_coord(grid:np.ndarray)->list[tuple[int], int]:
    """Get the error coordinates

    Args:
        grid (np.ndarray): the grid we are looking for error

    Returns:
        list[tuple[int], int]: the list of the reason there is an error
    """
    #Init the result return
    definitiveL=[]
    #If Both doesn't contain error
    if Sgrid_all_regions_verification(grid)==True and Sgrid_li_and_col_verification(grid)==True:
        return None
    #If one of the checking doesn't contain any error
    elif Sgrid_li_and_col_verification(grid)==True:
        #Gets all the coordinate of error
        for coordinate in Sgrid_all_regions_verification(grid, return_info=True)[2]:
            #Recover unique coordiantes
            if coordinate not in definitiveL:
                definitiveL.append(coordinate)
        return definitiveL
    elif Sgrid_all_regions_verification(grid)==True:
        #Gets all the coordinate of error
        for coordinate in Sgrid_li_and_col_verification(grid, return_info=True)[2]:
            #Recover unique coordiantes
            if coordinate not in definitiveL:
                definitiveL.append(coordinate)
        return definitiveL
    else:
        #Gets all the coordinate of error
        for coordinate in Sgrid_li_and_col_verification(grid, return_info=True)[2]+Sgrid_all_regions_verification(grid, return_info=True)[2]:
            #Recover unique coordiantes
            if coordinate not in definitiveL:
                definitiveL.append(coordinate)
        return definitiveL
    

#Testing Zone