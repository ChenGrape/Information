import errno
from flask import abort, jsonify,request,current_app,g,render_template
from info import constants, db
from info.models import User,News, Comment, CommentLike
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import news_blu


# 点赞/取消点赞
# 请求路径: /news/comment_like
# 请求方式: POST
# 请求参数:news_id,comment_id,action,g.user
# 返回值: errno,errmsg
@news_blu.route('/comment_like', methods=['POST'])
@user_login_data
def comment_like():
    """
    思路分析
    1.判断用户是否有登陆
    2.获取参数
    3.校验参数
    4.根据操作类型,执行具体操作
    5.返回响应
    :return:
    """
    # 1.判断用户是否有登陆

    if not g.user:

        return jsonify(errno=RET.NODATA, errmsg="该用户没有登陆")

    # 2.获取参数
    dict_data = request.json
    news_id = dict_data.get("news_id")
    comment_id = dict_data.get("comment_id")
    action = dict_data.get("action")

    # 3.校验参数

    if not all([news_id, comment_id, action]):

        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not action in ["add", "remove"]:

        return jsonify(errno=RET.DATAERR, errmsg="操作类型有误")

      # 取出评论对象

    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)


    if not comment:

        return jsonify(errno=RET.NODATA, errmsg="该评论不存在")

    # 4.根据操作类型,执行具体操作
    if action == "add":
        # 判断用户是否已经点过赞了
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id,
                                                     CommentLike.user_id == g.user.id).first()
        if not comment_like:
            comment_like = CommentLike()
            comment_like.comment_id = comment_id
            comment_like.user_id = g.user.id
            db.session.add(comment_like)

            # 将点赞数量 +1
            # comment.like_count += 1
    else:
        # 判断用户是否已经点过赞了
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id,
                                                     CommentLike.user_id == g.user.id).first()

        if comment_like:
            db.session.delete(comment_like)

            # 将点赞数量-1操作
            # comment.likecount -= 1

    # 5.返回响应

    return jsonify(errno=RET.OK, errmsg="操作成功")


#新闻评论
# 请求路径: /news/news_comment
# 请求方式: POST
# 请求参数:news_id,comment,parent_id g.user
# 返回值: errno,errmsg

@news_blu.route('/news_comment', methods=['POST'])
@user_login_data
def news_comment():
    """
    1.判断用户是否登陆
    2.获取参数
    3.校验参数,为空校验
    4.创建评论对象，设置属性
    5.提交到数据库
    6.返回响应
    :return:
    """
    # 1.判断用户是否登陆
    if not g.user:
        return jsonify(errno=RET.NODATA, errmsg="用户未登录")

    # 2.获取参数
    data_dict = request.json
    news_id = data_dict.get("news_id")
    content = data_dict.get("comment")
    parent_id = data_dict.get("parent_id")

    # 3.校验参数,为空校验
    if not all([news_id,content]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 4.创建评论对象，设置属性
    comment = Comment()
    comment.user_id = g.user.id
    comment.content = content
    comment.news_id = news_id
    if parent_id:
        comment.parent_id = parent_id

    # 5.提交到数据库
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
    # 6.返回响应
    return jsonify(errno=RET.OK, errmsg="操作成功",data=comment.to_dict())

#新闻收藏/取消收藏
# 请求路径: /news/news_collect
# 请求方式: POST
# 请求参数:news_id,action, g.user
# 返回值: errno,errmsg
@news_blu.route('/news_collect', methods=['POST'])
@user_login_data
def news_collect():


    # 1.判断用户是否登陆
    if not g.user:
        return jsonify(errno=RET.NODATA, errmsg="用户未登录")
    # 2.获取参数
    data_dict = request.json
    news_id = data_dict.get('news_id')
    action = data_dict.get('action')

    # 3.校验参数,为空校验,action操作类型
    if not all([news_id,action]):
        return jsonify(errno = RET.PARAMERR,errmsg="参数不完整")
    if not action in ['collect', 'cancel_collect']:
        return jsonify(errno=RET.DATAERR, errmsg="操作类型错误")

    # 取出新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="该新闻不存在")
    # 4.根据操作类型,做收藏或者取消收藏操作
    if action == "collect":
        g.user.collection_news.append(news)
    else:
        g.user.collection_news.remove(news)
    # 5.响应数据
    return jsonify(errno=RET.OK, errmsg="操作成功")



@news_blu.route("/<int:news_id>")
@user_login_data
def new_detail(news_id):

    # 查询数据库，返回点击量前10的新闻数据
    try:
        click_news =News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all();
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in click_news:
        click_news_list.append(news.to_dict())

    # 获取新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    # 如果没有该条新闻直接找不到页面
    if not news:
        abort(404)

    # 判断用户是否收藏过该新闻
    is_collected = False
    if g.user and news in g.user.collection_news:
        is_collected = True

    # 获取新闻所有评论
    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    # 查询用户对当前新闻,哪些评论点过赞
    if g.user:

        # 获取评论的id
        comm_ids = [comm.id for comm in comments]

        # 获取用户点赞过的评论, 的所有点赞对象
        # CommentLike.comment_id.in_(comment_ids): 获取当前新闻的,评论的,所有点赞对象(有张三,李四,王五的点赞)
        # CommentLike.user_id == g.user.id :过滤出了,某个(比如张三)人的点赞对象
        commentLike = CommentLike.query.filter(CommentLike.comment_id.in_(comm_ids),CommentLike.user_id == g.user.id).all()

        # 得到用户点赞过的，所有评论编号
        commentlike_id = [comm_like.comment_id for comm_like in commentLike]

    comments_list =[]
    for comment in comments:
        # comments_list.append(comment.to_dict())

        # 向评论字典中添加点赞属性
        comm_dict = comment.to_dict()
        comm_dict["is_like"] = False
        # 如果登陆了,并且,当前的评论编号在我点赞过的评论编号中,改变is_like的值
        if g.user and comment.id in commentlike_id:
            comm_dict["is_like"] = True

        comments_list.append(comm_dict)


    data = {
        # 如果user为空返回None,如果有内容返回左边
        "user_info": g.user.to_dict() if g.user else None,
        "news_info": click_news_list,
        "news":news.to_dict(),
        "is_collected":is_collected,
        "comments":comments_list

    }
    return render_template("news/detail.html", data = data)