def getMQList(conn,mqname):
    resultlist=conn.xrange(mqname,"-","+")
    return resultlist