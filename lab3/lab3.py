from flask import Flask, render_template, request


app = Flask(__name__)


def calculate_payment(credit_sum, rate, months):
    if credit_sum is None or rate is None or months is None:
        return
    try:
        return credit_sum * ((rate * (1 + rate) ** months) / ((1 + rate) ** months - 1))
    except ZeroDivisionError:
        return 0.0


@app.route("/")
def index():
    return render_template("index.html", error=None)


@app.route("/", methods=["post", "get"])
def form():
    error = {
        "credit_sum_error": False,
        "rate_error": False,
        "months_error": False,
    }
    if request.method == "POST":
        try:
            credit_sum = float(request.form.get("credit_sum"))
            if credit_sum < 0:
                error["credit_sum_error"] = True
                credit_sum = None
        except ValueError:
            error["credit_sum_error"] = True
            credit_sum = None

        try:
            rate = float(request.form.get("rate")) / 12 / 100
            if rate < 0:
                error["rate_error"] = True
                rate = None
        except ValueError:
            error["rate_error"] = True
            rate = None

        try:
            months = int(request.form.get("years")) * 12
            if months < 0:
                error["months_error"] = True
                months = None
        except ValueError:
            error["months_error"] = True
            months = None

    return render_template("index.html", error=error, ans=calculate_payment(credit_sum, rate, months))


if __name__ == "__main__":
    app.run()
