from mysdkgenerator import *
import numpy as np
import sudoku as sdk

#Global Variables

def generate_grid(difficulty:int=0.4):
    """generate a sudoku grid using the sudoku library
    Args:
        difficulty (int): beetween number beetween 0 and 1, set the difficulty of the grid. Default set to max difficulty (0.8)
    
    """
    #generate the grid via the library
    grid=sdk.Sudoku(3).difficulty(difficulty)
    return grid

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
    grid[coordinate[0], coordinate[1]]=value

def erase(grid:np.ndarray, coordinate:tuple[int]):
    """Erase the content of a cell

    Args:
        grid (np.ndarray): the play grid
        coordinate (tuple[int]): the position of the user where he want to erase
    """
    grid[coordinate[0], coordinate[1]]=0

def convert_sdk_to_np(grid:sdk.Sudoku)->np.ndarray:
    """Convert a object of type sdk.Sudoku to a np.ndarray

    Args:
        grid (sdk.Sudoku): the grid in sdk.Sudoku

    Returns:
        np.ndarray: the converted grid
    """
    #create an array of zeros
    npgrid=np.zeros((9,9), dtype=np.int8)
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

#Testing Zone