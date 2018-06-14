import random
import re
from flask import current_app, jsonify,request,make_response
from info import constants,redis_store, db
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu
from info.models import User


#注册用户
# 请求路径: /passport/register
# 请求方式: POST
# 请求参数: mobile, sms_code,password
# 返回值: errno, errmsg
@passport_blu.route('/register', methods=['POST'])
def register():

    # 1.获取参数
    data_dict = request.json
    mobile = data_dict.get("mobile")
    sms_code = data_dict.get("sms_code")
    password = data_dict.get("password")

    # 2.校验参数(为空校验,手机号格式校验)
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    # 3.通过手机号取出redis中的短信验证码
    try:
        redis_sms_code = redis_store.get("sms_code:%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取短信验证码异常")
    # 4.判断是否过期
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码过期")
    # 5.判断是否相等
    if sms_code != redis_sms_code :
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码填写错误")
    # 6.创建用户对象,设置属性
    user = User()
    user.nick_name = mobile
    user.mobile = mobile
    user.password_hash = user.jiami_secret(password)
    # 7.保存到数据库
    try:
        db.session.add(user)
        db.session.commit
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="用户保存异常")
    # 8.返回前端页面
    return jsonify(errno=RET.OK,errmsg="注册成功")








# 短信验证码
# 请求路径： /passport/sms_code
# 请求方式： post
# 请求参数： mobile,image_code,image_code_id
# 返回值： error,errmsg
@passport_blu.route('/sms_code', methods=['POST'])
def get_sms_code():

    # 1.获取参数,request.data,  json.loads(json)
    dict_data = request.json
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")
    print(image_code_id)
    # 2.校验参数为空情况
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")
    # 3.验证手机号格式
    if not re.match('1[356789]\\d{9}', mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式不正确")

    # 4.通过image_code_id取出redis中的图片验证码
    try:
       redis_image_code = redis_store.get("image_code:%s"%image_code_id)
    except Exception as e:
       current_app.logger.error(e)
       return jsonify(errno=RET.DBERR,errmsg="查找图片验证码失败")

    # 5.判断取出的图片验证码是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg="图片验证码过期")

    # 6.判断两者图片验证码是否相等
    if image_code.lower() != redis_image_code.lower():
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码不正确")

    # 7.生成短信验证码
    sms_code = "%06d"%random.randint(0,999999)

    # 8.调用云通讯发送(手机号,短信验证码,有效期,模板id)
    # ccp = CCP()
    # result =  ccp.send_template_sms(mobile,[sms_code,5],1)
    #
    # if result == -1:
    #     return jsonify(errno=RET.THIRDERR, errmsg="短信验证码发送失败")

    current_app.logger.debug("短信验证码是 = %s"%sms_code)

    # 9.保存到redis
    try:
       redis_store.set("sms_code:%s"%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="短信保存失败")

    # 10.返回前端
    return jsonify(errno=RET.OK,errmsg="发送成功")



# 图片验证码
@passport_blu.route('/image_code')
def get_image_code():
    # 1.获取请求参数
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")
    # 2. 生成图片验证码
    name,text,image_data = captcha.generate_captcha()
    # 3.保存到redis中
    try:
        redis_store.set("image_code:%s" % cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete("image_code:%s"%pre_id)
    except Exception as e:
        current_app.logger.error(e)

    # 4.返回图片验证码
    response = make_response(image_data)
    response.headers["Content-Type"] = "image/jpg"
    return response