
# database container name: postgres
SQLALCHEMY_DATABASE_URI = 'postgresql://mydbuser:password@postgres/mydb' 

## Price

# The minimum rent you want to pay per month.
MIN_PRICE = 500

# The maximum rent you want to pay per month.
MAX_PRICE = 3500

## Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'boston'

# What Craigslist subdirectories to search on.
# For instance, https://sfbay.craigslist.org/eby/ is the East Bay, and https://sfbay.craigslist.org/sfc/ is San Francisco.
# You only need the last three letters of the URLs.
# AREAS = ["eby", "sfc", "sby", "nby", "pen"]
# for boston: gbs nwb bmw nos sob
AREAS = ["gbs", "nwb", "bmw"]

## Search type preferences

# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
# aap: all apartments, nfa:all no-fee apartments, abo:by-owner apartments only
CRAIGSLIST_HOUSING_SECTION = 'aap'

## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 1 * 60 * 60 # 1 hours


# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

