from craigslist import CraigslistHousing
from dateutil.parser import parse
import time
import project.scraper_setting 
from project.models import Listing
from project import db
import datetime

def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistHousing(site=project.scraper_setting.CRAIGSLIST_SITE, area=area, category=project.scraper_setting.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': project.scraper_setting.MAX_PRICE, "min_price": project.scraper_setting.MIN_PRICE})

    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=30)
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

            
            print(parse(result["datetime"]))
            try:
                listing = Listing(
                    link=result["url"],
                    ptime=parse(result["datetime"]),
                    lat=lat,
                    lon=lon,
                    name=result["name"],
                    price=price,
                    location=result["where"],
                    cl_id=str(result["id"]),
                    area=result["area"],
                )
            except Exception:
                return
                

            # Save the listing so we don't grab it again.
            db.session.add(listing)
            db.session.commit()


def do_scrape():
    """
    Runs the craigslist scraper, and save data to file.
    """

    # Get all the results from craigslist.
    all_results = []
    for area in project.scraper_setting.AREAS:
        results = scrape_area(area)
        print(results)
        print(all_results)
        if results:
            all_results += results

    print("{}: Got {} results".format(time.ctime(), len(all_results)))


