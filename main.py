#Imports
from mygamefunct import grid_valid
from savefunc import *
from adaptlibfunc import *
import sudoku as sdk
import tkinter as tk
from tkinter import messagebox
import sys
import time
import threading
import json as js

#Init the variable containing time in display
time_str=""

#Link beetween GUI and Game functions

def playgridS(event=tk.Event):
    """The goal of this function is to do the link between the display and the empty grid

    Args:
        event (tk.Event, optional): The event generated (here is click)
    """
    global u_position
    #Checking if an error was done in the previous player move
    if not(u_position is None) and not(get_error_coord(gridnp) is None) and u_position in get_error_coord(gridnp):
        #delete the value inside of the last position on display
        erase_value(u_position)
        #Setting the new value of position
        u_position=mouse_to_case(event.x, event.y)
    else:
        u_position=mouse_to_case(event.x, event.y)
    #Display help for the user to choose a number
    default_highlight_cell(u_position)
    
def usern_selection(number:int):
    """

    Args:
        number (int): The chosen number
    """
    global u_number
    global u_position
    global coorderrorL
    global errorcount
    global errorlabel
    #Setting the global variable of user_number
    u_number=number
#The player is taking notes in the grid
    #checking if the player can take notes and if he wants to take notes
    if gridnp[u_position[0], u_position[1]]==0 and note_mode.get()==True:
        #Checking if the position already have note
        if str(u_position) in ids_notes:
            #checking if the user number is already in cell
            if str(u_number) in ids_notes[str(u_position)]:
                erase_note(u_position, u_number)
            #checking if the user number is not already in cell
            elif str(u_number) not in ids_notes[str(u_position)]:
                inject_note(u_position, u_number)
        #Checking if the position doesn't have note
        elif str(u_position) not in ids_notes:
                #create the sub-dictionary
                ids_notes[str(u_position)]={}
                #inject the note
                inject_note(u_position, u_number)
#The player is injecting value in the grid
    #Checking if the player can inject a value and if he don't want to note something
    if u_position not in cList and gridnp[u_position[0], u_position[1]]==0 and note_mode.get()==False:
        #Checking if there is any note in cell
        if str(u_position) in ids_notes:
            #erase every note in cell
            for ids in ids_notes[str(u_position)].values():
                playcanv.delete(ids)
                #erase in dictionary
            del ids_notes[str(u_position)]
        #Injecting the value in numpy board
        inject(gridnp, u_position, u_number)
        #Displaying in the user interface
        display_in_ugrid(u_position, u_number)
        

#Verifiyng game ends
    if grid_valid(gridnp)==True:
        #loop looking for each cell
        for cellid in list(ids_cell.values()):
            #Highlight every cells in green
            playcanv.itemconfig(cellid, fill="#D5F5E3", outline="black")
        #Stop binding
        playcanv.unbind('<ButtonPress-1>')
    #Stop buttons working
        #Save button
        sbutton.config(state=tk.DISABLED)
        #Note Mode Button
        nbutton.config(state=tk.DISABLED)
        #Erase button
        ebutton.config(state=tk.DISABLED)
        #Loop looking at every widgets in the selection canva
        for widget in selectbcanv.winfo_children():
            #Disable every button
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)
        #Go to the end game window
        end_game()
    else:
        #Checking if there is an error in the grid
        if not(get_error_coord(gridnp) is None):
            #Recover every errors coordinate
            coorderrorL=get_error_coord(gridnp)
            #Update the error count
            errorcount+=1
            #update the label of error
            errorlabel.config(text=f"{errorcount} errors", font=("CleanSans", 10, "bold"))
            #looking each coordinate in error coord
            for coordinate in coorderrorL:
                #Recover the cell id
                idc=ids_cell.get(str(coordinate))
                #Highlight this cell in red
                playcanv.itemconfig(idc, fill="#F1948A", outline="black")

#Display or GUI Functions

#About Notes
def erase_note(position:tuple[int],usern:int):
    """Erase individualy the note of a value in a cell

    Args:
        position (tuple[int]): the position in grid
        usern (int): the user number
    """
    #Delete the note in playcanv
    playcanv.delete(ids_notes[str(position)][str(usern)])
    #Delete the value in notes
    del ids_notes[str(position)][str(usern)]

def inject_note(position:tuple[int], usern:int):
    """Create notes in a cell of the grid

    Args:
        position (tuple[int]): the position in grid
        usern (int): the number user choosed
    """
    global playcanv
    global ids_notes
    #Recovering the canva height and width
    canvx = playcanv.winfo_reqwidth()
    canvy = playcanv.winfo_reqheight()
    #Recovering the cell x0 and y0 position in canva (px)
    casexpos=position[1]*(canvx/9)
    caseypos=position[0]*(canvy/9)
    #Calculate the pixel position of a text in a cell (Formulas given by an AI)
    xtextincell = ((((usern-1)%3)+1)/4)*(canvx/9)
    ytextincell = (int((usern+2)/3)/4)*(canvy/9)
    #Calculate the pixel position of text in canvas
    xtextincanv=casexpos+xtextincell
    ytextincanv=caseypos+ytextincell
    #Create text in canva at positions
    noteid=playcanv.create_text(xtextincanv, ytextincanv, text=usern, font=("CleanSans", 10, "bold"))
    #Catch the id in a temporary dictionary
    ids_notes[str(position)].update({str(usern):noteid})

#About Difficulty
def diffic_name(difficulty:float)->str:
    """Gives the difficulty following the blank/total cells ratio 
    All About Difficulty:
        -easy is set to 0.54 (54% of the grid is blank)
        -medium is set to 0.63 (63% of the grid is blank)
        -hard is set to 0.65 (65% of the grid is blank)
        -very Hard is set to 0.73 (73% of the grid is blank)
        -god Mode is set to 0.80 (80% of the grid is blank)
    Args:
        difficulty (float): the ratio blank/total cells

    Returns:
        str: the difficulty of the grid
    """
    if difficulty == 0.54:
        return "Easy Mode"
    elif difficulty == 0.63:
        return "Medium Mode"
    elif difficulty == 0.65:
        return "Hard Mode"
    elif difficulty == 0.73:
        return "Very Hard Mode"
    elif difficulty == 0.80:
        return "God Mode"
    else:
        return "Personalized Difficulty"

def diff_select(percentage:float):
    """Set the difficulty of the grid

    Args:
        percentage (float): the precentage of difficulty
    """
    global difficulty
    #Verify that percentage are valable
    assert percentage <= 0.80 and percentage >= 0.54
    difficulty=percentage
    #Display in window
    diffselec.config(text=f"{diffic_name(difficulty)} Selected", font=("tahoma", 8))

def diffic_menu():
    """Configuration of the Choosing Difficulty Menu"""
    global diffmenu
    global diffselec
    
    #iconify the root menu
    root.iconify()
    
    #Creating the window
    diffmenu=tk.Toplevel(root)
    diffmenu.geometry("300x325")
    
    #Diffmenu configuration
    diffmenu.grid_propagate(False)
    diffmenu.resizable(False, False)
    
    #Diffmenu grid configuration
    diffmenu.grid_columnconfigure(1, weight=2)
    
    #Creating widgets on window
    namelabel=tk.Label(diffmenu, text="Choose Difficulty", font=("tahoma", 10, "bold"))
    diff1=tk.Button(diffmenu, text="Easy Mode", font=("tahoma", 8, "bold"), width=15, height=2, bg="#DAF7A6",command=lambda:diff_select(0.54))
    diff2=tk.Button(diffmenu, text="Medium Mode", font=("tahoma", 8, "bold"), width=15, height=2, bg="#FFC300",command=lambda:diff_select(0.63))
    diff3=tk.Button(diffmenu, text="Hard Mode", font=("tahoma", 8, "bold"), width=15, height=2, bg="#FF5733",command=lambda:diff_select(0.65))
    diff4=tk.Button(diffmenu, text="Very Hard Mode", font=("tahoma", 8, "bold"), width=15, height=2, bg="#C70039",command=lambda:diff_select(0.73))
    diff5=tk.Button(diffmenu, text="God Mode", font=("tahoma", 8, "bold"), width=15, height=2, bg="#900C3F",command=lambda:diff_select(0.80))
    confirmbut=tk.Button(diffmenu, text="Confirm", font=("tahoma", 8), width=10, height=2,command=initgame)
    cancel=tk.Button(diffmenu, text="Cancel", font=("tahoma", 8), width=10, height=2, command=lambda : (diffmenu.destroy(), root.deiconify()))
    diffselec=tk.Label(diffmenu, text=f"{diffic_name(difficulty)} Selected", font=("tahoma", 8))
    
    #Display widgets in window
    namelabel.grid(row=0, column=1, padx=5, pady=5)
    diff1.grid(row=1, column=1, padx=5, pady=5)
    diff2.grid(row=2, column=1, padx=5, pady=5)
    diff3.grid(row=3, column=1, padx=5, pady=5)
    diff4.grid(row=4, column=1, padx=5, pady=5)
    diff5.grid(row=5, column=1, padx=5, pady=5)
    diffselec.grid(row=6, column=1, padx=5, pady=5)
    confirmbut.grid(row=6, column=2, padx=5, pady=5)
    cancel.grid(row=6, column=0, padx=5, pady=5)

def initgame():
    """Init game window from difficulty menu"""
    global grid
    global gridl
    global gridnp
    global d_name
    #Generate a sudoku grid
    grid=sdk.Sudoku(3, seed=rd.randint(0,sys.maxsize)).difficulty(difficulty)
    #Setting the grids of interaction
    gridl=grid.board
    gridnp=convert_sdk_to_np(grid)
        #Naming the difficulty
    d_name=diffic_name(difficulty)
    #Run the Game window
    game_window()
    #Destroy the difficulty menu 
    diffmenu.destroy()

#About Init of Game Window
def load_game():
    """Set all information for a loaded game
    """
    global gridnp
    global grid
    global gridl
    global ids_cell
    global ids_pgtxt
    global time_str
    global u_position
    global u_number
    global coorderrorL
    global errorcount
    global defaultminute
    global defaultseconds
    global difficulty
    global gridname
    global d_name
    global ids_notes
    #Recover the saved data
    with open("savesfiles/save_state.json", "r") as f:
        savedata=js.load(f)
    #Loading every games informations
    gridname = savedata["gridname"]
    grid = sdk.Sudoku(3,3, board=savedata["gridsdkboard"])
    gridl = grid.board
    gridnp = np.array(savedata["gridl"], dtype=np.uint8)
    u_position=None
    u_number = 0
    errorcount = savedata["error_count"]
    ids_pgtxt = savedata["ids_txt"]
    ids_cell = savedata["ids_cells"]
    ids_notes = savedata["ids_notes"]
    defaultminute = savedata["minute"]
    defaultseconds = savedata["seconds"]
    difficulty = savedata["difficulty"]
    #Naming the difficulty
    d_name=diffic_name(difficulty)
    #Run a game window
    game_window()

def new_game():
    """Set all information for a new game
    """
    global ids_cell
    global ids_pgtxt
    global time_str
    global u_position
    global u_number
    global coorderrorL
    global errorcount
    global defaultminute
    global defaultseconds
    global difficulty
    global gridname
    global d_name
    global ids_notes
#Setting informations of the game
    #Setting global Dictionary or List
    #Setting a dictionary to store the IDs of play grid texts
    ids_pgtxt={}
    ids_cell={}
    ids_notes={}

    #Setting global game variables
    u_position=(0,0)
    u_number=None
    coorderrorL=[]
    errorcount=0
    defaultminute=0
    defaultseconds=0
    gridname="New Grid"
    #(default to easy mode)
    difficulty = 0.54
    diffic_menu()

def pre_load_save(event=tk.Event):
    """Pre-load the saved level user wants to laod from listbox selection"""
    global gridnp
    global grid
    global gridl
    global ids_cell
    global ids_pgtxt
    global time_str
    global u_position
    global u_number
    global coorderrorL
    global errorcount
    global defaultminute
    global defaultseconds
    global difficulty
    global gridname
    global d_name
    global ids_notes
#Setting basic information of game
    #Setting informations of the game
    #Setting global Dictionary or List
    #Setting a dictionary to store the IDs of play grid texts
    ids_pgtxt={}
    ids_cell={}
    ids_notes={}

    #Setting global game variables
    u_position=(0,0)
    u_number=None
    coorderrorL=[]
    errorcount=0
    defaultminute=0
    defaultseconds=0
#Setting loaded informations of game
    #Recover everything to load
    gridname = gridinfL[listbox.curselection()[0]]["gridname"]
    difficulty = gridinfL[listbox.curselection()[0]]["difficulty"]
    d_name = diffic_name(difficulty)
    grid = sdk.Sudoku(3, 3, board=gridinfL[listbox.curselection()[0]]["gridsdkboard"])
    gridl = grid.board
    gridnp = convert_sdk_to_np(grid)
#Update display for the user to have information of the puzzle
    difficultylabel.config(text=f"Difficulty : {d_name}", font=("tahoma", 12))
    errorlab.config(text=f"Errors : {gridinfL[listbox.curselection()[0]]['errors']}", font=("tahoma", 12))
    besttimealabel.config(text=f"Best Time : {gridinfL[listbox.curselection()[0]]['time']}", font=("tahoma", 12))

def play_old_menu(savepath:str):
    """Configuration of the play old menu 

    Args:
        savepath (str): path of the saved grid user wants to replay
    """
    global difficultylabel
    global besttimealabel
    global root
    global listbox
    global gridinfL
    global errorlab
    
    #Load the saves
    with open(savepath, "r") as file:
        #Catch the list containing all the informations about grid
        gridinfL = js.load(file)

    #iconify the root menu
    root.iconify()
    
    #Creating a new window
    play_old_m = tk.Toplevel(root)
    
    #Configure the window
    play_old_m.geometry("600x500")
    play_old_m.resizable(False, False)
    
    #Widgets on window
    frame=tk.Frame(play_old_m, height=500, width=600)
    
    #Frame display configuration
    frame.grid_propagate(False)
    for i in range(4):
        frame.grid_rowconfigure(i, weight=1)
    for j in range(5):
        frame.grid_columnconfigure(j, weight=1)
    #Display on frame
    frame.grid()
    
    #Widgets on frame
    listbox = tk.Listbox(frame, selectmode="single", relief="sunken", height=18, width=40, bd=3, font=("tahoma", 14, "bold"), selectbackground="#797979", selectforeground="#000000", activestyle="none", highlightthickness=0)
    returnbutton = tk.Button(frame, text="Return", font=("tahoma", 12), relief="groove", command=lambda : (play_old_m.destroy(), root.deiconify()))
    confirmbutton = tk.Button(frame, text="Confirm", font=("tahoma", 12), relief="groove", command=lambda : (game_window() , play_old_m.destroy()))
    difficultylabel = tk.Label(frame, text="Difficulty : ---", font=("tahoma", 10))
    besttimealabel = tk.Label(frame, text="Best Time : --:--", font=("tahoma", 10))
    errorlab = tk.Label(frame, text="Errors : --", font=("tahoma", 10))
    
    #Filling the listbox
    for i in range(len(gridinfL)):
        listbox.insert(i, gridinfL[i]["gridname"])
    
    #Display on frame
    listbox.grid(row=0, column=0, rowspan=3,columnspan=5)
    returnbutton.grid(row=3, column=0, padx=10, pady=10)
    difficultylabel.grid(row=3, column=1, padx=10, pady=10)
    errorlab.grid(row=3, column=2, padx=10, pady=10)
    besttimealabel.grid(row=3, column=3, padx=10, pady=10)
    confirmbutton.grid(row=3, column=4, padx=10, pady=10)
    
    #Create a binding for listbox selection
    listbox.bind("<<ListboxSelect>>", pre_load_save)
#About Time
def time_counter():
    """Chronometer setting the time passed since the start of the game (made by an AI)
    """
    global timelabel
    global new_game_window
    global defaultminute
    global defaultseconds
    global minutes
    global seconds
    global time_str
    #Time management (Made by an AI)
    if defaultminute == 0 and defaultseconds == 0:
        start_time=time.time() # Get the starting time
    else:
        start_time=time.time()-((defaultminute*60)+defaultseconds) #Continue the time already passed
    # Run the chronometer until interrupted
    while grid_valid(gridnp)!=True and new_game_window.winfo_exists():
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        min, sec = divmod(elapsed_time, 60) #Calculate the value of minutes and seconds from the elapsed time
        minutes = int(min)#calculate the total minutes player has been playing
        seconds = int(sec)#calculate the total secodns player has been playing
        #Display the time on the extracanvas
        if int(minutes) >= 10 and int(seconds) >= 10:
            time_str=f"{int(minutes)}:{int(seconds)}"
        elif int(minutes)<10 and int(seconds)<10:
            time_str=f"{str(0)+str(int(minutes))}:{str(0)+str(int(seconds))}"
        elif int(minutes)<10 and int(seconds)>=10:
            time_str=f"{str(0)+str(int(minutes))}:{int(seconds)}"
        if int(seconds)<10 and int(minutes)>=10:
            time_str=f"{int(minutes)}:{str(0)+str(int(seconds))}"
        #Configure the label that will contain the time
        timelabel.config(text=time_str, font=("ClearSans", 10, "bold"))
        time.sleep(0.1)
        if not(new_game_window.winfo_exists()):
            return

#About display on Game Window
def default_highlight_cell(coordinate:tuple[int]):
    """Highlight the cells in the same column, line and region of the user position

    Args:
        coordinate (tuple[int]): the coordinate of the cell
    """
    global coorderrorL
    #if len(coorderrorL)!=0:
    #    #reset all the cells configuration except the error coordinates
    #    for cids,coord in zip(list(ids_cell.values()), list(ids_cell.keys())):
    #        if coord not in coorderrorL:
    #            playcanv.itemconfig(cids, fill="white", outline="black")
    #        else:
    #            playcanv.itemconfig(cids, fill="#F1948A", outline="black")
    #else:
    for cids in list(ids_cell.values()):
        playcanv.itemconfig(cids, fill="white", outline="black")
    #recover the coordinates of every cells that has to be highlighted
    for coordinates in default_coord_showL(coordinate):
        #recover the id of the cell in canvas
        cell_id=ids_cell.get(str(coordinates))
        #highlight the cell
        playcanv.itemconfig(cell_id, fill="#D6EAF8")
    #recover the id of the coordinate cell in canvas
    coord_cell_id=ids_cell.get(str(coordinate))
    #highlight the cell a little bit darker than everyone else
    playcanv.itemconfig(coord_cell_id, fill="#85C1E9")

def display_in_ugrid(coordinate:tuple[int], value:int):
    """Dislpay numbers on the grid

    Args:
        coordinate (tuple[int]): position in grid of the number (x_position, y_position)
        value (int): the value to enter inside of the grid
    """
    #Recover the playcanv height and width
    canvawidth = playcanv.winfo_reqwidth()
    canvaheight = playcanv.winfo_reqheight()
    #Getting x position of text
    postxt_y=(caseindex_to_casepx(coordinate[0], coordinate[1])[0])+((canvaheight/9)/2)
    postxt_x=(caseindex_to_casepx(coordinate[0], coordinate[1])[1])+((canvawidth/9)/2)
    #creating text in canva to diplay the number and assign all created text on play grid an ID
    ctxt_id=playcanv.create_text(postxt_x, postxt_y, text=str(value), font=("ClearSans", 20, "bold"))
    #Storing the id of the item in the ids dictionary
    ids_pgtxt[str(coordinate)]=ctxt_id

def erase_value(coordinate:tuple[int]):
    """Erase the value in cell for the user grid display

    Args:
        coordinate (tuple[int]): the position of the user
    """
    global newg_frame
    #Checking if the coordinate is a clue
    if coordinate not in cList:
    #Erase the value in board
        erase(gridnp, coordinate)
    #Erase in user interface
        #recover the id of the item
        txt_id = ids_pgtxt.get(str(coordinate))
        #erase in user interface
        playcanv.delete(txt_id)
    #Checking if the user remove an error and go back to default
    if u_position in coorderrorL:
        #set a pointer looking at the error coordinates
        for coordinates in coorderrorL:
            if coordinates == u_position:
                #recover the id of the error cell
                ercellid=ids_cell.get(str(coordinates))
                #configure the item to its default
                playcanv.itemconfig(ercellid, fill="#85C1E9", outline="black")
            #Checking if that coord is in the default _coord_showL
            elif coordinates in default_coord_showL(u_position):
                #recover the id of the error cell
                ercellid=ids_cell.get(str(coordinates))
                #configure the item to its default
                playcanv.itemconfig(ercellid, fill="#D6EAF8", outline="black")
            else:
                #recover the id of the error cell
                ercelid=ids_cell.get(str(coordinates))
                #configure the item to its default
                playcanv.itemconfig(ercelid, fill="white", outline="black")

def caseindex_to_casepx(x_pos:int, y_pos:int)->list[int,int]:
    """Convert Case Index position to Case Pixel position in canva

    Args:
        x_pos (int): Index x
        y_pos (int): Index y

    Returns:
        tuple[int]: (x positon in px, y position in px)
    """
    #Recovering the canva height and width
    canvawidth = playcanv.winfo_reqwidth()
    canvaheight = playcanv.winfo_reqheight()
    return (int((x_pos)*(canvawidth/9)), int((y_pos)*(canvaheight/9)))

def mouse_to_case(x_pos:int, y_pos:int)->tuple[int]:
    """Convert Mouse Position (px) in Canvas to Case index in grid

    Args:
        canva (tk.Canvas): the canva of the binding
        x_pos (int): Position x
        y_pos (int): Position y
    Returns:
        tuple[int]: (x_index, y_index)
    """
    #Recovering the height and width of the canva
    canvawidth = playcanv.winfo_reqwidth()
    canvaheight = playcanv.winfo_reqheight()
    return (int(y_pos//int(canvaheight/9)), int(x_pos//int(canvawidth/9)))

def give_up():
    """Quit the game window
    """
    global new_game_window
    if messagebox.askokcancel("You are quitting !", "Are you sure you want to quit ?"):
        #Clear every data used for the game
        ids_cell.clear()
        ids_pgtxt.clear()
        u_position=None
        u_number=None
        errorcount=0
        errorlabel.config(text=f"{errorcount} errors")
        new_game_window.destroy()
        root.deiconify()

def display_grid():
    """Display Grid on the playcanva

    Args:
        canva (tk.Canvas): The Canva to display grid in it
    """
    global ids_cell
    #Recovering the canva height and width
    canvawidth = playcanv.winfo_reqwidth()
    canvaheight = playcanv.winfo_reqheight()
    #Init the coordinate variable of the cell
    #x for column
    x=0
    #y for line
    y=0
    #creating the pointer of y0 position (line)
    for y0 in range(0,int((8*canvaheight)/9),int(canvaheight/9)):
        #creating the pointer of x0 position (column)
        for x0 in range(0,int((8*canvawidth)/9),int(canvawidth/9)):
            #Set x1 position 
            x1=x0+(canvawidth/9)
            #Set y1 position
            y1=y0+(canvaheight/9)
            #Create the rectangle and set its ID
            cell_id=playcanv.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
            #add the rectangle ID in id dictionary
            ids_cell[str((y,x))]=cell_id
            #update the coordinates
            if x < 8:
                x+=1
            elif x == 8:
                x=0
                y+=1
    #Just For Esthetic
    #create vertical regions lines
    for c in range(int(canvawidth/3), int(canvawidth), int(canvawidth/3)):
        playcanv.create_line(c, 0, c, canvaheight, width=3)
    #create horizontal region lines
    for l in range(int(canvaheight/3), int(canvaheight), int(canvaheight/3)):
        playcanv.create_line(0, l, canvawidth, l, width=3)

def game_window_closed():
    """This function put menu back and destroy newg_window
    """
    global root
    global new_game_window
    global errorlabel
    global errorcount
    global u_position
    global u_number
    global ids_cell
    global ids_pgtxt
    #Re-show the window of menu
    root.deiconify()
    #Clear every data used for the game
    ids_cell.clear()
    ids_pgtxt.clear()
    ids_notes.clear()
    u_position=None
    u_number=None
    errorcount=0
    errorlabel.config(text=f"{errorcount} errors")
    #quit the new game window
    new_game_window.destroy()

#About end of the Game
def endg_quit():
    """Quit the game window at the end of game"""
    #Clear every data used for the game
    ids_cell.clear()
    ids_pgtxt.clear()
    u_position=None
    u_number=None
    errorcount=0
    errorlabel.config(text=f"{errorcount} errors")
    new_game_window.destroy()
    root.deiconify()
    #Re-show the root main menu
    root.deiconify
    #Destroy new_game_window
    new_game_window.destroy

def saveandquit(gridsdkboard: list, difficulty:int, errorcount:int, name:str, timestr:str):
    """Save the grid and quit"""
    #Saving informations
    save_grid(gridsdkboard, difficulty, errorcount, name, timestr)
    #Quit
    endg_quit()

def set_gridname():
    """Set the name of the grid"""
    #Resize the window
    end_window.geometry("300x115")
    #Remove every widget on frame
    congrat.destroy()
    quit_button.destroy()
    save_but.destroy()
    #Updating the window
    end_window.update()
    
    #Create new widgets on window
    lbl=tk.Label(end_window, text="Enter the name you want for the grid", font=("ClearSans", 12, "bold"))
    namentry=tk.Entry(end_window, width=32)
    confirmnands=tk.Button(end_window, text="Confirm and save", font=("ClearSans", 10), command=lambda: (saveandquit(gridl, difficulty, errorcount, namentry.get(), time_str)))
    cancelbut=tk.Button(end_window, text="Cancel", font=("ClearSans", 10), width=8, command=endg_quit)
    
    #Display new widgets
    lbl.grid(row=0, column=0, columnspan=2, padx=10,  pady=5)
    namentry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    confirmnands.grid(row=2, column=0, padx=10, pady=5)
    cancelbut.grid(row=2, column=1, padx=10, pady=5)

def end_game():
    """Set the window of end game"""
    global end_window
    global congrat
    global quit_button
    global save_but
    end_window=tk.Toplevel(new_game_window)
    end_window.geometry("225x75")
    #end_window.resizable(False)
    end_window.resizable(False, False)
    
    #Widget on window
    congrat=tk.Label(end_window, text="Congratulation You Have Win !", font=("ClearSans", 10, "bold"))
    quit_button=tk.Button(end_window, text="Quit",width=8, command=endg_quit)
    save_but=tk.Button(end_window, text="Save Grid", command=set_gridname)
    
    #Display on the window
    congrat.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    quit_button.grid(row=1, column=0, padx=10, pady=5)
    save_but.grid(row=1, column=1, padx=10, pady=5)

#Principal Game Window
def game_window():
    """Create a Sudoku Game Window"""
    global root
    global new_game_window
    global selectbcanv
    global extracanv
    global playcanv
    global u_position
    global u_number
    global gridnp
    global grid
    global gridl
    global newg_frame
    global cList
    global errorlabel
    global timelabel
    global note_mode
    global ebutton
    global sbutton
    global nbutton
    #Iconify the root window
    root.iconify()
    #Creating a new window
    new_game_window=tk.Toplevel(root)
    #Setting New Game Window
    new_game_window.resizable(False,False)
    new_game_window.title("Sudoku Game")
    
    #Frame on New Game Window
    newg_frame=tk.Frame(new_game_window, width=1000, height=750)
    newg_frame.grid()
        
    #Widgets on Frame
    playcanv=tk.Canvas(newg_frame, width=702, height=702, borderwidth=5, relief="sunken")
    selectbcanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="sunken")
    extracanv=tk.Canvas(newg_frame, width=250, height=250, borderwidth=5, relief="ridge")
    
    #Extra Canva Configuration
    extracanv.grid_propagate(False)
    for c in range(3):
        extracanv.grid_columnconfigure(c, weight=1)
    for r in range(4):
        extracanv.grid_rowconfigure(r, weight=1)
    
    #Select Canva Configuration
    selectbcanv.grid_propagate(False)
    for c in range(3):
        selectbcanv.grid_columnconfigure(c, weight=1)
    for r in range(3):
        selectbcanv.grid_rowconfigure(r, weight=1)
    
    #Displaying grid on playgrid
    display_grid()
    
    #create the list of coordinates for clues
    cList=get_values_coord(gridl)
    
    #Create the list containing every values of the grid
    vList=get_values_coord(gridnp.astype(int).tolist())
    #filling the grid with every non-zeros cells
    for coordinate in vList:
        display_in_ugrid(coordinate, gridnp[coordinate[0], coordinate[1]])
    
    #Filling the grid with every notes
    for coordinate in ids_notes:
        for key_number in ids_notes[coordinate]:
            inject_note((int(coordinate[1]), int(coordinate[4])), int(key_number))

    #Binding the playcanv
    playcanv.bind('<ButtonPress-1>', playgridS)
    
    #widgets in Select Canva
    b1=tk.Button(selectbcanv, text="1", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(1))
    b2=tk.Button(selectbcanv, text="2", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(2))
    b3=tk.Button(selectbcanv, text="3", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(3))
    b4=tk.Button(selectbcanv, text="4", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(4))
    b5=tk.Button(selectbcanv, text="5", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(5))
    b6=tk.Button(selectbcanv, text="6", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(6))
    b7=tk.Button(selectbcanv, text="7", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(7))
    b8=tk.Button(selectbcanv, text="8", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(8))
    b9=tk.Button(selectbcanv, text="9", font=("ClearSans"), relief="groove", padx=15, pady=10, command=lambda: usern_selection(9))
    
    #Display on Select Canva Frame
    b1.grid(row=0, column=0)
    b2.grid(row=0, column=1)
    b3.grid(row=0, column=2)
    b4.grid(row=1, column=0)
    b5.grid(row=1, column=1)
    b6.grid(row=1, column=2)
    b7.grid(row=2, column=0)
    b8.grid(row=2, column=1)
    b9.grid(row=2, column=2)
    
    #Widgets in Extra Canva
    #The boolean variable for the checkbutton
    note_mode=tk.BooleanVar()
    #Checkbutton creation and parameters
    nbutton=tk.Checkbutton(extracanv, text="Note Mode", font=("CleanSans",10), relief="groove", variable=note_mode)
    #Save button creation and parameters
    sbutton=tk.Button(extracanv, text="Save State", font=("CleanSans", 10), relief="groove", command=lambda:(save_state(gridl, gridnp, errorcount, ids_pgtxt, ids_cell, ids_notes, coorderrorL, minutes, seconds, difficulty)))
    #Erase button creation and parameters
    ebutton=tk.Button(extracanv, text="Erase", font=("CleanSans", 10), relief="groove", command=lambda:erase_value(u_position))
    #Give Up button creation and parameters
    qbutton=tk.Button(extracanv, text="Give up", font=("CleanSans", 10), relief="groove", command=give_up)
    #Display the Name of the grid
    namelabel=tk.Label(extracanv, text=gridname, font=("CleanSans", 16, "bold"))
    #Display the level of difficulty
    difficlabel=tk.Label(extracanv, text=d_name, font=("CleanSans", 14, "bold"))
    #Display the Time
    timelabel=tk.Label(extracanv, text=time_str, font=("ClearSans", 10, "bold"))
    #Display the number of errors
    errorlabel=tk.Label(extracanv, text=f"{errorcount} errors", font=("CleanSans", 10, "bold"))
    
    #Updating the time display in background
    # Start the time counter function in a separate thread (Every code lines in link with time has been made by an AI)
    time_counter_thread = threading.Thread(target=time_counter)
    time_counter_thread.start()
    
    #Display on Extra Canva
    ebutton.grid(row=3, column=0)
    nbutton.grid(row=3, column=1)
    sbutton.grid(row=3, column=2)
    qbutton.grid(row=0, column=0)
    errorlabel.grid(row=0, column=1)
    timelabel.grid(row=0, column=2)
    namelabel.grid(row=1, column=0, columnspan=3)
    difficlabel.grid(row=2, column=0, columnspan=3)
    
    #Display on Frame
    playcanv.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
    selectbcanv.grid(row=1, column=1, padx=10, pady=10)
    extracanv.grid(row=0, column=1, padx=10, pady=10)
    
    #When game_window is closed
    new_game_window.protocol("WM_DELETE_WINDOW", game_window_closed)

#Root
root=tk.Tk()
root.title("Sudoku Game ")
root.resizable(False, False)

#First Frame on root
menuframe=tk.Frame(root, width=250, height=200)
menuframe.grid_propagate(False)
for c in range(3):
    menuframe.grid_columnconfigure(c, weight=1)
for r in range(5):
    menuframe.grid_rowconfigure(r, weight=1)
menuframe.grid()

#Widgets
#Widgets on menu frame
titlemenu=tk.Label(menuframe, text="Sudoku Game ", font=("tahoma", 14, "bold"), anchor="center")
newgb=tk.Button(menuframe, text="New Game", padx=5, pady=5, command=new_game)
loadgb=tk.Button(menuframe, text="Load Game", padx=5, pady=5, command=load_game)
playoldb=tk.Button(menuframe, text="Play Old Ones", padx=5, pady=5, command= lambda : play_old_menu("savesfiles/save_grids.json"))
quitb=tk.Button(menuframe, text="Quit", command=root.quit, padx=5, pady=5)
menuloc=tk.Label(menuframe, text="Menu", font=("tahoma", 8, "italic"))
msgbox=tk.Message()

#Display
#Widgets on menu frame
titlemenu.grid(row=0, column=1, pady=5)
newgb.grid(row=1, column=1, pady=5)
loadgb.grid(row=2 ,column=1, pady=5)
playoldb.grid(row=3, column=1, pady=5)
quitb.grid(row=4, column=0, padx=10, pady=10)
menuloc.grid(row=4, column=2, sticky="SE")
root.mainloop()