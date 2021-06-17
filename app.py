from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mtg_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mtg_card_predictor_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mtg_cards = mongo.db.mtg_cards.find_one()
    return render_template("index.html", mtg_cards=mtg_cards)

@app.route("/scrape")
def scraper():
    mtg_cards = mongo.db.mtg_cards
    mtg_cards_data = mtg_scrape.scrape()
    mtg_cards.update({}, mtg_cards_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)