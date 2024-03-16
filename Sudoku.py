import tkinter as tk

#Global Variables
usernumber=0

#Game Functions

#Display or GUI Functions
def caseindex_to_casepx(x_pos:int, y_pos:int, row:int, column:int, canwidth:int, canheight:int, canborder=0)->list[int,int]:
    """Convert Case Index position to Case Pixel position in canva

    Args:
        x_pos (int): Index x
        y_pos (int): Index y
        row (int): Row of the canva
        column (int): Column of the canva
        canwidth (int): Width of canva
        canheight (int): Height of canva
        canborder (int, optional): Canva border. Defaults to 0.

    Returns:
        list[int,int]: [x positon in px, y position in px]
    """
    return [int(x_pos*((canwidth+canborder)/column)), int(y_pos*((canheight+canborder)/row))]

def mouse_to_case(x_pos:int, y_pos:int, row:int, column:int, canwidth:int, canheight:int, canborder=0)->list[int,int]:
    """Convert Mouse Pix Position in Canvas to Case index in grid

    Args:
        x_pos (int): Position x
        y_pos (int): Position y
        row (int): Number of row
        column (int): Number of column
        canwidth (int): Width of Canva
        canheight (int): Height of Canva
        canborder (int, optional): Canva border thickness. Defaults to 0.

    Returns:
        list[int,int]: [x_index, y_index]
    """
    return [int(x_pos//((canwidth+canborder)/column)), int(y_pos//((canheight+canborder)/row))]

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

def playgridS(event=tk.Event):
    """The goal of this function is to do the link between the display and the empty grid

    Args:
        event (tk.Event, optional): The event generated (here is click)
    """
    print(f'Click on Playgrid : {mouse_to_case(event.x, event.y, 9, 9, 702, 702, 7)}')

def usern_selection(number:int):
    """Set User Selected number

    Args:
        number (int): The chosen number
    """
    global usernumber
    usernumber=number
    print(usernumber)
    
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
    global usernumber
    root.iconify()
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

    #Playcanv configuration
    playcanv.grid_propagate(False)
    playcanv.grid_propagate(False)
    for c in range(9):
        playcanv.grid_columnconfigure(c, weight=1)
    for r in range(9):
        playcanv.grid_rowconfigure(r, weight=1)
    
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
    
    #Widget on Play Canv
    gridframe=tk.Frame(playcanv, width=702, height=702, bg="")
    
    #Display on Play Canv
    gridframe.grid(row=0, column=0, columnspan=9, rowspan=9)
    
    #Binding Play Canva Grid
    gridframe.bind('<ButtonPress-1>', playgridS)
    
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
    ebutton=tk.Button(extracanv, text="Erase", font=("CleanSans", 10), relief="groove")
    qbutton=tk.Button(extracanv, text="Give up", font=("CleanSans", 10), relief="groove", command=new_game_window.destroy)
    namelabel=tk.Label(extracanv, text="Grid Number", font=("CleanSans", 16, "bold"))
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