import time
import sys
import traceback
from datetime import datetime
from project.models import MyLog
from project.base import session_factory
import project.scraper
import project.scraper_setting

time.sleep(5)
while True:
	print("{}: Starting scrape cycle".format(time.ctime()))
	try:
		session = session_factory()
		now = MyLog(datetime.now())
		session.add(now)
		session.commit()
		session.close()

		project.scraper.do_scrape()
		print('scraper finish')
		
	except KeyboardInterrupt:
		print("Exiting....")
		sys.exit(1)
	except Exception as exc:
		print("Error with the scraping:", sys.exc_info()[0])
		traceback.print_exc()
	else:
		print("{}: Successfully finished scraping".format(time.ctime()))
	time.sleep(project.scraper_setting.SLEEP_INTERVAL)
