from info.utils.common import user_login_data
from . import profile_blu
from flask import render_template,g

@profile_blu.route('/user_info')
@user_login_data
def get_user_info():

    data = {
        "user_info":g.user.to_dict()
    }

    return render_template("news/user.html", data=data)