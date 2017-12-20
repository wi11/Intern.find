import scraper

from flask import *
import pandas as pd
app = Flask(__name__)

@app.route("/")
def display_tables():
    max_results_per_state = 10
    state_set = ["California", "New York", "Washington", "Illinois", "Texas"]
    data = {"Job Title":[], "Company":[], "Location":[]}
    dataframe = scraper.scrape(max_results_per_state, state_set, data)
    print "HI"
    return render_template("table.html", dataframe=dataframe.to_html())

if __name__ == "__main__":
    app.run(debug=True)


