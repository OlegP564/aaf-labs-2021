from table import Table
from container import pass_tree_dfs
from interface import message


class Database:
    def __init__(self):
        self.T = [] # tables    
    
    def cmd(self,cmd):
        if cmd['cmd'] == "CREATE":
            self.create(cmd)
        elif cmd['cmd'] == "INSERT":
            self.insert(cmd)
        elif cmd['cmd'] == "DELETE":
            self.delete(cmd)
        elif cmd['cmd'] == "SELECT":
            self.select(cmd)
        else:
            message("[Incorrect command]")
            
    
    def create(self,cmd):
        if cmd['args'] == [] or cmd['args'] == None:
            message("[Create error]: incorrect columns list")
            return
        self.T.append(Table(cmd['table_name'], cmd['args'], cmd['condition']))
        message("[Created \"{}\" successfully]".format(cmd['table_name']))

        
    def delete(self,cmd):
        for table in self.T:
            if table.name == cmd['table_name']:
                table.delete(cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'])
                message("[Deleted successfully]")
        
        
    def display(self, cmd):
        for table in self.T:
            if table.name == cmd['table_name']:
                table.display()
        
    def insert(self, cmd):
        for table in self.T:
            if table.name == cmd['table_name']:
                table.insert(cmd['args'])
                message("[Inserted in  \"{}\" successfully]".format(cmd['table_name']))
            
        
        
    def select(self, cmd):
        for table in self.T:
            if table.name == cmd['table_name'] and not cmd["JOIN"]:
                if not cmd['args']:
                    cmd['args'] = table.cols
                if not cmd['condition']:
                    table.select(cmd['args'], 1, '=', 1)
                else:
                    table.select(cmd['args'], cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'])
                
            if cmd["JOIN"]:
                if table.name == cmd['table_name']:
                    t1 = table
                if table.name == cmd['join_table']:
                    t2 = table  
                    
        if cmd["JOIN"]:
            for table in self.T:
                if table.name ==cmd['table_name']:
                    t1 = table
                if table.name ==cmd['join_table']:
                    t2 = table
            
            
            import numpy
            # read all tables into array
            arr1, arr2 = [],[]
            pass_tree_dfs(t1.data.root, arr1)
            pass_tree_dfs(t2.data.root, arr2)
            # for more efficiency
            import random
            random.shuffle(arr1)
            random.shuffle(arr2)
            
            w_cols = t1.cols + t2.cols
            mask = []
            # create wide mask
                                      
            wide_table = Table("wide", w_cols, [False for i in range(len(w_cols))])
            
            for node in arr1:
                print(node[-1].value)
                wide_table.insert(node[-1].value + [""]*len(t2.cols))
                
            for node in arr2:
                wide_table.insert([""]*len(t1.cols) + node[-1].value)
            # add rows to new wide table
            
            if cmd['join_args'][0] in w_cols and cmd['join_args'][0] in w_cols:
                
            # firstly, when col1==col2
                pass
                
                
            else:
                message("[Select error]: incorrect join arguments")          
            
            
            wide_table
            if not cmd['args']:
                cmd['args'] = wide_table.cols
            if not cmd['condition']:
                wide_table.select(cmd['args'], 1, '=', 1)
            else:
                wide_table.select(cmd['args'], cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'])
        
            
            # 1. create wide table t_wide
                
            # 2. change sign
            
            # 3. delete all rows from table, which not satisfy JOIN condition
          #  t_wide.delete(cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'])
           # table.select(cmd['args'], cmd['condition']['value1'], cmd['condition']['operator'], cmd['condition']['value2'])
    
