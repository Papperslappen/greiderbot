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
        logging.log("")
        value = 0
    return value


@bp.route('/test')
def test():
    return "TEST"

@bp.route('/<name>')
def counter_data(name):
    log.info("Get counter: {}".format(name))
    counter = getCount(name)
    if not (counter == ""):
        return abort(404)
    else:
        return json.dumps({"name":name,"value":counter})

@bp.route('/<name>/overlay')
def counter_overlay(name):
    counter = getCount(name)
    return render_template("overlay.html",name=name,value=counter)
