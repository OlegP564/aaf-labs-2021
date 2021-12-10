from container import Tree, Row, pass_tree
from interface import message


class Table:
    def __init__(self, name, cols, indexed_cols_mask):
        self.name = name
        self.data = Tree(Row(cols, indexed_cols_mask))
        self.cols = cols
        self.w = 0
        self.imask = [i for i in range(len(indexed_cols_mask)) if indexed_cols_mask[i]]
        message("Table {} has been successfully created".format(name))

    def __generate_index(self, values):
        i = []
        if (self.imask):
            for k in self.imask:
                i.append(values[k])
        else:
            pass_tree(self.data.root, i)
            i = len(i) + 1
            message("[Warning]: default indexing used")
        return i
    

    def wideness(self):
            array = []
            pass_tree(self.data.root, array)
            widthes = []
            for row in array:
                widthes.append(max([len(str(col)) for col in row[0:-1]]))
            self.w = max(widthes) + 2
            return self.w


    def display(self, start=0, end=-1):
        array = []
        pass_tree(self.data.root, array)
        
        stxt = "+" + ("-"*self.wideness() + "+")*len(array[0][0:-1])
        txt = "|"
        for rn in array[0][0:-1]:
            txt = txt + " " + str(rn)  + str(" "*max(self.wideness() - len(str(rn)) - 2 , 0)) + " |"

        message(stxt)
        message(txt)
        message(stxt)
        
        for row in array[1::]:
            rtxt = "|"
            for col in row[0:-1]:
                rtxt = rtxt + " " + str(col) + " "*max(self.wideness() - len(str(col)) - 2 , 0) + " |"
            message(rtxt)
        message(stxt)

    def insert(self, values):
        if  len(values) == len(self.cols):
            for key in self.imask:
                values[key] = int(values[key])
            index = self.__generate_index(values)
            if index:
                row = Row(values, index)
                self.data.add(row)
        else:
            message("[Insert error]: row size incorrect")
            
            
    def delete(self, operand1, sign, operand2):
                
        array, arr = [], []
        pass_tree(self.data.root, arr)
        arr.pop(0)
        if operand1 and sign and operand2:
            if operand1 in self.cols:
                i1 = self.cols.index(operand1)
                val = operand2
            elif operand2 in self.cols:
                i1 = self.cols.index(operand2)
                val = operand1
            else:
                message("[Delete error]: incorrect operand")
                return
                
            # get all table in array view


            if sign == '=':
                array = [row for row in arr if row[i1] == val]                
            elif sign == "!=":
                array = [row for row in arr if not row[i1] == val]
            elif sign == ">":
                array = [row for row in arr if row[i1] > val]
            elif sign == "<":
                array = [row for row in arr if row[i1] < val]
            elif sign == ">=":
                array = [row for row in arr if row[i1] >= val]
            elif sign == "<=":
                array = [row for row in arr if row[i1] <= val]        
            else:
                message("[Delete error]: incorrect operation")     
             # delete all
            for row in array:
                self.data.delete(self.data.root, row[len(row)-1])
                
        else:
            for row in arr:
                self.data.delete(self.data.root, row[len(row)-1])
            self.data.delete(self.data.root, self.data.root.value)

        
        
        
        
        
    def select(self, cols, operand1, sign, operand2):
        if cols == [] or cols == None:
            cols = self.cols
        # get all table in array view
        array, arrr, arr = [], [], []
        pass_tree(self.data.root, arrr)
        arrr.pop(0)
        for c in cols:
            if c not in self.cols:
                message("[Select error]: incorrect column names")
                return
             
        for row in arrr:
            a = []
            for col in cols:
                a.append(row[self.cols.index(col)])
            arr.append(a)

        ####################
        # manage conditons
        if operand1 in self.cols and operand2 in self.cols:
            if operand1 not in cols or operand2 not in cols:
                message("[Select error]: incorrect command")
            i1, i2 = self.cols.index(operand1),  self.cols.index(operand2)
            if sign == '=':
                array = [row for row in arr if row[i1] == row[i2]]                
            elif sign == "!=":
                array = [row for row in arr if not row[i1] == row[i2]]
            elif sign == ">":
                array = [row for row in arr if row[i1] > row[i2]]
            elif sign == "<":
                array = [row for row in arr if row[i1] < row[i2]]
            elif sign == ">=":
                array = [row for row in arr if row[i1] >= row[i2]]
            elif sign == "<=":
                array = [row for row in arr if row[i1] <= row[i2]]        
            else:
                message("[Select error]: incorrect operation")
              
        elif operand1 in self.cols and operand2 not in self.cols:
            i1 = self.cols.index(operand1)
            if sign == '=':
                array = [row for row in arr if row[i1] == operand2]                
            elif sign == "!=":
                array = [row for row in arr if not row[i1] == operand2]
            elif sign == ">":
                array = [row for row in arr if row[i1] > operand2]
            elif sign == "<":
                array = [row for row in arr if row[i1] < operand2]
            elif sign == ">=":
                array = [row for row in arr if row[i1] >= operand2]
            elif sign == "<=":
                array = [row for row in arr if row[i1] <= operand2]        
            else:
                message("[Select error]: incorrect operation")
        elif operand1 not in self.cols and operand2 in self.cols:
            i2 = self.cols.index(operand2)
            if sign == '=':
                array = [row for row in arr if operand1 == row[i2]]                
            elif sign == "!=":
                array = [row for row in arr if not operand1 == row[i2]]
            elif sign == ">":
                array = [row for row in arr if operand1 > row[i2]]
            elif sign == "<":
                array = [row for row in arr if operand1 < row[i2]]
            elif sign == ">=":
                array = [row for row in arr if operand1 >= row[i2]]
            elif sign == "<=":
                array = [row for row in arr if operand1 <= row[i2]]        
            else:
                message("[Select error]: incorrect operation")    
        else:
            if sign == '=':
                array = [row for row in arr if operand1 == operand2]                
            elif sign == "!=":
                array = [row for row in arr if not operand1 == operand2]
            elif sign == ">":
                array = [row for row in arr if operand1 > operand2]
            elif sign == "<":
                array = [row for row in arr if operand1 < operand2]
            elif sign == ">=":
                array = [row for row in arr if operand1 >= operand2]
            elif sign == "<=":
                array = [row for row in arr if operand1 <= operand2]        
            else:
                message("[Select error]: incorrect operation")    
            
        stxt = "+" + ("-"*self.wideness() + "+")*len(cols)
        txt = "|"
        for rn in cols:
            txt = txt + " " + str(rn)  + str(" "*max(self.wideness() - len(rn) - 2 , 0)) + " |"

        message(stxt)
        message(txt)
        message(stxt)
        for row in array:
            rtxt = "|"
            for col in row:
                rtxt = rtxt + " " + str(col) + " "*max(self.wideness() - len(str(col)) - 2 , 0) + " |"
            message(rtxt)
        message(stxt)  
        


