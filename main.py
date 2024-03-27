#Imports
from sdklibmyfunc import *
import tkinter as tk

#Global Dictionary or List
#Setting a dictionary to store the IDs of play grid texts
ids_pgtxt={}

#Global Variables
u_position=None
u_number=None

#Link beetween GUI and Game functions

def playgridS(event=tk.Event):
    """The goal of this function is to do the link between the display and the empty grid

    Args:
        event (tk.Event, optional): The event generated (here is click)
    """
    global u_position
    u_position=mouse_to_case(event.x, event.y, 9, 9, 702, 702)

def usern_selection(number:int):
    """Set User Selected number

    Args:
        number (int): The chosen number
    """
    global u_number
    #Setting the global variable of user_number
    u_number=number
    #Injecting the value in board
    inject(board, u_position, u_number)
    #Displaying in the user interface
    display_in_ugrid(u_position, u_number)

#Display or GUI Functions

def display_in_ugrid(coordinate:tuple[int], value:int):
    """Dislpay numbers on the grid

    Args:
        coordinate (tuple[int]): position in grid of the number (x_position, y_position)
        value (int): the value to enter inside of the grid
    """
    #Getting x position of text
    postxt_y=(caseindex_to_casepx(coordinate[0], coordinate[1], 9, 9, 702, 702, 7)[0])-(caseindex_to_casepx(0, 0, 9, 9, 702, 702, 7)[0]/2)+5
    postxt_x=(caseindex_to_casepx(coordinate[0], coordinate[1], 9, 9, 702, 702, 7)[1])-(caseindex_to_casepx(0, 0, 9, 9, 702, 702, 7)[1]/2)+5
    #creating text in canva to diplay the number and assign all created text on play grid an ID
    ctxt_id=playcanv.create_text(postxt_x, postxt_y, text=str(value), font=("ClearSans", 20, "bold"), anchor=tk.CENTER)
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
        erase(board, coordinate)
    #Erase in user interface
        #recover the id of the item
        txt_id = ids_pgtxt.get(str(coordinate))
        #erase in user interface
        playcanv.type(txt_id)
        playcanv.delete(txt_id)

def caseindex_to_casepx(x_pos:int, y_pos:int, row:int, column:int, canwidth:int, canheight:int, canborder=0)->list[int,int]:
    """Convert Case Index position to Case Pixel position in canva

    Args:
        x_pos (int): Index x
        y_pos (int): Index y
        row (int): Number of row of the canva
        column (int): Number of column of the canva
        canwidth (int): Width of canva
        canheight (int): Height of canva
        canborder (int, optional): Canva border. Defaults to 0.

    Returns:
        tuple[int]: (x positon in px, y position in px)
    """
    return (int((x_pos+1)*((canwidth+canborder)/column)), int((y_pos+1)*((canheight+canborder)/row)))

def mouse_to_case(x_pos:int, y_pos:int, row:int, column:int, canwidth:int, canheight:int, canborder=0)->tuple[int]:
    """Convert Mouse Position (px) in Canvas to Case index in grid

    Args:
        x_pos (int): Position x
        y_pos (int): Position y
        row (int): Number of row
        column (int): Number of column
        canwidth (int): Width of Canva
        canheight (int): Height of Canva
        canborder (int, optional): Canva border thickness. Defaults to 0.

    Returns:
        tuple[int]: (x_index, y_index)
    """
    return (int(y_pos//((canheight+canborder)/row)), int(x_pos//((canwidth+canborder)/column)))

def slicecanvas(canva:tk.Canvas,rows:int,column:int,canvawidth:int,canvaheight:int):
    """Slice a Canva into rows x column parcels

    Args:
        canva (tk.Canvas): The Canva to slice
        rows (int): number of row we want
        column (int): number of column we want
        canvawidth (int): Canva width
        canvaheight (int): Canva height
    """
    Lparcel=canvawidth//column
    Hparcel=canvaheight//rows
    for r in range(rows):
        for c in range(column):
            x1=c*Lparcel+7
            y1=r*Hparcel+7
            if (x1==(canvawidth/3)+7 and y1==(canvaheight/3)+7) or (x1==2*(canvawidth/3)+7 and y1==2*(canvaheight/3)+7):
                canva.create_line(x1, 7, x1, canvaheight+7, width=3)
                canva.create_line(7,y1,canvawidth+7,y1, width=3)
            else:
                canva.create_line(x1, 7, x1, canvaheight+7)
                canva.create_line(7,y1,canvawidth+7,y1)

def game_window_closed():
    """This function put menu back and destroy newg_window
    """
    global root
    global new_game_window
    root.deiconify()
    new_game_window.destroy()

def game_window():
    """Create a Sudoku Game Window"""
    global root
    global new_game_window
    global selectbcanv
    global extracanv
    global playcanv
    global u_position
    global u_number
    global board
    global newg_frame
    global cList
    root.iconify()
#Game Part
    #Generate a sudoku grid
    grid=generate_grid(0.1)
    #Setting the grid of interaction
    board=manip_grid(grid)
#Display Part
    new_game_window=tk.Toplevel(root)
    #New Game Window
    new_game_window.resizable(False,False)
    new_game_window.title("Sudoku Game")

    #Frame on New Game Window
    newg_frame=tk.Frame(new_game_window, width=1000, height=750)
    newg_frame.grid_propagate(False)
    newg_frame.grid()
    
    #Widgets on Frame
    playcanv=tk.Canvas(newg_frame, width=702, height=702, borderwidth=5, relief="sunken")
    selectbcanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="sunken")
    extracanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="ridge")
    
    #Extra Canva Configuration
    extracanv.grid_propagate(False)
    extracanv.grid_propagate(False)
    for c in range(3):
        extracanv.grid_columnconfigure(c, weight=1)
    for r in range(4):
        extracanv.grid_rowconfigure(r, weight=1)
    
    #Select Canva Configuration
    selectbcanv.grid_propagate(False)
    selectbcanv.grid_propagate(False)
    for c in range(3):
        selectbcanv.grid_columnconfigure(c, weight=1)
    for r in range(3):
        selectbcanv.grid_rowconfigure(r, weight=1)
    
    #Slicing Play Canv
    slicecanvas(playcanv, 9, 9, 702, 702)

    #create the list of coordinates
    cList=get_values_coord(board)
    #filling the grid with the clues (to write)
    for element in cList:
        display_in_ugrid(element, board[element[0]][element[1]])

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
    nbutton=tk.Checkbutton(extracanv, text="Note Mode", font=("CleanSans",10), relief="groove")
    sbutton=tk.Button(extracanv, text="Save", font=("CleanSans", 10), relief="groove")
    ebutton=tk.Button(extracanv, text="Erase", font=("CleanSans", 10), relief="groove", command=lambda:erase_value(u_position))
    qbutton=tk.Button(extracanv, text="Give up", font=("CleanSans", 10), relief="groove", command=new_game_window.destroy)
    namelabel=tk.Label(extracanv, text="New Grid", font=("CleanSans", 16, "bold"))
    difficlabel=tk.Label(extracanv, text="Difficulty", font=("CleanSans", 14, "bold"))
    timelabel=tk.Label(extracanv, text="00:00", font=("ClearSans", 10))
    errorlabel=tk.Label(extracanv, text="x errors", font=("CleanSans", 10))
    
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
    playcanv.grid(row=0, column=0, rowspan=2, padx=10,pady=10)
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
newgb=tk.Button(menuframe, text="New Game", padx=5, pady=5, command=game_window)
loadgb=tk.Button(menuframe, text="Load Game", padx=5, pady=5)
playoldb=tk.Button(menuframe, text="Play Old Ones", padx=5, pady=5)
quitb=tk.Button(menuframe, text="Quit", command=root.quit, padx=5, pady=5)
menuloc=tk.Label(menuframe, text="Menu", font=("tahoma", 8, "italic"))

#Display
#Widgets on menu frame
titlemenu.grid(row=0, column=1, pady=5)
newgb.grid(row=1, column=1, pady=5)
loadgb.grid(row=2 ,column=1, pady=5)
playoldb.grid(row=3, column=1, pady=5)
quitb.grid(row=4, column=0, padx=10, pady=10)
menuloc.grid(row=4, column=2, sticky="SE")

root.mainloop()