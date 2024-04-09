#Imports
from liblinkfunc import get_values_coord
import json
import os
import numpy as np

def save_state(gridsdkboard:list, gridnp:np.ndarray, error_count:int, ids_text:dict, ids_cells:dict, ids_notes:dict, coorderrorList:list[tuple[int]], minutes:int, seconds:int, difficulty:float):
    """Save in a file informations of game

    Args:
        gridsdk (list): The grid of game in format sdk.Sudoku (the original puzzle)
        grid (np.ndarray): the grid of game in format numpy array (with every modifications done by the user)
        error_count (int): number of error done
        ids_text (dict): the ids of the numbers displayed in the grid 
        ids_cells (dict): the ids of the cells forming the grid
        ids_notes (dict): the ids of the notes on the grid
        coorderrorList (list[tuple[int]]): list of error coordinates
        minutes (int): total minutes player have been playing this grid
        seconds (int): total seconds player have been playing this grid
        difficulty (float): the difficulty of the grid puzzle
    """
#Erase every error if there was during saving
    #Checking if user stops in an error move
    if len(coorderrorList)!=0:
        #Getting the coordinates of last error
        for coord in coorderrorList:
            #Checking if the value is not a clue
            if coord not in get_values_coord(gridsdkboard):
                #erasing it inside of the grid
                gridnp[coord[0], coord[1]]=0
                break
    #Converting every list into a json treatable data
    gridL=gridnp.astype(int).tolist()
    #Storing every game information in a dictionary
    save_data={
        "gridname":"Lastgrid", 
        "gridsdkboard":list(gridsdkboard),
        "gridl":gridL, 
        "error_count":error_count, 
        "ids_txt":ids_text, 
        "ids_cells":ids_cells,
        "ids_notes":ids_notes, 
        "minute":minutes, "seconds":seconds, 
        "difficulty":difficulty
        }
    
    #Create a file in format JSON that will stock the game data
    with open("savesfiles/save_state.json","w") as f:
        #converting the python object to a json 
        f.write(json.dumps(save_data, indent=2))

def save_grid(gridsdkboard: list, gridnp:np.ndarray, difficulty:int,  coorderrorList:list[tuple[int]], name:str, timestr=str):
    """Save the Grid information for the play old ones button in main menu

    Args:
        gridsdkboard (list): the sudoku grid converted to a list by the board method
        gridnp (np.ndarray): the sudoku grid converted to a numpy by the converting function
        difficulty (int): the difficulty percentage
        coorderrorList (list[tuple[int]]): the list of coordinates of errors in grid
        name (str): the name of the grid
        timestr (str): the time needed by the user to complete the grid
    """
    #Erase every error if there was during saving
    #Checking if user stops in an error move
    if len(coorderrorList)!=0:
        #Getting the coordinates of last error
        for coord in coorderrorList:
            #Checking if the value is not a clue
            if coord not in get_values_coord(gridsdkboard):
                #erasing it inside of the grid
                gridnp[coord[0], coord[1]]=0
                break
    #Converting every list into a json treatable data
    gridL=gridnp.astype(int).tolist()
    save_data={
        "gridname":name,
        "difficulty":difficulty,
        "time":timestr,
        "gridsdkboard":list(gridsdkboard),
        "gridl":gridL,
    }
    #Checking if the save file already created
    if os.path.exists("savesfiles/save_grids.json") == False:
        #create the file
        with open("savesfiles/save_grids.json","w") as file:
            file.write("[\n")
            file.write("]")
    with open("savesfiles/save_grids.json","r") as f:
        #Recover the data
        saveL=json.loads(f.read())
    #Modify the saving list
    saveL.append(save_data)
    #Open the file in writing mode and inject the new save list
    with open("savesfiles/save_grids.json","w") as fi:
        fi.write(json.dumps(saveL, indent=4))