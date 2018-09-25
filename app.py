# Import necessary libraries
from flask import Flask, render_template, redirect, jsonify
import pymongo
import scrape_mars
from pprint import pprint

# Create instance of Flask app
app = Flask(__name__)

# Create connection to MongoDB database `weather_db` and collection `forecasts`
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

# Create route that renders index.html template and finds documents from mongo
@app.route('/')
def home():
    mars = collection.find_one()
    return render_template('index.html', mars_data=mars)

# Create route that will trigger scrape functions
@app.route('/scrape')
def scrape():   
    
    news_data = scrape_mars.scrape_news()
    featured_image_url = scrape_mars.scrape_featured_image()
    mars_weather = scrape_mars.scrape_weather()
    facts_table = scrape_mars.scrape_facts()
    hemisphere_image_urls = scrape_mars.scrape_hems()

    print("THIS PRINTS")
    # Combine results into one dictionary
    mars_data = {
        'news_title': news_data['news_title'],
        'news_summary': news_data['news_summary'],
        'featured_image': featured_image_url,
        'weather': mars_weather,
        'facts': facts_table,
        'hemispheres': hemisphere_image_urls,
    }   

    print("ABOUT TO INSERT DATA")
    # Insert forecast into database
    pprint(mars_data, indent=4)
    collection.drop()
    collection.insert_one(mars_data)


    print("DATA HAS BEEN INSERTED")
    return mars_data

if __name__ == '__main__':
    app.run(debug=True)
