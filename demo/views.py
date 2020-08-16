from demo import app,db
from flask import Flask,url_for,render_template,request,fl ash,redirect
from flask_login import login_user,logout_user,login_required,current_user
from demo.models import User,Student
# views 视图函数
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单的数据
        name = request.form.get('name')
        E_score= request.form.get('E_score')
        P_score= request.form.get('P_score')
        C_score= request.form.get('C_score')
        # 验证数据
        if not name or not E_score or not P_score or not C_score or len(E_score)>4 or len(name)>60 or len(P_score)>4 or len(C_score)>4:
            flash('输入错误')
            return redirect(url_for('index'))
        # 将数据保存到数据库
        student = student(name=name,E_score=E_score,P_score=P_score,C_score=C_score) # 创建记录
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('index'))

    iniformation = Student.query.all()
    return render_template('index.html',iniformation=iniformation)

# 更新/student/edit
@app.route('/student/edit/<int:student_id>',methods=['GET','POST']) 
@login_required
def edit(student_id):
    Student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        name = request.form.get('name')
        E_score= request.form.get('E_score')
        P_score= request.form.get('P_score')
        C_score= request.form.get('C_score')
       if not name or not E_score or not P_score or not C_score or len(E_score)>4 or len(name)>60 or len(P_score)>4 or len(C_score)>4:
            flash('输入有误')
            return redirect(url_for('edit'),student_id = student_id)
        Student.name = name
        Student.E_score = E_score
        Student.P_score = P_score
        Student.C_score = C_score
        db.session.commit()
        flash('学生信息更新完成')
        return redirect(url_for('index'))
    return render_template('edit.html',Student=Student)

# delete视图函数
@app.route('/student/delete/<int:student_id>',methods=['GET','POST']) 
@login_required
def delete(student_id):
    Student= Student.query.get_or_404(student_id)
    db.session.delete(Student)
    db.session.commit()
    flash('删除完成')
    return redirect(url_for('index'))

# 登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入有误')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功')
            return redirect(url_for('index'))
        flash('验证失败')
        return redirect(url_for('login'))

    return render_template('login.html')

# 注册
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form["password2"]

        if not username or not password and password != password2:
            flash('输入有误')
            return redirect(url_for('register'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
              user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            
            flash('注册成功')
            return redirect(url_for('login'))
        flash('验证失败')
        return redirect(url_for('register'))

    return render_template('register.html')


# find 查找
@app.route('/student/find/<int:student_id>',methods=['GET','POST']) 
def find():
     Student = Student.query.get_or_404(student_id)

    if Student is None:

        content = " "

    iniformation = Student.query.filter(Student.name.like("%"+name+"%"),
    Student.E_score.like("%"+E_score+"%"),
    Student.P_score.like("%"+P_score+"%"),
    Student.C_score.like("%"+C_score+"%"),if content is not None else "").all()

    return render_template('search.html',iniformation = iniformation)

 # 展示所有信息
 @app.route('/all_iniformation/<int:student_id>')
def detail(student_id):
    info = Student.objects.all()
    return render_template('detail.html',info=info)



# detail 详细信息
@app.route('/detail/<int:student_id>')
def detail(student_id):
    info = iniformation[student_id]
    return render_template('index.html',info=info)


# logout 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('index'))

# settings 设置
@app.route('/settings',methods=['POST','GET'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('名字已经更新')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 