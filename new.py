#####################################################################################################
'''                                ******Contact Page******
                      *****Created By: Pradeep Kumar Yadav*****

                            *****Programming Language*****
                                   1. Python programming using Flask Framework
                                   2. HTML for create templates, form
                                   3. Bootstrap for CSS and JavaScript

                        *****Additional tools and technologies*****
                                   1. Flask-SQLAlchemy
                                   2. pymysql - mysql connector for python programming language

***************For any suggestion/query please mail me: pkyadav3444@gmail.com***************
'''
# import required libraries
from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy



# create a flask class and store it in app
app = Flask(__name__)

# create database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pradeep'
# create secret key for additional security
# below both lines are optional
app.config['SECRET_KEY'] = 'I_LOVE_INDIA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# create a variable to give access of database to app
db = SQLAlchemy(app)


# create a class for creating a table if not existing already and containing columns
class APIUserModel(db.Model):
    __tablename__='student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))


# create app route for access app in client machine
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method=='POST':
        # get user information from html form
        form = request.form
        name = form['name']
        email = form['email']
        # and store value to the class 
        api_user_model = APIUserModel(name = name, email=email)
        # everytime when you made changes in your database, you should need to create a session
        save_to_database = db.session()
        try:
            # add values to the database using class declared above
            save_to_database.add(api_user_model)
            # always commit to the database for making changes confirm
            save_to_database.commit()
            # return home page
            return redirect(url_for(index))
        except:
            # if something not going right, then rollback
            save_to_database.rollback()
            # and flush garbage from database
            save_to_database.flush()

    # execute query for all values
    data = APIUserModel.query.all()
    # return the index page
    return render_template("index.html", data = data)


# Delete data from database one by one using id
@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    # again create session
    save_to_database = db.session()
    # run this query to filter data according id and delete it
    APIUserModel.query.filter_by(id= id).delete()
    # commit changes to database
    save_to_database.commit()
    # and redirect to home page
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=7040)
