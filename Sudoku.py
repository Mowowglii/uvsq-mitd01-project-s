import tkinter as tk

#Functions
def px_to_index(x_pos:int, y_pos:int, row:int, column:int, canwidth:int, canheight:int, canborder=0)->list[int,int]:
    """Convert Pix Position in Canvas to index in grid

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
    print(f'Click on Playgrid : {px_to_index(event.x, event.y, 9, 9, 702, 702, 7)}')
    
def selectcanvS(event=tk.Event):
    """The goal of this function is to lock user number selection from clicking in the selection grid

    Args:
        event (tk.Event, optional): The event generated (here is click)
    """
    print(f'Click in Selectgrid : {px_to_index(event.x, event.y, 3, 3, 225, 225, 7)}')
    
def newg_closed():
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
    
    #Slicing Play Canva for Grid Display
    slicecanvas(playcanv, 9, 9, 702, 702)
    
    #Binding Play Canva Grid
    playcanv.bind('<ButtonPress-1>', playgridS)
        
    #Slicing Select Canva
    slicecanvas(selectbcanv, 3, 3, 225, 225)
    
    #Binding Select Canva Grid
    selectbcanv.bind('<ButtonPress-1>', selectcanvS)
    
    #widgets in Select Canva
    label1=tk.Label(selectbcanv, text="1", font=("ClearSans"))
    label2=tk.Label(selectbcanv, text="2", font=("ClearSans"))
    label3=tk.Label(selectbcanv, text="3", font=("ClearSans"))
    label4=tk.Label(selectbcanv, text="4", font=("ClearSans"))
    label5=tk.Label(selectbcanv, text="5", font=("ClearSans"))
    label6=tk.Label(selectbcanv, text="6", font=("ClearSans"))
    label7=tk.Label(selectbcanv, text="7", font=("ClearSans"))
    label8=tk.Label(selectbcanv, text="8", font=("ClearSans"))
    label9=tk.Label(selectbcanv, text="9", font=("ClearSans"))
    
    #Display on Select Canva Frame
    label1.grid(row=0, column=0)
    label2.grid(row=0, column=1)
    label3.grid(row=0, column=2)
    label4.grid(row=1, column=0)
    label5.grid(row=1, column=1)
    label6.grid(row=1, column=2)
    label7.grid(row=2, column=0)
    label8.grid(row=2, column=1)
    label9.grid(row=2, column=2)
    
    #Widgets in Extra Canva
    nbutton=tk.Checkbutton(extracanv, text="Note Mode", font=("CleanSans",10), relief="groove")
    sbutton=tk.Button(extracanv, text="Save", font=("CleanSans", 10), relief="groove")
    ebutton=tk.Button(extracanv, text="Erase", font=("CleanSans", 10), relief="groove")
    qbutton=tk.Button(extracanv, text="Give up", font=("CleanSans", 10), relief="groove", command=new_game_window.destroy)
    namelabel=tk.Label(extracanv, text="Grid Number", font=("CleanSans", 16, "bold"))
    difficlabel=tk.Label(extracanv, text="Difficulty", font=("CleanSans", 14, "bold"))
    timelabel=tk.Label(extracanv, text="Timer", font=("ClearSans", 10))
    errorlabel=tk.Label(extracanv, text="Error n°", font=("CleanSans", 10))
    
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
    
    #When newg_window is closed
    new_game_window.protocol("WM_DELETE_WINDOW", newg_closed)

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