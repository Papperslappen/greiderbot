from flask import Blueprint,abort,render_template
from common.storage import redis
import json
import logging
import sys


log = logging.getLogger("www.counter")

bp = Blueprint('counter',__name__,url_prefix='/counter')

def getCount(name):
    try:
        value = int(redis.hget("counter",name))
    except:
        log.warning("Exception in setting counter: {} - {}".format(name,sys.exc_info()[0]))
        value = 0
    return value


@bp.route('/test')
def test():
    return "TEST"

@bp.route('/api/<name>/')
def counter_data(name):
    log.info("Get counter: {}".format(name))
    counter = getCount(name)
    if (counter == ""):
        return abort(404)
    else:
        return json.dumps({"name":name,"value":counter})

@bp.route('/overlay/<name>/')
def counter_overlay(name):
    counter = getCount(name)
    return render_template("overlay.html",name=name,value=counter)
