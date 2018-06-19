#coding:utf8
from qiniu import Auth, put_file, etag, urlsafe_base64_encode,put_data
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = 'uamqojf_BxYBinVjndycNhWYRXgBukLbMtdNEUXZ'
secret_key = 'I4f473dX6m3r-mTpHUKtHv1_Khy7WH1VE3Vg1SHN'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'image1'

#生成上传 Token，空间名称,名字不传由七牛云维护, 可以指定过期时间等
token = q.upload_token(bucket_name, None, 3600)

def image_storage(image_data):

    # 上传图片
    ret, info = put_data(token,None,image_data)

    #判断图片是否有上传成功
    if info.status_code == 200:
        return ret.get("key")
    else:
        return  "上传失败"

# if __name__ == '__main__':
#
#     with open('22.png','rb') as f:
#         image_storage(f.read())