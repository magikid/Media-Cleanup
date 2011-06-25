#!/bin/sh

language='en'
url='http://www.thetvdb.com/api/'
apikey='D2B2FFFCEEDF7E83/'
seriesname='Lost'

if [ ! -d "tmp" ]; then
	mkdir "tmp";
fi

#curl -o tmp/selections.xml  $url"GetSeries.php?seriesname="$seriesname
for tag in seriesid SeriesName FirstAired
do
OUT=`grep $tag 'tmp/selections.xml' | tr -d '\t' | sed 's/^<.*>\([^<].*\)<.*>$/\1/' `

eval ${tag}=`echo -ne \""${OUT}"\"`
done

seriesid_array=( `echo ${seriesid}` )
seriesname_array=( `echo ${SeriesName}` )
firtaired_array=( `echo ${FirstAired}` )

echo ${seriedid_array[@]}
echo ${seriesname_array[@]}
echo ${firstaired_array[@]}
