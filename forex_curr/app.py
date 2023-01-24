from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates, CurrencyCodes

from currencies import currencies


app = Flask(__name__)
app.config["SECRET_KEY"] = "asdjfhsadklfkldgh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

curr = CurrencyRates(force_decimal=False)
curr_code = CurrencyCodes()
curr_code_list = [curr["cc"] for curr in currencies]



@app.route("/")
def root_route():
    """ The root route that asks the user to input the currency information"""
    return render_template("convert-form.html")

@app.route("/convert", methods=["POST"])
def convert_route():
    """ Convert the values from the user input into the actual currency values using """

    curr_from = request.form["curr_from"]
    curr_to = request.form["curr_to"]
    # using a try catch block to check if the amount input is a numeric value
    try:
        amount = float(request.form["amount"])
    except ValueError:
        flash("Amount must be a valid number!")
        return redirect("/")

    # check if user input is valid (correct currency formats and correct amount format
    if (not curr_from in curr_code_list):
        flash(f"Not valid Currency Code: {curr_from} in Currency From")
        return redirect("/")

    if (not curr_to in curr_code_list):
        flash(f"Not valid Currency Code: {curr_to} in Currency To")
        return redirect("/")

    if (amount < 0):
        flash("Amount cannot be negative!")
        return redirect("/")

    #use the info from the forms and the API to convert the currency
    curr_from_info = {
        "symbol": curr_code.get_symbol(curr_from),
        "name": curr_code.get_currency_name(curr_from),
        "amount": amount
    }
    curr_to_info = {
        "symbol": curr_code.get_symbol(curr_to),
        "name": curr_code.get_currency_name(curr_to),
        "new_amount": round(curr.convert(curr_from, curr_to, amount), 2)
    }

    return render_template("result.html", curr_from=curr_from_info, curr_to=curr_to_info)
