def parse(cmd, print_parsed=False):
    cmds = {}
    
    # find end of command
    cmd = cmd[0:cmd.find(';')]
    
    # split by space
    lst = cmd.split()
    # first word always command
    cmds['cmd'] = lst[0].strip(' \n\t“”"').upper()
    
    # detect table name
    if 'INTO' in cmd:
        cmds['table_name'] = cmd[cmd.upper().find('INTO') + 4:cmd.find('(')].strip()
    elif 'FROM' in cmd:
        cmds['table_name'] = cmd[cmd.upper().find('FROM') + 4::].split()[0].strip()
    else:
        cmds['table_name'] = lst[1].strip(' \n\t“”"')
        
    # work with arguments for INSERT
    if cmds['cmd'] == 'INSERT':
        parse_insert(cmd, cmds)
        
    # work with arguments for CREATE
    if cmds['cmd'] == 'CREATE':
        parse_create(cmd, cmds)

    # work with arguments for SELECT
    if cmds['cmd'] == 'SELECT':
        parse_select(cmd, cmds)

    # work with arguments for DELETE
    if cmds['cmd'] == 'DELETE':
        parse_delete(cmd, cmds)
        
    if print_parsed:
        for key in cmds:
            print(key, ' --> ', cmds[key])
    return cmds




def parse_create(cmd, dictionary):
    args = []
    indexed = []
    for arg in cmd[cmd.find("(")+1: cmd.find(')')].split(','):
        # fill bool array for indexing
        if "INDEXED" in arg:
            indexed.append(True)
        else:
            indexed.append(False)
        args.append(arg.replace("INDEXED", '').strip(' \n\t“”"') )

    dictionary['args'] = args
    dictionary['condition'] = indexed  
    
    
    
    
def parse_insert(cmd, dictionary):
    args = []
    for arg in cmd[cmd.find("(")+1: cmd.find(')')].split(','):
        args.append(arg.strip(' \n\t“”"') )

    dictionary['args'] = args
    
    
def parse_select(cmd, cmds):
    args = []
    conditions = []

    # find columns
    for arg in cmd[cmd.upper().find("SELECT")+6: cmd.upper().find('FROM')].split(','):
        if '*' in arg:
            break
        args.append(arg.strip(' \n\t“”"') )

    # if there is FULL_JOIN
    if ('FULL_JOIN') in cmd.upper():
        # second table name
        cmds['join_table'] = cmd[cmd.upper().find("FULL_JOIN")+9: cmd.find('ON')].strip(' \n\t“”"')

        # join condition
        cmds['join_args'] = []
        condition = cmd[cmd.find("ON")+2 : cmd.find('WHERE')].split('=')
        for col in condition:
            cmds['join_args'].append(col.strip('\n\t“”" '))


    # if there is WHERE keyword:
    cmds['condition'] = []
    if ('WHERE') in cmd.upper():
        cols = []
        condition = cmd[cmd.find("WHERE")+5 : cmd.find(';')].split()
        for col in condition:
            if '"' in col or '“' in col or "'" in col:
                cols.append({'value': col.strip('"“”\n\t')})
            elif '>' in col or '=' in col or '<' in col:
                cols.append({'operator':col.strip('\n\t')})
            else:
                cols.append({'column':col.strip('\n\t')})
        cmds['condition'] = cols

    cmds['args'] = args
    

def parse_delete(cmd, cmds):
    cols = []
    if ('WHERE') in cmd.upper():
        condition = cmd[cmd.find("WHERE")+5 : cmd.find(';')].split()
        for col in condition:
            if '"' in col or '“' in col or "'" in col:
                cols.append({'value': col.strip('"“”\n\t')})
            elif '>' in col or '=' in col or '<' in col:
                cols.append({'operator':col.strip('\n\t')})
            else:
                cols.append({'column':col.strip('\n\t')})
        cmds['condition'] = cols



d = parse('''

SELECT cat_id, cat_owner_id 
  FROM cats 
  WHERE name = “Murzik”;


'''
, 1)