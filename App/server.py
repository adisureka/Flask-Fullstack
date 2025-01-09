import json
from pathlib import Path
from flask import Flask, render_template
from flask import request, session, url_for
#from flask_session import Session
from authentication import authentication
from database import get_data
import stripe

path = Path("./Env/api.json")
with open(path) as file:
	data = json.loads(file.read())
	public_key = data["public_key"]
	secret_key = data["secret_key"]
	product_keys = data["product_key"]

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["STRIPE_PUBLIC_KEY"] = public_key
app.config["STRIPE_SECRET_KEY"] = secret_key
stripe.api_key = app.config["STRIPE_SECRET_KEY"]


@app.route("/products", methods=["POST","GET"])
def products():
	display = False
	username = request.form.get("name")
	if not username:
		username = "Visitor"
	password = request.form.get("password")
	print(username, password)
	check = request.form.get("check")
	print("CHECK", check)
	if check != None:
		info = authentication(username, password, check)
	else:
		info = authentication(username, password)
	
	products = get_data('products')
	if request.method == "GET":
		info = "Please Login"
	return render_template("products.html", products = products, 
		                   info=info, display = display)


@app.route("/")
def login():	
	success = False
	return render_template("login.html", success=success)

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/cancel")
def cancel():
	return render_template("cancel.html")

@app.route("/success")
def success():
	return render_template("success.html")

@app.route("/charge", methods = ["POST", "GET"])
def charge():
	session = stripe.checkout.Session.create(
					payment_method_types=["card"],
					line_items=[{"price": product_keys[0], "quantity": 1}],
					mode="payment",
					success_url=url_for("success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
					cancel_url= url_for("cancel", _external=True)
					#
			   )
	return render_template('charge 2.html', 
		                   checkout_session_id = session["id"],
		                   checkout_public_key = app.config["STRIPE_PUBLIC_KEY"])



print("System exit 0")
