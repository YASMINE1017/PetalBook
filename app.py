from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

app = Flask(__name__)

# 设置图片上传路径
app.config['UPLOADED_PHOTOS_DEST'] = 'static/photos'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# 首页路由
@app.route('/')
def index():
    # 获取图片文件列表
    image_files = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('index.html', image_files=image_files)

# 上传图片路由
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        photo.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], photo.filename))
        return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
