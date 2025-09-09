from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session management

# ---------------- MONGODB CONFIG ----------------
app.config["MONGO_URI"] = "mongodb://localhost:27017/kfc"  # database = kfc
mongo = PyMongo(app)


# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = mongo.db.users.find_one({"username": username, "password": password})
        if user:
            session['username'] = username  # store login session
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="❌ Invalid Username or Password")

    return render_template("login.html")


# ---------------- SIGN UP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Check if username/email already exists
        existing_user = mongo.db.users.find_one(
            {"$or": [{"username": username}, {"email": email}]}
        )
        if existing_user:
            return render_template("signup.html", error="⚠ Username or Email already exists")

        # Insert new user
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": password
        })

        return redirect(url_for('login'))

    return render_template("signup.html")


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('username', None)  # remove user session
    return redirect(url_for('login'))


# ---------------- HOME ----------------
@app.route('/home')
def home():
    if 'username' not in session:  # if not logged in, go back to login
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])


# ---------------- OTHER PAGES ----------------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # You can save order details to MongoDB here
        return redirect(url_for('home'))  # or redirect to order_success page
    return render_template('order.html')


# ---------------- CANTEEN PAGES ----------------
@app.route('/kfc-canteen')
def kfc_canteen():
    return render_template('kfc-canteen.html')

# Snacks page
@app.route('/kfc-canteen/snacks')
def kfc_canteen_snacks():
    return render_template('kfc-canteen-snacks.html')

# Fastfood page
@app.route('/kfc-canteen/Fastfood')
def kfc_canteen_Fastfood():
    return render_template('kfc-canteen-Fastfood.html')

# Beverages page
@app.route('/kfc-canteen/beverages')
def kfc_canteen_beverages():
    return render_template('kfc-canteen-beverages.html')



# ---------------- KFC PAGES ----------------
@app.route('/Mess')
def Mess():
    return render_template('Mess.html')

@app.route('/Mess-breakfast')
def Mess_breakfast():
    return render_template('Mess-breakfast.html')

@app.route('/Mess-lunch')
def Mess_lunch():
    return render_template('Mess-lunch.html')

@app.route('/Mess-dinner')
def Mess_dinner():
    return render_template('Mess-dinner.html')

@app.route('/Mess-snacks')
def Mess_snacks():
    return render_template('Mess-snacks.html')


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)