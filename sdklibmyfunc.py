import numpy as np
import sudoku as sdk


def generate_grid(difficulty:int=0.4):
    """generate a sudoku grid using the sudoku library
    Args:
        difficulty (int): beetween number beetween 0 and 1, set the difficulty of the grid. Default set to max difficulty (0.8)
    
    """
    #generate the grid via the library
    grid=sdk.Sudoku(3).difficulty(difficulty)
    return grid

def manip_grid(grid:sdk.Sudoku):
    """Convert the grid in dtype: sudoku.sudoku.Sudoku into a maniable grid

    Args:
        grid (sdk.Sudoku): the grid in format sudoku.sudoku.Sudoku
    """
    return grid.board

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

def inject(grid:list, coordinate:tuple[int], value:int)->list[list[int]]:
    """inject a value inside of the handled grid

    Args:
        grid (list): handled grid

    Returns:
        list[list[int]]: the grid with injection
    """
    #Debugging part 
    assert coordinate not in get_values_coord(grid)
    #Injecting the value inside of the grid
    grid[coordinate[0]][coordinate[1]]=value

def erase(grid:list, coordinate:tuple[int]):
    """Erase the content of a cell

    Args:
        grid (list): the play grid
        coordinate (tuple[int]): the position of the user where he want to erase
    """
    grid[coordinate[0]][coordinate[1]]=None

#Testing Zone