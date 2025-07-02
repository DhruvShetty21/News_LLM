from flask import Flask, render_template, request, redirect, url_for, flash
from news_ai_agent import process_and_send
from dotenv import load_dotenv
import os
load_dotenv()  # Only needed locally

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_unsafe_dev_key")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            category = request.form.get("category", "general")
            region = request.form.get("region")
            top_n = int(request.form.get("top_n", 10))
            sources = request.form.getlist("sources")
            status = process_and_send(email, category, region, top_n, sources)
            flash(status)
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
        return redirect(url_for("index"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)