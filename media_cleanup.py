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

shows = {'id': [], 'name': [], 'airdate': []}

for elements in rss.getElementsByTagName('Series'):

		if len(elements.getElementsByTagName('seriesid')) > 0:
			shows['id'].append(elements.getElementsByTagName('seriesid')[0].firstChild.data)
		if len(elements.getElementsByTagName('SeriesName')) > 0:
			shows['name'].append(elements.getElementsByTagName('SeriesName')[0].firstChild.data)
		if len(elements.getElementsByTagName('FirstAired')) > 0:
			shows['airdate'].append(elements.getElementsByTagName('FirstAired')[0].firstChild.data)

lens = []
# lens[0] is id, lens[1] is name, lens[2] is airdate
lens.append(len(shows['id']))
lens.append(len(shows['name']))
lens.append(len(shows['airdate']))
for x in range(max(lens)):
	print "ID: %s" % shows['id'][x]
	print "Name: %s" % shows['name'][x]
	print "AirDate: %s" % shows['airdate'][x]
