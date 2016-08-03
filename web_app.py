from flask import Flask, render_template,request, redirect, url_for
app = Flask(__name__)

# SQLAlchemy stuff
### Add your tables here!
# For example:
# from database_setup import Base, Potato, Monkey
from database_setup import Base,Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/signin/',methods=['POST'])
def signin():
    email=request.form['email']
    password=request.form['password']
    user=session.query(Users).filter_by(email=email).filter_by(password=password).first()
    if(user!=null):
        return render_template('main_page.html')
    return render_template('sign_in.html')
@app.route('/')
def main():
    return render_template('sign_in.html')

if __name__ == '__main__':
    app.run(debug=True)
