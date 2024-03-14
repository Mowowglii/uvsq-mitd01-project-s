import tkinter as tk

#Functions
def newg_closed():
    """This function is used when newg_window is closed, it put menu back and destroy newg_window
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
    new_game_window.title("Sudoku New Grid")

    #Frame on New Game Window
    newg_frame=tk.Frame(new_game_window, width=1000, height=750)
    newg_frame.grid_propagate(False)
    newg_frame.grid()

    #Widgets on Frame
    playcanv=tk.Canvas(newg_frame, width=702, height=702, borderwidth=5, relief="sunken")
    selectbcanv=tk.Canvas(newg_frame,width=225,height=225,borderwidth=5, relief="sunken")
    infocanv=tk.Canvas(newg_frame, width=225, height=225, borderwidth=5, relief="ridge")
    
    #Select Canva Configuration
    selectbcanv.grid_propagate(False)
    for c in range(3):
        selectbcanv.grid_columnconfigure(c, weight=1)
    for r in range(3):
        selectbcanv.grid_rowconfigure(r, weight=1)
    
    #Widgets on Select Canvas
    button1=tk.Button(selectbcanv, text="1", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button2=tk.Button(selectbcanv, text="2", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button3=tk.Button(selectbcanv, text="3", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button4=tk.Button(selectbcanv, text="4", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button5=tk.Button(selectbcanv, text="5", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button6=tk.Button(selectbcanv, text="6", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button7=tk.Button(selectbcanv, text="7", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button8=tk.Button(selectbcanv, text="8", font=("ClearSans"), padx=5, pady=5, relief="groove")
    button9=tk.Button(selectbcanv, text="9", font=("ClearSans"), padx=5, pady=5, relief="groove")
    
    #Display on Select Canvas
    button1.grid(row=0, column=0, padx=5, pady=5)
    button2.grid(row=0, column=1, padx=5, pady=5)
    button3.grid(row=0, column=2, padx=5, pady=5)
    button4.grid(row=1, column=0, padx=5, pady=5)
    button5.grid(row=1, column=1, padx=5, pady=5)
    button6.grid(row=1, column=2, padx=5, pady=5)
    button7.grid(row=2, column=0, padx=5, pady=5)
    button8.grid(row=2, column=1, padx=5, pady=5)
    button9.grid(row=2, column=2, padx=5, pady=5)
    
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