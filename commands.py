from decimal import *
from math import sqrt
from tkinter import *

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

    #If backspace is pressed, remove last character from userString and functionString
    def back(self):
        textVal = self.gui.textBox.get()
        #if last character is digit, delete from textbox also
        if len(textVal) > 0:
            if all(ar_op not in self.userString for ar_op in self.opList[1:5]):
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
            temp = Decimal(textVal) / 100
            funcTempString = f"{temp}"
        if func == "inv":
            temp = 1/Decimal(textVal)
            funcTempString = f"inv({textVal})"
        if func == "sqr":
            temp = Decimal(textVal)**2
            funcTempString = f"sqr({textVal})"
        if func == "sqrt":
            temp = sqrt(Decimal(textVal))
            funcTempString = f"sqrt({textVal})"
        if func == "negate":
            temp = -1*Decimal(textVal)
            funcTempString = f"negate({textVal})"


        #If no arithmetic operators are in the opBox, replace the previous funcKey command from the userString
        if any(ar_op in self.userString for ar_op in self.opList[1:5]):
            self.userString += funcTempString
        else:
            self.userString = funcTempString
            #removes previous answer from the function string to be evaluated
            n = len(textVal)
            self.functionString = self.functionString[:-n]


        self.gui.opBox.config(text = self.userString)
        #adds temp to functionString
        self.functionString += str(temp)
        self.clear()
        self.gui.textBox.insert("end", f"{temp}")
        return


    def funcOpFix(self, i):
        #fix multiplication and division operators for eval function
        funcVal = i
        if i == "×":
            funcVal = "*"
        elif i == "÷":
            funcVal = "/"
        return funcVal

    def click(self, i):
        #if operation in oplist already exists in the user string,
        #don't allow button to be pressed
        if len(self.userString) > 0  and self.userString[-1] == i and i in self.opList:
            return                

        #prevents user from typing 0 where there are no other entries in the userString. Ensures errors do not occur with decimal handling
        if len(self.userString) == 0 and str(i) == "0":
            return

        #prevents numbers from being placed after funcKey without an arithmetic operation
        if "(" in self.userString and str(i).isdigit() and all(ar_op not in self.userString for ar_op in self.opList[1:5]):
            return

        #If user presses different arithmetic operator after one already exists in the userString, replace the operator with the newly clicked operation
        #Ex. 3+ becomes 3- when - is clicked
        if len(self.userString) > 0 and self.userString[-1] in self.opList[1:5] and i in self.opList[1:5]:
            self.userString = self.userString[:-1] + i
            funcVal = self.funcOpFix(i)
            self.functionString = self.functionString[:-1] + funcVal
            self.gui.opBox.config(text = self.userString)
            return

        funcVal = self.funcOpFix(i)
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
            for operation in self.opList[1:]:
                if operation in self.userString:
                    self.clear()
            textVal = self.gui.textBox.get()


            #If textbox is just 0, don't add more 0's
            if textVal == "0":
                textVal = ""
            #Keep 0 if i is a decimal point
            if textVal == "" and i == ".":
                textVal = "0"
                #deletes . from click and add preceding 0 to decimal
                self.userString = self.userString[:-1] + "0."
                self.gui.opBox.config(text = self.userString)
            self.clear()
            self.gui.textBox.insert("end", textVal + str(i))

        #resets math flag since i should be a number or . if it reaches this
        self.math = FALSE

    def firstNumGet(self):
        if "=" in self.userString:
            return
        first = self.gui.textBox.get()
        self.first_num = Decimal(first)
        
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
        self.gui.textBox.insert("end", f"{self.result}")
        self.first_num = self.result
        self.math = FALSE
        self.click("=")