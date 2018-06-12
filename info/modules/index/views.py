from info import redis_store
from . import index_blu
from flask import render_template


@index_blu.route("/", methods=['GET', 'POST'])
def hello_world():


    return render_template("news/index.html")