#Imports
from sdklibmyfunc import *
import tkinter as tk

#Global Dictionary or List
#Setting a dictionary to store the IDs of play grid texts
ids_pgtxt={}
ids_cell={}
#Game global Variables
u_position=None
u_number=None

#Link beetween GUI and Game functions

def playgridS(event=tk.Event):
    """The goal of this function is to do the link between the display and the empty grid

    Args:
        event (tk.Event, optional): The event generated (here is click)
    """
    global u_position
    u_position=mouse_to_case(event.x, event.y)

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
def highlight_cell(coordinate:tuple[int]):
    """Highlight a cell in the playgrid

    Args:
        coordinate (tuple[int]): the coordinate of the cell
    """
    

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
        erase(board, coordinate)
    #Erase in user interface
        #recover the id of the item
        txt_id = ids_pgtxt.get(str(coordinate))
        #erase in user interface
        playcanv.type(txt_id)
        playcanv.delete(txt_id)

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
            ids_cell[(y,x)]=cell_id
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
    grid=generate_grid(0.9)
    #Setting the grid of interaction
    board=manip_grid(grid)
#Display Part
    new_game_window=tk.Toplevel(root)
    #New Game Window
    new_game_window.resizable(False,False)
    new_game_window.title("Sudoku Game")

    #Frame on New Game Window
    newg_frame=tk.Frame(new_game_window, width=1000, height=750)
    #newg_frame.grid_propagate(False)
    newg_frame.grid()
    
    #Widgets on Frame
    playcanv=tk.Canvas(newg_frame, width=702, height=702, borderwidth=5, relief="sunken")
    selectbcanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="sunken")
    extracanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="ridge")
    
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