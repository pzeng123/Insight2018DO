from craigslist import CraigslistHousing
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
#from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
#from slackclient import SlackClient
import time
import settings
from datetime import datetime


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:5590503@127.0.0.1:3306/listings"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120), unique=True)
    timestr = db.Column(db.DateTime)
    geotag = db.Column(db.String(120))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    name = db.Column(db.Text)
    price = db.Column(db.Float)
    location = db.Column(db.String(120))
    cl_id = db.Column(db.String(120), unique=True)
    area = db.Column(db.Text)


    def __repr__(self):
        return '<Link: %r>' % self.link

db.create_all()


def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': settings.MAX_PRICE, "min_price": settings.MIN_PRICE})

    results = []
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue

        listing = Listing.query.filter_by(cl_id=result["id"]).first()


        # Don't store the listing if it already exists.
        if listing is None:
            lat = 0
            lon = 0
            if result["geotag"] is None:
                continue
            # Assign the coordinates.
            lat = result["geotag"][0]
            lon = result["geotag"][1]

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.


#            print(type(result["area"].encode('utf-8')))
#            print(result["url"])
#            print(type(result["name"].encode('utf-8')))
#            print(result["area"])
            err = 0
            try:
                listing = Listing( 
                    link=result["url"],
                    timestr=parse(result["datetime"]), #.strftime('%s')),
                    name = result["name"], 
                    lat=lat, 
                    lon=lon, 
                    price=price,
                    cl_id=str(result["id"]),
                    area=result["area"],
                )
            except pymysql.err.InternalError:
                err += 1
                continue
            except Exception:
                pass

            

            # Save the listing so we don't grab it again.
            db.session.add(listing)
            db.session.commit()

    return results

def do_scrape():
    """
    Runs the craigslist scraper
    """

    # Get all the results from craigslist.

    all_results = []
    for area in settings.AREAS:
        all_results += scrape_area(area)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))




if __name__ == "__main__":
    do_scrape()

