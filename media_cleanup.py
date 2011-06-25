import urllib
from xml.dom import minidom

language = 'en'
api_url = 'http://www.thetvdb.com/api/%s'
search_url = 'GetSeries.php?seriesname=%s'
apikey = 'D2B2FFFCEEDF7E83'
seriesname = 'LOST'

#feed = urllib.urlopen(api_url % search_url % seriesname)
feed = 'tmp/selections.xml'
rss = minidom.parse(feed)

shows = []

for elements in rss.getElementsByTagName('Series'):

		if len(elements.getElementsByTagName('seriesid')) > 0:
			shows.append('id': elements.getElementsByTagName('seriesid')[0].firstChild.data)
		if len(elements.getElementsByTagName('SeriesName')) > 0:
			shows.append('name': elements.getElementsByTagName('SeriesName')[0].firstChild.data)
		if len(elements.getElementsByTagName('FirstAired')) > 0:
			shows.append('airdate': elements.getElementsByTagName('FirstAired')[0].firstChild.data)


print shows
