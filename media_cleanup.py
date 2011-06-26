#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys,os
from urllib2 import urlopen, URLError, HTTPError
from xml.dom import minidom
################################
#   Vars you should edit       #
################################

# Make sure your tvdir has a trailing slash and ends with %s
tvdir = '/home/chrisj/TV/%s'
tmpdir = 'tmp'

#################################
#  Don't edit below here unless #
#  you know what you're doing   #
#################################

base_url = 'http://www.thetvdb.com/'
search_url = 'http://www.thetvdb.com/api/GetSeries.php?seriesname=%s'
feed = '{0}/selections.xml'.format(str(tmpdir))



if len(sys.argv) > 1:
	if sys.argv[1] == '-h' or sys.argv[1] == '--help':
		print ''
		print 'Usage: python media_cleanup.py TVShowDirectory'
		print 'Takes one argument, your TV show directory, which can be manually configured in the script.'
		print ''
		sys.exit()
	else:
		tvdir = sys.argv[1] + '%s'


if not(os.path.exists(tmpdir)):
	os.makedirs(tmpdir)

print "Finding titles..."
seriesname = []

for f in os.listdir(tvdir % ''):
	if os.path.isdir(os.path.join(tvdir % '', f)):
		seriesname.append(f)

seriesname.sort()
for x in range(len(seriesname)):
	yesno = raw_input('Found {0}.  Work with this show? (Y/n) '.format(seriesname[x]))
	if yesno == 'n' or yesno == 'N':
		continue
	print "Downloading possible matches..."
	safe_url = seriesname[x]
	safe_url = safe_url.replace("%", "%25")
	safe_url = safe_url.replace("$", "%26")
	safe_url = safe_url.replace("+", "%2B")
	safe_url = safe_url.replace(",", "%2C")
	safe_url = safe_url.replace("/", "%2F")
	safe_url = safe_url.replace(":", "%3A")
	safe_url = safe_url.replace(";", "%3B")
	safe_url = safe_url.replace("=", "%3D")
	safe_url = safe_url.replace("?", "%3F")
	safe_url = safe_url.replace("@", "%40")
	safe_url = safe_url.replace(" ", "%20")
	safe_url = safe_url.replace("'", "%22")
	safe_url = safe_url.replace("<", "%3C")
	safe_url = safe_url.replace(">", "%3E")
	safe_url = safe_url.replace("#", "%23")
	safe_url = safe_url.replace("{", "%7B")
	safe_url = safe_url.replace("}", "%7D")
	safe_url = safe_url.replace("|", "%7C")
	safe_url = safe_url.replace("\\", "%5C")
	safe_url = safe_url.replace("^", "%5E")
	safe_url = safe_url.replace("~", "%7E")
	safe_url = safe_url.replace("[", "%5B")
	safe_url = safe_url.replace("]", "%5D")
	safe_url = safe_url.replace("`", "%60")
	try:
		f = urlopen("{0}".format(search_url % safe_url))
		local_file = open(feed, "w+b")
		local_file.write(f.read())
		local_file.close()
	except HTTPError, e:
		print "HTTP Error:",e.code
	except URLError, e:
		print "URL Error:",e.reason

	rss = minidom.parse(feed)

	numselections = len(rss.getElementsByTagName('Series'))
	if numselections > 15:
		print "Found more than 15 similar titles."		
		numselections = 15
	else if numselections < 1:
		print "Nothing found with that title."
		yesno = raw_input("Do you want to continue? (Y/n) ")
		if not(yesno == "N" or yesno == "n")
			continue
		else
			break

	else:
		print "Found {0} similar titles.".format(numselections)	

	shows = {'id': [], 'name': [], 'airdate': [], 'overview': [], 'banner': []}

	for elements in rss.getElementsByTagName('Series'):

			if len(elements.getElementsByTagName('seriesid')) > 0:
				shows['id'].append(elements.getElementsByTagName('seriesid')[0].firstChild.data)
			if len(elements.getElementsByTagName('SeriesName')) > 0:
				shows['name'].append(elements.getElementsByTagName('SeriesName')[0].firstChild.data)
			if len(elements.getElementsByTagName('FirstAired')) > 0:
				shows['airdate'].append(elements.getElementsByTagName('FirstAired')[0].firstChild.data)
			if len(elements.getElementsByTagName('Overview')) > 0:
				shows['overview'].append(elements.getElementsByTagName('Overview')[0].firstChild.data)
			if len(elements.getElementsByTagName('banner')) > 0:
				shows['banner'].append(elements.getElementsByTagName('banner')[0].firstChild.data)

	if numselections > 0:
		for x in range(numselections):
			junk = x+1
			output = '%i. ' % junk
			if x < len(shows['id']):
				output += shows['id'][x]
			output += " "
			if x < len(shows['name']):
				output += shows['name'][x]
			output += " "
			if x < len(shows['airdate']):
				output += shows['airdate'][x]
			output += " "
			if x < len(shows['overview']):
				output += shows['overview'][x][:40]
			output += "..."
			print output
		selection = raw_input('Which one is it? ')
		selection = int(selection) - 1
		sel_id = shows['id'][selection]
		sel_name = shows['name'][selection]
		sel_banner = shows['banner'][selection]
		sel_overview = shows['overview'][selection]
		sel_airdate = shows['airdate'][selection]
	else:
		sel_id = shows['id'][0]
		sel_name = shows['name'][0]
		sel_banner = shows['banner'][0]
		sel_overview = shows['overview'][0]
		sel_airdate = shows['airdate'][0]

	momentoftruth = raw_input('Do you want me to write {0}{1}'.format(tvdir % sel_name, "/tvshow.nfo? (Y/n)? "))
	momentoftruth2 = raw_input('Do you want my to get the banner? (Y/n)'))
	if not(momentoftruth2 == 'n' or momentoftruth2 == 'N'):
		if not(os.path.exists(tvdir % sel_name)):
			os.makedirs(tvdir % sel_name)
		try:
			f = urlopen("{0}{1}{3}".format(base_url, "banners/", sel_banner))
			local_image = open(tvdir % sel_name + "/folder.jpg", "w+b")
			local_image.write(f.read())
			local_image.close()
		except HTTPError, e:
			print "HTTP Error:", e.code
		except URLError, e:
			print "URL Error: ", e.reason
		except IOError, e:
			print "File Error", e.strerror

	if not(momentoftruth == 'n' or momentoftruth == 'N'):
		if not(os.path.exists(tvdir % sel_name)):
			os.makedirs(tvdir % sel_name)
	
		try:

			local_zip = open(tvdir % sel_name + "/tvshow.nfo", "w+b")
			local_zip.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
			local_zip.write('<tvshow>\n')
			local_zip.write('\t<title>{0}</title>\n'.format(sel_name))
			local_zip.write('\t<episodeguide>\n')
			local_zip.write('\t\t<url cache="{0}.xml">http://www.thetvdb.com/api/D2B2FFFCEEDF7E83/series/{0}/all/en.zip</url>\n'.format(sel_id))
			local_zip.write('\t</episodeguide>\n')
			local_zip.write('\t<id>{0}</id>\n'.format(sel_id))
			local_zip.write('\t<thumb>{0}banners/{1}</thumb>\n'.format(base_url,sel_banner))
			local_zip.write('\t<plot>{0}</plot>\n'.format(sel_overview.encode('ascii', 'xmlcharrefreplace')))
			local_zip.write('\t<premiered>{0}</premiered>\n'.format(sel_airdate))
			local_zip.write('</tvshow>\n')
			local_zip.write('</xml>\n')
			local_zip.close()
		except IOError, e:
			print "File Error", e.strerror
	else:
		yesno = raw_input("Print out XML file instead? (Y/n)")
		if not(yesno == 'n' or yesno == 'N'):
			print "Printing XML file: \n"
			print '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
			print '<tvshow>'
			print '\t<title>{0}</title>'.format(sel_name)
			print '\t<episodeguide>'
			print '\t\t<url cache="{0}.xml">http://www.thetvdb.com/api/D2B2FFFCEEDF7E83/series/{0}/all/en.zip</url>'.format(sel_id)
			print '\t</episodeguide>'
			print '\t<id>{0}</id>'.format(sel_id)
			print '\t<thumb>{0}banners/{1}</thumb>\n'.format(base_url,sel_banner)
			print '\t<plot>{0}</plot>'.format(sel_overview.encode('ascii', 'xmlcharrefreplace'))
			print '\t<premiered>{0}</premiered>'.format(sel_airdate)
			print '</tvshow>'
			print '</xml>'
		else:
			continue
