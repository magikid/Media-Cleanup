import urllib
from xml.dom import minidom

language = 'en'
api_url = 'http://www.thetvdb.com/api/'
apikey = 'D2B2FFFCEEDF7E83'
seriesname = 'LOST'

def series_id(seriesname):
	url = api_url + 'GetSeries.php?seriesname=%s' % seriesname
	dom = minidom.parse(urllib.urlopen(url))
	series = []
	for node in dom.getElementsByTagName('')
