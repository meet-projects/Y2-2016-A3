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

@app.route('/article/<int:article_id>/')
def view_article(article_id):
    article=session.query(Articles).filter_by(id=article_id).first()
    return render_template('article.html', article=article)



@app.route('/mainpage/')
def mainpage():
    user=session.query(Users).filter_by(id=flasksession['userid']).first()
    articles = session.query(Articles).all()
    return render_template('main_page.html',user=user, articles=articles)

@app.route('/signin/',methods=['POST'])
def signin():
    email=request.form['email']
    password=request.form['password']
    user=session.query(Users).filter_by(email=email).filter_by(password=password).first()
    flasksession['userid'] = user.id
    if(user!=None):
        return redirect(url_for('mainpage',))
    return render_template('sign_in.html')

@app.route('/')
def main():
    return render_template('sign_in.html')

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
    return render_template('main_page.html',user=user)
if __name__ == '__main__':
    app.run(debug=True)

