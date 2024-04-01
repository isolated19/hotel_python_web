from flask import Flask ,request,render_template,redirect,flash,session


import sqlite3

sqlconnection =sqlite3.connect("hotel.db")
sqlconnection.execute("create table if not exists users(id integer primary key,username text,password integer, email text,phone integer,address text,pincode integer,picture blob,dob date)")
# Create the 'adlogin' table if it does not exist
sqlconnection.execute("CREATE TABLE IF NOT EXISTS adlogin (id INTEGER PRIMARY KEY, adusername TEXT, adpassword TEXT)")
sqlconnection.execute("CREATE TABLE IF NOT EXISTS booking (id INTEGER PRIMARY KEY, status TEXT, checkin TEXT, guest TEXT, customerinfo TEXT, price TEXT, accomodation TEXT, date date)")
sqlconnection.close()

app=Flask(__name__)
app.secret_key="123"

# admin
@app.route('/admin')
def admin():
    return render_template('admin/index.html')
@app.route('/dash')
def dash():
    return render_template('admin/dashboard.html')
@app.route('/revroom')
def revroom():
    return render_template('admin/updroom.html')
@app.route('/bookin')
def bookin():
    bdata = get_data_from_bookin()
    return render_template('admin/checkin.html',bdata=bdata)
@app.route('/cout')  
def cout(): 
  return render_template('admin/checkout.html')
@app.route('/user')  
def user():
    image_path = get_data_from_database()
    data = get_data_from_database()
    return render_template('admin/revuser.html', data=data,image_path=image_path)
@app.route('/adlog',methods =["GET","POST"])
def adlog():
    if request.method =="POST":
        name=request.form['username']
        psswd=request.form['password']
        sqlconnection= sqlite3.connect('hotel.db')
        sqlconnection.row_factory=sqlite3.Row
        cur=sqlconnection.cursor()
        
        cur.execute("select * from adlogin where adusername =? and adpassword =?",(name,psswd))
        data=cur.fetchone()
        if (data):
          session['name']=data["adusername"] 
          session['psswd']=data["adpassword"] 
          flash("Welcome to Zomaika","logged")
          return redirect("/dash")
        else:
            flash("Invalid Username and Password","danger")
            return redirect('/admin')
    return redirect('/')


# Function to retrieve data from the database
def get_data_from_database():
    sqlconnection = sqlite3.connect('hotel.db')
    cur = sqlconnection.cursor()
    cur.execute("SELECT * FROM  users")
   
    data = cur.fetchall()
    sqlconnection.close()
    return data
def get_image_path_from_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT picture FROM users")  # Add your SQL query here
    image_path = cursor.fetchone()
    conn.close()
    return image_path
def get_data_from_bookin():
    sqlconnection = sqlite3.connect('hotel.db')
    cur = sqlconnection.cursor()
    cur.execute("SELECT * FROM  booking")
   
    bdata = cur.fetchall()
    sqlconnection.close()
    return bdata






#***************************************************************************************# 


# user-side api

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/room')
def room():
    return render_template('room.html')
@app.route('/facilities')
def facilities():
    return render_template('facilities.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/Cashreturn')
def Cashreturn():
    return render_template('Cashreturn.html')

@app.route('/clog',methods =["GET","POST"])
def log():
    if request.method =="POST":
        mail=request.form['email']
        psswd=request.form['password']
        sqlconnection= sqlite3.connect('hotel.db')
        sqlconnection.row_factory=sqlite3.Row
        cur=sqlconnection.cursor()
        
        cur.execute("select * from users where email =? and password =?",(mail,psswd))
        data=cur.fetchone()
        if (data):
          session['name']=data["username"] 
          session['mail']=data["email"] 
          flash("Welcome to Zomaika","logged")
          return redirect("/room")
        else:
            flash("Invalid Username and Password","danger")
            return redirect('/')
    return redirect('/room')

@app.route('/signup',methods =["GET","POST"])
def signup():
    if request.method =="POST":
        try:
            name=request.form['username']
            psswd=request.form['password']
            mail=request.form['email']
            phone=request.form['phonenumber']
            address=request.form['address']
            pincode=request.form['pincode']
            profile=request.form['profile']
            dob=request.form['dob']
            sqlconnection=sqlite3.connect('hotel.db')
            cur=sqlconnection.cursor()
            cur.execute("insert into users(username,password,email,phone,address,pincode,picture,dob)values(?,?,?,?,?,?,?,?)",(name,psswd,mail,phone,address,pincode,profile,dob))
            sqlconnection.commit()
            flash("Record added Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:   
           return redirect('/')
           sqlconnection.close()
      
    return render_template('/')

# @app.route('/chat',methods =["GET","POST"])
# def chat():
#     if request.method =="POST":
#         try:
#             fname=request.form['firstname']
#             lname=request.form['lastname']
#             add=request.form['address']
#             cont=request.form['country']
#             zipcde=request.form['zipcode']
#             cit=request.form['city']
#             cit=request.form['state']
#             sqlconnection=sqlite3.connect('login.db')
#             cur=sqlconnection.cursor()
#             cur.execute("insert into users(username,password,email)values(?,?,?)",(name,psswd,mail))
#             sqlconnection.commit()
#             flash("Order has been placed ","success")
#         except:
#             flash("Error in Insert Operation","danger")
#         finally:   
#            return redirect('/client')
#            sqlconnection.close()
        
#     return render_template('signup.html')

@app.route('/product')
def product():
    return render_template('product.html')

if __name__=="__main__":
    app.run(debug=True)

    