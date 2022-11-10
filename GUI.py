from tkinter import *
import tksvg
from button import buttonGrid, hover
from coloredit import *
from commands import *


class GUI():
    def __init__(self):
        # create window object
        self.window = self.initialize_window()
        # create all the GUI components (Buttons, text, etc...)
        self.initialize_components()
        

    def initialize_window(self):
        window = Tk()
        window.title("Calculator")
        window.geometry('307x500') #325x500
        window.config(background="silver")
        window.resizable(False, False)
        return window


    def initialize_components(self):
        #Initiaize the label frame
        self.calcLabelFrame=Frame(width=0, background="#c0c0c0")#window, width=325, fg="green")
        self.calcLabelFrame.grid(row = 0, column = 0, sticky = W)
        self.labelImg = tksvg.SvgImage(master=self.calcLabelFrame, file="./svg/list.svg", gamma = 1)
        self.listButton = Button(self.calcLabelFrame, 
                    relief="flat", 
                    height = 20, 
                    width = 20, 
                    bd = 0, 
                    background="#c0c0c0", 
                    activebackground = make_darker("#c0c0c0", .75), 
                    foreground = "black", 
                    image=self.labelImg)
        hover(self.listButton, make_darker("#c0c0c0", .9), "#c0c0c0")
        self.listButton.grid(row=0, column=0, ipadx = 5, ipady = 5)

        #Standard Calculator label
        calcLabel = Label(self.calcLabelFrame, text = "Standard", background="#c0c0c0", font=("Segoe Medium", 14))
        #Places Standard Calculator label next to menu list button
        calcLabel.grid(row=0, column=1)

        #Initialize operation frame and box
        self.opFrame=Frame(self.window, width=0)
        self.opFrame.grid(row = 1, column = 0, pady=(0,5), sticky=W)
        self.opBox = Label(self.opFrame, bg="silver", font=('Segoe', 14))
        self.opBox.pack(side=LEFT)

        #Initialize text entry frame and box
        self.textFrame=Frame(self.window, width=0)
        self.textFrame.grid(row = 3, column = 0, columnspan=1, pady=(0,20))
        self.textBox = Entry(self.textFrame, relief="flat", bg="silver", font=('Segoe', 40))
        self.textBox.insert("end", "0")
        self.textBox.pack(side=LEFT, fill="both", expand=True, padx=0, pady=0)
        
        #Set frame for calculator buttons
        self.buttonFrame = Frame(padx=5, background="silver")
        self.buttonFrame.grid(row = 5, column = 0, columnspan=2, sticky=EW)
        
        #Get commands for each button
        self.commands = helperCommands(self)
        #Initialize buttons
        buttonGrid(self.buttonFrame, self, self.commands)


    def start(self):
        self.window.mainloop()