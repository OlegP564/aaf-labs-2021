
def error(message):
    # do something maybe =/ ...
    print("\nERROR:", message, '\n')


    
def check_commands(cmd):
    if cmd['cmd'] not in ['INSERT', 'SELECT', 'DELETE', 'CREATE']:
        error("Incorrect command")
        return 1
    if cmd['table_name'] == '' or cmd['table_name'] == 'WHERE':
        error("Incorrect table name")
        return 1
    if cmd['cmd'] == "SELECT" or  cmd['cmd'] == "DELETE":
        for key in cmd['condition']:
            if cmd['condition'][key] == '':
                error("Incorrect condition state")
                return 1
    return 0
        

def parse(cmd, print_parsed=False):
    cmds = {}
    cmd  = cmd + ";"
    # find end of command
    cmd = cmd[0:cmd.find(';')]
    
    # split by space
    lst = cmd.split()
    # first word always command
    cmds['cmd'] = lst[0].replace('\n', '').replace(' ', '').replace('\t', '').upper()
    
    # detect table name
    if 'INTO' in cmd:
        name = cmd[cmd.upper().find('INTO') + 4: cmd.find('(')].replace(',', ' ')
        cmds['table_name'] = name.split()[0]

    elif 'FROM' in cmd:
        cmds['table_name'] = cmd[cmd.upper().find('FROM') + 4::].split()[0].strip()
    else:
        cmds['table_name'] = lst[1].replace('\n', '').replace('\t', '')
        
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
        
    if print_parsed and not check_commands(cmds):
        for key in cmds:
            print(key, ' --> ', cmds[key])
    # check cmd        
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
    for arg in cmd[max(cmd.find("(")+1, 1+cmd.find(dictionary['table_name']) + len(dictionary['table_name'])): cmd.find(')')].replace(',', ' ').split(' '):
        arg = arg.replace('\n', ' ').replace('\t', ' ').replace(' ', '')
        if len(arg) >= 1 and arg!='\n':
            args.append(arg)

    dictionary['args'] = args
    
    
def parse_select(cmd, cmds):
    args = []
    conditions = []
    cmd = cmd.replace('\n', ' ').replace('\t', ' ')

    # find columns
    for arg in cmd[cmd.upper().find("SELECT")+6: cmd.upper().find('FROM')].replace(',', ' ').split(' '):
        if '*' in arg:
            break
        arg = arg.replace(' ', '')
        if len(arg) >= 1 and arg!='\n':
            args.append(arg)

    # if there is FULL_JOIN
    if ('FULL_JOIN') in cmd.upper():
        # second table name
        cmds['join_table'] = cmd[cmd.upper().find("FULL_JOIN")+9: cmd.find('ON')].strip(' \n\t“”"')

        # join condition
        cmds['join_args'] = []
        condition = cmd[cmd.find("ON")+1 : cmd.find('WHERE')].split('=')
        for col in condition:
            cmds['join_args'].append(col.strip('\n\t“”" '))


    # if there is WHERE keyword:
    cmds['condition'] = []
    if ('WHERE') in cmd.upper():
        cols = {'value1':'', 'operator':'', 'value2':''}
        condition = cmd[cmd.find("WHERE")+5 : cmd.find(';')].split()
        for col in condition:
            if '"' in col or '“' in col or "'" in col:
                cols['value1'] = col.strip('"“”\n\t')
            elif '>' in col or '=' in col or '<' in col:
                cols['operator'] = col.strip('\n\t')
            else:
                cols['value2'] = col.strip('\n\t')
        cmds['condition'] = cols

    cmds['args'] = args
    

def parse_delete(cmd, cmds):
    cols = {'value1':'', 'operator':'', 'value2':''}
    if ('WHERE') in cmd.upper():
        condition = cmd[cmd.find("WHERE")+5 : cmd.find(';')].split()
        for col in condition:
            if '"' in col or '“' in col or "'" in col:
                cols['value1'] = col.strip('"“”\n\t')
            elif '>' in col or '=' in col or '<' in col:
                cols['operator'] = col.strip('\n\t')
            else:
                cols['value2'] = col.strip('\n\t')
        cmds['condition'] = cols
