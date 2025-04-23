from flask import Flask, render_template, request, redirect, url_for, session
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用于session管理

# 图片上传配置
app.config['UPLOADED_PHOTOS_DEST'] = 'static/photos'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# 密码白名单
PASSWORDS = {'yasmine', 'rian', 'danny', 'yt'}

# 登录页（封面）
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_password = request.form.get('password', '').lower()
        if entered_password in PASSWORDS:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='密码错误，请重试。')
    return render_template('login.html')

# 首页：展示图片
@app.route('/home')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    image_files = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('index.html', image_files=image_files)

# 上传图片
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        photo.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], photo.filename))
        return redirect(url_for('index'))
    return render_template('upload.html')

# 退出登录（可选功能）
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)
    app.run(debug=True)
