from flask import Flask, render_template,request, redirect, url_for
from flask import session as flasksession
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'sdfljk348u389t4ejke8te89yhi'

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base,Users,Articles,Picture,Comments
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import shutil
engine = create_engine('sqlite:///crudlab.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
def find(article,str1):
    str1=str1.upper()
    if(article.region not in str1):
        return -1
    return 1
@app.route('/article/<int:articleid>/')
def article(articleid):
    userid=flasksession['userid']
    article=session.query(Articles).filter_by(id=articleid).first()
    comments=session.query(Comments).filter_by(articleid=articleid).all()
    users=[]
    for comment in comments:
        users.append(session.query(Users).filter_by(id=comment.userid).first())
    user=session.query(Users).filter_by(id=userid).first()
    lencomments=len(comments)
    return render_template('full_article.html',article=article,users=users,user=user,comments=comments,lencomments=lencomments)

@app.route('/loggedout')
def log_out():
    flasksession['userid']=None
    return render_template('main_page1.html',user=None)

@app.route('/mainpage/')
def mainpage():
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    articles = session.query(Articles).all()
    return render_template('main_page.html',user=user, articles=articles)

@app.route('/signin/',methods=['GET','POST'])
def signin():
    if(request.method=='GET'):
        return render_template('sign_in.html')
    email=request.form['email1']
    password=request.form['password1']
    user=session.query(Users).filter_by(email=email).filter_by(password=password).first()
    flasksession['userid'] = user.id
    if(user!=None):
        return redirect(url_for('mainpage'))
    return render_template('sign_in.html')

@app.route('/')
def main():
    return render_template('main_page1.html',user=None)
@app.route('/<int:articleid>',methods=['POST'])
def add_comment(articleid):
    userid=flasksession['userid']
    user=session.query(Users).filter_by(id=userid).first()
    article=session.query(Articles).filter_by(id=articleid).first()
    date=datetime.today()
    comment=Comments(articleid=articleid,userid=userid,date=date,comment=request.form['comment'])
    session.add(comment)
    session.commit()
    comments=session.query(Comments).filter_by(articleid=articleid).all()
    users=[]
    for comment in comments:
        users.append(session.query(Users).filter_by(id=comment.userid).first())
    lencomments=len(comments)
    return render_template("full_article.html",users=users,user=user,article=article,comments=comments,lencomments=lencomments)
@app.route('/',methods=['POST'])
def search():
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    word=request.form['search']
    articles=session.query(Articles).all()
    articles1=[]
    for article in articles:
        if(find(article,word)!=-1):
            articles1.append(article)
    return render_template("main_page.html",Articles=articles1,user=user)
@app.route('/main')
def main1():
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    return render_template('main_page.html',user=user)

@app.route('/add_article/',methods=['GET','POST'])
def add_article():
    if request.method=='GET':
        return render_template('add_article.html')
    title=request.form['title']
    description=request.form['description']
    explanation=request.form['explanation']
    region=request.form['region']
    region=region.upper()
    article=Articles(
        title=title,
        description=description,
        explanation=explanation,
        region=region
        )
    session.add(article)
    session.commit()
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    return redirect(url_for('mainpage',user=user))

@app.route('/about/')
def about():
    return render_template('about.html',user=None)

        
@app.route('/signup/',methods=['GET','POST'])
def signup():
    if(request.method=='GET'):
        return render_template('sign_up.html',user=None)
    email=request.form['email']
    password=request.form['password']
    confirmpassword=request.form['confirmpassword']
    if(confirmpassword!=password):
        return render_template('main_page1.html',user=Users(name="Passwords are not the same!!"))
    name=request.form['name']
    user1=session.query(Users).filter_by(email=email).first()
    if(user1!=None):
        return render_template('main_page1.html',user=Users(name="Email already used!!"))
    user=Users(name=name,email=email,password=password)
    session.add(user)
    session.commit()
    articles=session.query(Articles).all()
    return render_template('main_page.html',user=user,articles=articles)
    
if __name__ == '__main__':
    app.run(debug=True)

