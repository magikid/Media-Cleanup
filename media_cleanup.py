import sys,os
from urllib2 import urlopen, URLError, HTTPError
from xml.dom import minidom

seriesname = "%s" % sys.argv[1]


language = 'en'
search_url = 'http://www.thetvdb.com/api/GetSeries.php?seriesname=%s'
apikey = 'D2B2FFFCEEDF7E83'
zip_url = 'http://www.thetvdb.com/api/D2B2FFFCEEDF7E83/series/%s/all/en.zip'
feed = 'tmp/selections.xml'
tvdir = '/home/chrisj/TV/%s'
#seriesname = 'LOST'

try:
	f = urlopen(search_url % seriesname)	print "Downloading..."
	local_file = open(feed, "w")
	local_file.write(f.read())
	local_file.close()
except HTTPError, e:
	print "HTTP Error:",e.code
except URLError, e:
	print "URL Error:",e.reason

rss = minidom.parse(feed)

shows = {'id': [], 'name': [], 'airdate': [], 'overview': []}

for elements in rss.getElementsByTagName('Series'):

		if len(elements.getElementsByTagName('seriesid')) > 0:
			shows['id'].append(elements.getElementsByTagName('seriesid')[0].firstChild.data)
		if len(elements.getElementsByTagName('SeriesName')) > 0:
			shows['name'].append(elements.getElementsByTagName('SeriesName')[0].firstChild.data)
		if len(elements.getElementsByTagName('FirstAired')) > 0:
			shows['airdate'].append(elements.getElementsByTagName('FirstAired')[0].firstChild.data)
		if len(elements.getElementsByTagName('Overview')) > 0:
			shows['overview'].append(elements.getElementsByTagName('Overview')[0].firstChild.data)

lens = []
# lens[0] is id, lens[1] is name, lens[2] is airdate, lens[3] is overview
lens.append(len(shows['id']))
lens.append(len(shows['name']))
lens.append(len(shows['airdate']))
lens.append(len(shows['overview']))
for x in range(9):
	junk = x+1
	output = '%i. ' % junk
	if x < lens[0]:
		output += shows['id'][x]
	output += " "
	if x < lens[1]:
		output += shows['name'][x]
	output += " "
	if x < lens[2]:
		output += shows['airdate'][x]
	output += " "
	if x < lens[3]:
		output += shows['overview'][x][:40]
	output += "..."
	print output
selection = input('Which one is it? ')
selection -= 1
sel_id = shows['id'][selection]
sel_name = shows['name'][selection]
if not(os.path.exists(tvdir % sel_name)):
	os.makedirs(tvdir % sel_name)
	
try:
	f = urlopen(zip_url % sel_id)
	local_zip = open(tvdir % shows['name'][selection], "w")
	local_zip.write(f.read())
	local_zip.close()
except HTTPError, e:
	print "HTTP Error:",e.code
except URLError, e:
	print "URL Error,e.reason
