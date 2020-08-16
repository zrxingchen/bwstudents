from watchlist import db,app
from watchlist.models import User,Movie
import click
# 自定义命令
# 建立空数据库
@app.cli.command()  # 注册为命令
@click.option('--drop',is_flag=True,help="先删除再创建")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")

# 向空数据库中插入数据
@app.cli.command()
def forge():
    name = "Dom"
    iniformation = [
       {'name':"小明","E_score":"99","P_score":"99","C_score":"99"},
       {'name':"小红","E_score":"100","P_score":"100","C_score":"100"},
       {'name':"小黑","E_score":"97","P_score":"97","C_score":"97"},
       {'name':"小白","E_score":"98","P_score":"98","C_score":"98"},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in iniformation:
        student = student(name=m['name'],E_score=m['E_score'],P_score=m['P_score'],C_score=m['C_score'])
        db.session.add(movie)
    db.session.commit()
    click.echo("导入数据完成")


# 自定义指令，生成管理员账号flask admin
# 输入用户名Admin,密码，确认密码
@app.cli.command()
@click.option('--username',prompt=True,help='登录的用户名')
@click.option('--password',prompt=True,help='登录的密码',confirmation_prompt=True,hide_input=True)
def admin(username,password):
    user = User.query.first()
    if user is not None:
        click.echo('更新管理员用户')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建管理员账户')
        user = User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo('管理员账号更新/创建完成')

