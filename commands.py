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

        #operation flag
        self.math = ""

        #result from eval()
        self.result = ""

        #sets precision of Decimal package
        getcontext().prec = 8

        self.opList = ['.', '+', '-', '×', '÷', '=']

    #function to clear contents of textBox
    def clear(self):
        self.gui.textBox.delete(0, END)
        return

    #same as clear but inserts a 0 in the textBox
    def clear_entry(self):
        textVal = self.gui.textBox.get()
        
        #prevents clearing info from self.userString if textBox = 0  or is empty
        if textVal == "0" or "":
            return
            
        #if funcKey has been used, 
        if "(" in self.userString:
            #remove characters up to the arithmetic operation
            for ar_op in self.opList[1:5]:
                if ar_op in self.userString:
                    op_index = self.userString.index(ar_op)
                    self.userString = self.userString[:op_index+1]
                    self.gui.opBox.config(text = self.userString)
                    break
        else:        
            n = len(textVal)
            self.userString = self.userString[:-n]
            self.gui.opBox.config(text = self.userString)
        
        self.textBoxInsert("0")
        return

    #Replaces value in textBox with insertVal
    def textBoxInsert(self, insertVal):
        self.clear()
        self.gui.textBox.insert("end", insertVal)

    def clear_all(self):
        #self.first_num = None
        self.userString = ""
        self.gui.opBox.config(text = self.userString)
        self.textBoxInsert("0")
        return

    def lastCharNotArithOp(self):
        return all(ar_op != self.userString[-1] for ar_op in self.opList[1:5])

    #If backspace is pressed, remove last character from userString
    def back(self):
        textVal = self.gui.textBox.get()
        #if last character is digit, delete from textbox also
        if len(textVal) > 0:
            if self.lastCharNotArithOp():
                self.textBoxInsert(textVal[:-1])
            self.userString = self.userString[:-1]
            self.gui.opBox.config(text = self.userString)
        return


    def inv(self, x):
        return 1/Decimal(x)

    def square(self, x):
        return Decimal(x)**2
        
    def sqroot(self, x):
        return sqrt(Decimal(x))

    def negate(self, x):
        return -1*Decimal(x)

    def funcDict(self):
        return {'sqrt': self.sqroot, 'sqr': self.square, 'inv': self.inv, 'negate': self.negate}

    def funcCalc(self, i, funcName):
        if funcName == "perc":
            temp = Decimal(i) / 100
            return temp, f"{temp}"
        else:
            temp = f"{funcName}({i})"
            return eval(temp, self.funcDict()), temp

    def anyArithOpInUserString(self):
        return any(ar_op in self.userString for ar_op in self.opList[1:5])

    def funcKey(self, func):
        textVal = self.gui.textBox.get()

        #Remove num to be replaced with func(num)
        #If false: 2+ -> 2+func(2)
        if self.userString[-1].isdigit():
            self.clear_entry()
        
        textBoxVal, userStrUpdate = self.funcCalc(textVal, func)

        #If no arithmetic operators are in the opBox, replace the previous funcKey command from the userString
        if "=" in self.userString or not self.anyArithOpInUserString():
            self.userString = userStrUpdate
        else:
            self.userString += userStrUpdate

        self.gui.opBox.config(text = self.userString)
        self.textBoxInsert(f"{textBoxVal}")
        return

    def noArithOpsInString(self):
        return all(ar_op not in self.userString for ar_op in self.opList[1:5])

    def click(self, i):
        #if operation in oplist already exists in the user string,
        #don't allow button to be pressed
        if len(self.userString) > 0  and self.userString[-1] == i and i in self.opList:
            return                

        #prevents user from typing 0 where there are no other entries in the userString. Ensures errors do not occur with decimal handling
        if len(self.userString) == 0 and str(i) == "0":
            return

        #prevents numbers from being placed after funcKey without an arithmetic operation
        #Ex. sqrt(3)5 is not allowed but sqrt(3)+5 is
        if "(" in self.userString and str(i).isdigit() and self.noArithOpsInString():
            return

        #If user presses different arithmetic operator after one already exists in the userString, replace the operator with the newly clicked operation
        #Ex. 3+ becomes 3- when - is clicked
        if len(self.userString) > 0 and self.userString[-1] in self.opList[1:5] and i in self.opList[1:5]:
            self.userString = self.userString[:-1] + i
            self.gui.opBox.config(text = self.userString)
            return

        #Writes to opBox
        self.opBoxUdpate(i)

        if str(i).isdigit() or i == ".":
            self.digitHandling(i)

        #resets math flag since i should be a number or . if it reaches this
        self.math = FALSE

    def opBoxUdpate(self, i):
        if "=" in self.userString and i != "=":
            #Set userString to result from equation
            self.userString = str(f"{self.result:.0f}")
            #add operation to userString
            self.userString += str(i)
            self.gui.opBox.config(text = self.userString)
        else:
            #Overwrites 0 when initial number is clicked
            if self.userString  == "0" and i != ".":
                self.userString = str(i)
            else:
                self.userString += str(i)
            self.gui.opBox.config(text = self.userString)

    def digitHandling(self, i):
        #Allows number to stay in textBox until another number is clicked
            for operation in self.opList[1:]:
                if len(self.userString) > 1 and self.userString[-2] == operation:
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
            self.textBoxInsert(textVal + str(i))

    '''def firstNumGet(self):
        if "=" in self.userString:
            return
        first = self.gui.textBox.get()
        self.first_num = Decimal(first)'''
        
    #Sets operations for addition, subtraction, multiplication, and division
    def arith(self, op):
        #self.firstNumGet()
        self.math = TRUE
        self.click(op)

    #fix multiplication and division operators for eval function
    def evalOpFix(self, strUpdate):
        return strUpdate.replace("×","*").replace("÷","/")

    def equal(self):
        #prevents user from pressing = twice in a row or trying to evaluate an empty string
        if "=" in self.userString or self.userString == "":
            return

        #replaces mult and div symbol for evaluation
        self.functionString = self.evalOpFix(self.userString)

        #evaluates functionString and pushes result to textBox
        self.result = eval(self.functionString, self.funcDict())
        self.textBoxInsert(f"{self.result}")
        #self.first_num = self.result
        self.math = FALSE
        self.click("=")