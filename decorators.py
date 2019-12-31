# encoding: utf-8

# 放所有限制的裝飾器
# 重要觀念
#def abc(): # 看成index函數
#    return 'abc'
#def demo(): # 看成wrapper函數
    # 雖然abc()有返回, 但這裡並無return 所有demo()不會返回 abc()返回的值, 所以因該要有return才能返回
    # 同理 wrapper函數因該要有return
#    abc()

from functools import wraps
from flask import session, redirect, url_for

# 登錄限制的裝飾器
# 1.轉換 index = login_required(index) = wrapper
# 2.執行index() 時 = wrapper()
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 若已登錄則可執行該函數, 若未登錄則跳轉到登錄頁面
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

