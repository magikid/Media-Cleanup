import urllib
from xml.etree.ElementTree import parse

language = 'en'
api_url = 'http://www.thetvdb.com/api/%s'
search_url = 'GetSeries.php?seriesname=%s'
apikey = 'D2B2FFFCEEDF7E83'
seriesname = 'LOST'

feed = urllib.urlopen(api_url % search_url % seriesname)
rss = parse(feed)

series = []
for element in rss.findall('data/series'):
	series.append({
		'title' : element.get('SeriesName'),
		'id' : element.get('seriesid'),
		'fa' : element.get('FirstAired')
	})
	print series

