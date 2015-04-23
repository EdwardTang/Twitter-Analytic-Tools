import _mysql
import sys

def mysql_connection():
    try:
        con=_mysql.connect(host="localhost",port=3306,user="root",db="twitter")
        con.query("SELECT VERSION()")
        result = con.use_result()
        print "MySQL version: %s" % \
            result.fetch_row()[0]
    except _mysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    
    finally:
        
        if con:
            return con
            
