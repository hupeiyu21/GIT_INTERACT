def getMQList(conn,mqname):
    resultlist=conn.xrange(mqname,"-","+")
    return resultlist

def getValue(conn,mkey):
    if(conn.exists(mkey)):
        return conn.get(mkey)
    else:
        return False