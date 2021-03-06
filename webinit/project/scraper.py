from craigslist import CraigslistHousing
from dateutil.parser import parse
import time
import project.scraper_setting 
from project.models import Listing
from project.base import session_factory

import datetime

def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistHousing(site=project.scraper_setting.CRAIGSLIST_SITE, area=area, category=project.scraper_setting.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': project.scraper_setting.MAX_PRICE, "min_price": project.scraper_setting.MIN_PRICE})
    results_count = 0
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=30)
    for i in gen:
        print(i)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        
      
        session = session_factory()

        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()
        
        # todo 1 not sure
        # session.close()
        
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
            session = session_factory()

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
                print("listing exception")
                session.close()
                return                

            results_count += 1
            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()
            session.close()

    return results_count


def do_scrape():
    """
    Runs the craigslist scraper, and save data to file.
    """

    # Get all the results from craigslist.
    all_results_count = 0
    for area in project.scraper_setting.AREAS:
        temp = scrape_area(area)
        all_results_count += temp
        print("  In {}: got {} results".format(area, temp))

    print("{}: got total {} results".format(time.ctime(), all_results_count))

