#!/usr/bin/env python
# main runner of damba engine
# ver. 1.13. run 2019-11-19
# Mikhail Kolodin

version = '1.13'

import datetime
import ulid
import redis

#import bottle
from bottle import get, post, route, run, debug, app, template, Bottle

app = Bottle()

app.config["autojson"] = True

dt = datetime.datetime.now()
dtstr = str(dt)
print ("damba engine. starting at %s\n" % (dtstr,))

print ("connect to redis: ", end="")
myredis = None
try:
#    myredis = redis.Redis()
    myredis = redis.Redis(host="db", port=6379, db=0)
    print ("connected")
except:
    print ("cannot connect")


# --------------- bazed ULID
def bazed_ulid(n):
    baza = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    bl = len(baza)
    res = ''
    if n == 0:
        return '0'
    while n:
        r = n % bl
        n //= bl
        res = baza[r] + res
    return res


# --------------- web services

# --------------- index
@app.get('/')
def index ():
    dt = datetime.datetime.now()
    dtstr = str(dt)
    myulid = ulid.new()
    strmyulid = myulid.str
    intmyulid = myulid.int
    bmyulid = bazed_ulid(intmyulid)

    return "<tt>hello from engine ver.%s at %s<br />as long %s [len%d] and short %s [len%d]</tt>" % (
        version, dtstr, strmyulid, len(strmyulid), bmyulid, len(bmyulid))

# --------------- info
@app.get('/info')
def info():
    return {"version": version, "datetime_utc": dtstr}

# --------------- putredis
@app.get('/putredis')
def putredis():
    if myredis:
        myredis.set(b"foo", b"bar")
        return "set foo=bar"
    else:
        return "no redis connection"
    
# --------------- getredis
@app.get('/getredis')
def getredis():
    if myredis:
        bar = myredis.get(b"foo")
        return "got foo=%s" % (str(bar),)
    else:
        return "no redis connection"

# ---------------- caller
if __name__ == '__main__':
    app.run (server='gunicorn', host='0.0.0.0', port=8080, debug=True)

#    app.debug (True)
#    app.run (host='0.0.0.0', port=8080)
#    app.run (host='localhost', port=8080)

# the end.
