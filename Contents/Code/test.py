from lxml import etree
import urllib2
import common
import urlparse
import re
import time
import datetime



MovieName='Maya'
url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
    'v=1.0&q='+MovieName+' tamil movie online')

request = urllib2.Request(url, None, {'Referer': common.Reffer})
response = urllib2.urlopen(request)

# Process the JSON string.
results = simplejson.load(response)
Log(results)


#//*[contains(@src,'www.youtube.com')]

