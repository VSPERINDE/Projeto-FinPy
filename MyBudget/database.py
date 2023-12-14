from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/finpy"
mongo = PyMongo(app)

db = MongoClient("mongodb://localhost:27017/")["finpy"]


# @app.route("/register", methods=["GET", "POST"])
# def register():
#    if request.method == "POST":
#        email = request.form["email"]
#        password = request.form["password"]
#        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
#        user = {"email": email, "password": hashed_password}
#        mongo.db.users.insert_one(user)
#        return redirect(url_for("login"))
#    return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#    if request.method == "POST":
#        email = request.form["email"]
#        password = request.form["password"]
#        user = mongo.db.users.find_one({"email": email})
#        if user and bcrypt.check_password_hash(user["password"], password):
#            # Autenticação bem-sucedida, redirecione para o painel do usuário
#            return redirect(url_for("user_dashboard"))
#        else:
#            # Autenticação falhou, redirecione para a página de login
#            return redirect(url_for("login"))
#    return render_template("login.html")
