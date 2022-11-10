from coloredit import *
from commands import *


#darkens button color on hover and reverts color on leave
class hover():
    def __init__(self, tempbutton, hoverColor, buttonColor):
        self.tempbutton = tempbutton
        self.hoverColor = hoverColor
        self.buttonColor = buttonColor
        self.tempbutton.bind("<Enter>", self.on_enter)
        self.tempbutton.bind("<Leave>", self.on_leave)


    #When hovering over button, darken the color of the button
    def on_enter(self, event):
        self.tempbutton.config(background=self.hoverColor)
    

    #When mouse stops hovering over button, revert back to button's original color
    def on_leave(self, event):
        self.tempbutton.config(background=self.buttonColor)

#button grid
class buttonGrid():
    def __init__(self, master, gui, c):
        self.master = master
        self.gui = gui
        self.buttonText = [['%', 'CE', 'C', 'back'], ['1/x', 'x²', '√', '÷'], ['7', '8', '9', '×'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['±', '0', '.', '=']]
        self.buttonCommands = [[lambda: c.funcKey("perc"), c.clear_entry, c.clear_all, c.back], 
                                [lambda: c.funcKey("inv"), lambda: c.funcKey("sqr"), lambda: c.funcKey("sqrt"), lambda: c.arith('÷')], 
                                [lambda: c.click(7), lambda: c.click(8), lambda: c.click(9), lambda: c.arith('×')], 
                                [lambda: c.click(4), lambda: c.click(5), lambda: c.click(6), lambda: c.arith('-')], 
                                [lambda: c.click(1), lambda: c.click(2), lambda: c.click(3), lambda: c.arith('+')],
                                [lambda: c.funcKey("negate"), lambda: c.click(0), lambda: c.click("."), c.equal]]

        self.make_buttons()
    

    def make_buttons(self):
        for row in range(len(self.buttonText)):
            for col in range(len(self.buttonText[row])):
                i = self.buttonText[row][col]
                com = self.buttonCommands[row][col]
                #Set colors for number buttons
                buttonColor = "#f2f2f2"
                #gFunction button color
                if row < 2 or col > 2:
                    buttonColor = "#d8d8d8"
                #equal button color
                if row == 5 and col == 3:
                    buttonColor = "#72a2c8"
                tempButton = Button(self.master,
                                    text=i,
                                    relief="flat", 
                                    bg = buttonColor, 
                                    bd = 0, 
                                    width=4,
                                    activebackground = make_darker(buttonColor, .75), 
                                    font=('Segoe', 14), 
                                    padx=12, 
                                    pady=6, 
                                    command=com)
                tempButton.grid(row = row, column=col, padx=1, pady=1, sticky = EW)
                hover(tempButton, make_darker(buttonColor, .9), buttonColor)
