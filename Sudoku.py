import tkinter as tk

#Functions
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
    parcelmatrix=[]
    for r in range(rows):
        for c in range(column):
            x1=c*Lparcel+7
            y1=r*Hparcel+7
            x2=x1+Lparcel
            y2=y1+Hparcel
            parcel_id=canva.create_rectangle(x1, y1, x2, y2, outline="black")
            parcelmatrix.append(parcel_id)
    return parcelmatrix

def newg_closed():
    """This function put menu back and destroy newg_window
    """
    global root
    global new_game_window
    root.deiconify()
    new_game_window.destroy()

def newg_window():
    """Create a new window from new game button
    """
    global root
    global new_game_window
    root.iconify()
    new_game_window=tk.Toplevel(root)
    #New Game Window
    new_game_window.resizable(False,False)
    new_game_window.title("Sudoku New Game")

    #Frame on New Game Window
    newg_frame=tk.Frame(new_game_window, width=1000, height=750)
    newg_frame.grid_propagate(False)
    newg_frame.grid()

    #Widgets on Frame
    playcanv=tk.Canvas(newg_frame, width=702, height=702, borderwidth=5, relief="sunken")
    selectbcanv=tk.Canvas(newg_frame,width=225,height=225,borderwidth=5, relief="sunken")
    infocanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="ridge")
    
    #Slicing Play Canva for Grid Display
    playitem=slicecanvas(playcanv, 9, 9, 702, 702)
    for l in range(1,3):
        for h in range(1,3):
            playcanv.create_line(l*(702/3)+7,7,l*(702/3)+7,709,width=3)
            playcanv.create_line(7,h*(702/3)+7,709,h*(702/3)+7,width=3)
    
    #Select Canva Configuration
    selectbcanv.grid_propagate(False)
    for c in range(3):
        selectbcanv.grid_columnconfigure(c, weight=1)
    for r in range(3):
        selectbcanv.grid_rowconfigure(r, weight=1)
    
    #Slicing Select Canva
    selectcanvitem=slicecanvas(selectbcanv, 3, 3, 225, 225)
    
    #Display on Frame
    playcanv.grid(row=0, column=0, rowspan=2, padx=10,pady=10)
    selectbcanv.grid(row=1, column=1, padx=10, pady=10)
    infocanv.grid(row=0, column=1, padx=10, pady=10)
    
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
newgb=tk.Button(menuframe, text="New Game", padx=5, pady=5, command=newg_window)
loadgb=tk.Button(menuframe, text="Load Game", padx=5, pady=5)
playoldb=tk.Button(menuframe, text="Play Old Ones", padx=5, pady=5)
quitb=tk.Button(menuframe, text="Quit", command=root.destroy, padx=5, pady=5)
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