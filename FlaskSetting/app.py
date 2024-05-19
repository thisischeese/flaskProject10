from flask import Flask, render_template    # 서버기능

app = Flask(__name__)

@app.route('/')
def home():
    return 'render_template('index.html')

@app.route('/mypage')
def mypage():
    return 'This is My Page!'    # URL 나누기 / 함수이름 달라야 함.

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    