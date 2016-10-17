import redis





def testRedisConn(address, port, auth):
    try:
        rd=redis.Connection(host=address, port=port, db=0, password=auth)
        rd.connect()
    except:
        return 0
    return 1