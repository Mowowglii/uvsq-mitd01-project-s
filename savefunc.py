#Imports
import json
import numpy as np

def save_state(gridsdkboard:list, gridnp:np.ndarray, user_pos:list[tuple[int]], error_count:int, ids_text:dict, ids_cells:dict, coorderrorList:list[tuple[int]], minutes:int, seconds:int, difficulty:float):
    """Save in a file informations of game

    Args:
        gridsdk (list): The grid of game in format sdk.Sudoku (the original puzzle)
        grid (np.ndarray): the grid of game in format numpy array (with every modifications done by the user)
        user_pos (tuple[int]): the last position of the user 
        error_count (int): number of error done
        ids_text (dict): the ids of the numbers displayed in the grid 
        ids_cells (dict): the ids of the cells forming the grid
        coorderrorList (list[tuple[int]]): list of error coordinates
        minutes (int): total minutes player have been playing this grid
        seconds (int): total seconds player have been playing this grid
        difficulty (float): the difficulty of the grid puzzle
    """
    #Converting every list into a json treatable data
    gridL=gridnp.astype(int).tolist()
    #Init a new coord error list
    new_coorderrorl=[]
    for coord in coorderrorList:
        new_coorderrorl.append((int(coord[0]), int(coord[1])))
    #Storing every game information in a dictionary
    save_data={
        "gridname":"Lastgrid", 
        "gridsdkboard":list(gridsdkboard) ,
        "gridnp":gridL, 
        "user_pos":list(user_pos), 
        "error_count":error_count, 
        "ids_txt":ids_text, 
        "ids_cells":ids_cells, 
        "coorderrorlist":new_coorderrorl, 
        "minute":minutes, "seconds":seconds, 
        "difficulty":difficulty
        }
    
    #Create a file in format JSON that will stock the game data
    with open("savesfiles/save_state.json","w") as f:
        #converting the python object to a json 
        f.write(json.dumps(save_data, indent=4))