import MySQLdb

def mysqldb_connection():
    try:
        #con=_mysql.connect(host="localhost",port=3306,user="root",db="twitter")
        connection = MySQLdb.connect(
                host = 'localhost',
                port=3306,
                user = 'root',
                db='twitter'
                )  # create the connection

        cursor = connection.cursor()     # get the cursor
        
        #cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)
    except MySQLdb.Error as e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
    
    finally:
        
        if cursor:
            return cursor