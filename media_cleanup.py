import sys,os
from urllib2 import urlopen, URLError, HTTPError
from xml.dom import minidom

if len(sys.argv) >= 1:
	seriesname = "%s" % sys.argv[1]
else:
	seriesname = input("Show's Title? ")


language = 'en'
search_url = 'http://www.thetvdb.com/api/GetSeries.php?seriesname=%s'
apikey = 'D2B2FFFCEEDF7E83'
zip_url = 'http://www.thetvdb.com/api/D2B2FFFCEEDF7E83/series/%s/all/en.zip'
feed = 'tmp/selections.xml'
#tvdir = '/home/chrisj/TV/%s/'
tvdir = '/home/chrisj/Documents/projects/media_cleanup/tmp/%s'

try:
	f = urlopen(search_url % seriesname)
	print "Downloading..."
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
	local_zip = open(tvdir % sel_name + "/tvshow.nfo", "w")
	local_zip.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
	local_zip.write('<tvshow>\n')
	local_zip,write('\t<title>{0}</title>\n'.format(str(sel_name)))
	local_zip.write('\t<episodeguide>\n')
	local_zip.write('\t\t<url cache="{0}" .xml">http://www.thetvdb.com/api/D2B2FFFCEEDF7E83/series/{0}/all/en.zip</url>\n'.format(str(sel_id)))
	local_zip.write('\t</episodeguide>\n')
	local_zip.write('\t<id>{0}</id>\n'.format(str(sel_id)))
	local_zip.write('</tvshow>\n')
	local_zip.write('</xml>\n')
	local_zip.close()
except HTTPError, e:
	print "HTTP Error:", e.code
except URLError, e:
	print "URL Error: ", e.reason
