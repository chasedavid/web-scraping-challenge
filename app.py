#import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

mars_data = {}

#create flask instance
app = Flask(__name__)

#establish mongo connection
conn = 'mongodb://localhost:27017'
mongo = PyMongo(app, uri=conn, upsert=True)


mongo.db.collection.update({}, mars_data, upsert=True)
@app.route('/')
def home():
    #find one record
    mars_data = mongo.db.collection.find_one()
    
    #return template with data
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_info = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    mars_data = scrape_mars.scrape_img()
    mars_data = scrape_mars.scrape_weather()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hems()
    
    #return to home
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
