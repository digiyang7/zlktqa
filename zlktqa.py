# encoding: utf-8

# 註: 清掉瀏覽器緩存,以免造成開發中的困擾,底下2個方法都可以使用
#   1. 更多工具->開發人員工具->Network->將Disable cache打勾緩存
#   2. 更多工具->清除瀏覽資料

# zlktqa 項目實戰 : 項目結構搭建 => 導航條
# 項目用到jquery和Bootstrap
# 1.Bootstrap => https://www.bootcss.com/
# 2.jquery => https://code.jquery.com/jquery/

# 1.引用Bootstrap和jquery
# 2.修改導航條內容
# 3.修改導航條排版(將container-fluid改為container)
# 4.使用繼承方式新增base.html,並修改index.html
# 5.登錄 和 註冊 都有共同的一塊白色背景區塊且居中,在base.html加入main區塊並設置css
# 6.製作 登錄 和 註冊 頁面
# 7.創建User模型 -> 完成註冊功能 -> 完成登錄功能
# 8.製作 發佈問答 頁面 -> 發佈問答 登錄限製 裝飾器
# 9.創建Question Model -> 完成發佈問答功能
# 10.製作 首頁 頁面 -> 完成首頁功能
# 11.製作 發佈問答詳情頁面 -> 完成發佈問答詳情頁面功能
# 12.製作 評論 頁面 -> 創建評論模型 -> 完成評論功能 -> 完成評論列表的顯示

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    # 從DB查到資料 => 渲染到樣版
    context = {
        'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET','POST'])
def login():
   if request.method == 'GET':
       return render_template('login.html')
   else:
       telephone = request.form.get('telephone')
       password = request.form.get('password')
       # 查詢登錄的手機號與密碼是否正確
       user = User.query.filter(User.telephone == telephone, User.password == password).first()
       if user:
           # 可再加上checkbox功能, 若打勾,則記住user,下次不用在登錄
           session['user_id'] = user.id
           # 如果想在31天內都不需要登錄
           session.permanent = True
           return redirect(url_for('index'))
       else:
           # 可加上js即時顯示功能, 若不正常,直接顯示在此頁面做錯誤的提示
           return u'手機號碼或密碼不正常, 請確認! '

@app.route('/regist/', methods=['GET','POST'])
def regist():
    print(request.method)
    if request.method == 'GET':
       return render_template('regist.html')
    else:
       telephone = request.form.get('telephone')
       username = request.form.get('username')
       password1 = request.form.get('password1')
       password2 = request.form.get('password2')
       # print(telephone, username, password1, password2)
       # 手機號碼驗証, 如果被註冊了, 就不能再註冊了
       user = User.query.filter(User.telephone == telephone).first()
       if user:
           return u'該手機號碼已被註冊, 請更換手機號碼! '
       else:
            # password1與password2必須相等
            if password1 != password2:
                return u'兩次密碼不相等, 請核對後再填寫! '
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果註冊成功, 就讓頁面跳轉到登錄的頁面
                return redirect(url_for('login'))

@app.route('/question/', methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_detail = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_detail)

@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()