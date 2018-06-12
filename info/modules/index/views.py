from . import index_blu

@index_blu.route("/", methods=['GET', 'POST'])
def hello_world():
    # redis_store.set("name", "zhangsan")
    # name = redis_store.get("name")
    # print(name)
    # logging.debug('debugAAAA')
    # logging.info('infoAAA')
    # logging.error('errorAAA')
    #
    # current_app.logger.debug('debugBBB')
    # current_app.logger.info('infoBBB')
    # current_app.logger.error('errorBBB')

    return "hello word!"