from flask import Flask, render_template,request, redirect, url_for
from flask import session as flasksession
app = Flask(__name__)
app.secret_key = 'sdfljk348u389t4ejke8te89yhi'

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base,Users,Articles,Picture,Comments
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///crudlab.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/article/<int:articleid>/')
def article(articleid):
    article=session.query(Articles).filter_by(id=articleid).first()
    return render_template('full_article.html',article=article)

@app.route('/loggedout')
def log_out():
    flasksession['userid']=None
    return render_template('sign_in.html')

@app.route('/mainpage/')
def mainpage():
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    articles = session.query(Articles).all()
    return render_template('main_page.html',user=user, articles=articles)

@app.route('/signin/',methods=['GET','POST'])
def signin():
    if(request.method=='GET'):
        return render_template('sign_in.html')
    email=request.form['email']
    password=request.form['password']
    user=session.query(Users).filter_by(email=email).filter_by(password=password).first()
    flasksession['userid'] = user.id
    if(user!=None):
        return redirect(url_for('mainpage'))
    return render_template('sign_in.html')

@app.route('/')
def main():
    articles=session.query(Articles).all()
    return render_template('main_page1.html',articles=articles,user=None)

@app.route('/',methods=['POST'])
def search():

    word=request.form['search']
    Articles=session.query(Articles).all()
    articles1=[]
    for article in Articles:
        val = js.call('find', article.description, word)
        val1 = js.call('find', article.explanation, word)
        val2 = js.call('find', article.title, word)
        if(val!=-1 or val1!=-1 or val2!=-1):
            articles1.append(article)
    return render_template("main_page.html",Articles=articles1)
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
    article=Articles(
        title=title,
        description=description,
        explanation=explanation,
        )
    session.add(article)
    session.commit()
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    return redirect(url_for('mainpage'))
@app.route('/signup/',methods=['GET','POST'])
def signup():
    if(request.method=='GET'):
        return render_template('sign_up.html',user=None)
    email=request.form['email']
    password=request.form['password']
    confirmpassword=request.form['confirmpassword']
    if(confirmpassword!=password):
        return render_template('sign_up.html',user=Users(name="Passwords are not the same!!"))
    name=request.form['name']
    user1=session.query(Users).filter_by(email=email).first()
    if(user1!=None):
        return render_template('sign_up.html',user=Users(name="Email already used!!"))
    user=Users(name=name,email=email,password=password)
    session.add(user)
    session.commit()
    articles=session.query(Articles).all()
    return render_template('main_page.html',user=user,articles=articles)
if __name__ == '__main__':
    app.run(debug=True)

