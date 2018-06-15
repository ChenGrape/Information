from . import news_blu
from flask import render_template

@news_blu.route("/<int:news_id>")
def new_detail(news_id):

    return render_template("news/detail.html")