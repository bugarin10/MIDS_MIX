from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"


class UserTypeForm(FlaskForm):
    user_type = HiddenField("User Type")
    submit_customer = SubmitField("I'm a Customer")
    submit_owner = SubmitField("I'm an Owner")


@app.route("/", methods=["GET", "POST"])
def index():
    form = UserTypeForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        if user_type == "Customer":
            return redirect(url_for("customer"))
        elif user_type == "Owner":
            return redirect(url_for("owner"))
    return render_template("index.html", form=form)


@app.route("/Customer")
def customer():
    return render_template("Customer.html", user_type="Customer")


@app.route("/Owner")
def owner():
    return render_template("owner.html", user_type="Owner")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
