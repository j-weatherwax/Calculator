from tkinter import *
from math import sqrt

class helperCommands():
    def __init__(self, gui):
        self.gui = gui

        #String to be displayed to opBox
        self.userString = ""

        #String to be evaluated
        self.functionString = ""

        self.math = ""
        self.result = ""

        self.opList = ['.', '+', '-', '×', '÷', '=']

    #function to clear contents of textBox
    def clear(self):
        self.gui.textBox.delete(0, END)
        return

    #same as clear but inserts a 0 in the textBox
    def clear_entry(self):
        textVal = self.gui.textBox.get()
        
        #prevents clearing info from self.userString and self.functionString if textBox = 0  or is empty
        if textVal == "0" or "":
            return
        n = len(textVal)
        self.userString = self.userString[:-n]
        self.gui.opBox.config(text = self.userString)
        self.functionString = self.functionString[:-n]
        self.clear()
        self.gui.textBox.insert("end", "0")
        return

    def clear_all(self):
        self.clear()
        self.first_num = None
        self.userString = ""
        self.gui.opBox.config(text = self.userString)
        self.functionString = ""
        self.gui.textBox.insert("end", "0")
        return

    def back(self):
        textVal = self.gui.textBox.get()
        self.clear()
        self.gui.textBox.insert("end", textVal[:-1])
        self.userString = self.userString[:-1]
        self.gui.opBox.config(text = self.userString)
        self.functionString = self.functionString[:-1]
        return

    def funcKey(self, func):
        textVal = self.gui.textBox.get()

        #Remove num to be replaced with func(num)
        #If false: 2+ -> 2+func(2)
        if self.userString[-1].isdigit():
            self.clear_entry()
        
        if func == "perc":
            temp = float(textVal) / 100
            funcTempString = f"{temp}"
        if func == "inv":
            temp = 1/float(textVal)
            funcTempString = f"inv({textVal})"
        if func == "sqr":
            temp = float(textVal)**2
            funcTempString = f"sqr({textVal})"
        if func == "sqrt":
            temp = sqrt(float(textVal))
            funcTempString = f"sqrt({textVal})"
        if func == "negate":
            temp = -1*float(textVal)
            funcTempString = f"negate({textVal})"


        if "=" in self.userString:
            self.userString = funcTempString
        else:
            self.userString += funcTempString


        self.gui.opBox.config(text = self.userString)
        #adds temp to functionString
        self.functionString += str(temp)
        self.clear()
        self.gui.textBox.insert("end", f"{temp}")#:.0f}")
        return

    def click(self, i):
        #if operation in oplist already exists in the user string,
        #don't allow button to be pressed
        if len(self.userString) > 0  and self.userString[-1] == i and i in self.opList:
            return                

        #fix mult and div for eval
        funcVal = i
        if i == "×":
            funcVal = "*"
        elif i == "÷":
            funcVal = "/"
        self.functionString += str(funcVal)

        #Writes to opBox
        if "=" in self.userString and i != "=":
            #Set userString to result from equation
            self.userString = str(f"{self.result:.0f}")
            #add operation to userString
            self.userString += str(i)
            self.functionString = str(self.result)
            self.functionString += str(funcVal)
            self.gui.opBox.config(text = self.userString)
        else:
            #Overwrites 0 when initial number is clicked
            if self.userString  == "0" and i != ".":
                self.userString = str(i)
            else:
                self.userString += str(i)
            self.gui.opBox.config(text = self.userString)

        if str(i).isdigit() or i == ".":
            #Allows number to stay in textBox until another number is clicked
            for operation in self.opList:
                if operation in self.userString and operation != ".":
                    self.clear()
            textVal = self.gui.textBox.get()

            #If textbox is just 0, don't add more 0's
            if textVal == "0":
                textVal = ""
            #Keep 0 if i is a decimal point
            if textVal == "" and i == ".":
                textVal = "0"
                self.userString = "0."
                self.gui.opBox.config(text = self.userString)
                #self.functionString = "0."
            self.clear()
            self.gui.textBox.insert("end", textVal + str(i))

        #resets math flag since i should be a number or . if it reaches this
        self.math = FALSE

    def firstNumGet(self):
        if "=" in self.userString:
            return
        first = self.gui.textBox.get()
        self.first_num = float(first)
        
    #Sets operations for addition, subtraction, multiplication, and division
    def arith(self, op):
        self.firstNumGet()
        self.math = TRUE
        self.click(op)

    def equal(self):
        if "=" in self.userString or self.userString == "":
            return

        self.result = eval(self.functionString)
        self.clear()
        self.gui.textBox.insert("end", f"{self.result:.0f}")
        self.first_num = self.result
        self.math = FALSE
        self.click("=")