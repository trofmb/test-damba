#!/usr/bin/env python
# main runner of damba engine
# ver. 1.4. ok 2019-11-18

import datetime

#import bottle
from bottle import get, put, route, run, debug, app, template, Bottle

app = Bottle()

dt = datetime.datetime.now()
dtstr = str(dt)
print ("damba engine. starting at %s\n" % (dtstr,))

@app.get('/')
def index ():
    dt = datetime.datetime.now()
    dtstr = str(dt)
    return "hello from engine at %s" % (dtstr,)

if __name__ == '__main__':
    app.run (server='gunicorn', host='0.0.0.0', port=8080)

#    app.debug (True)
#    app.run (host='0.0.0.0', port=8080)
#    app.run (host='localhost', port=8080)

