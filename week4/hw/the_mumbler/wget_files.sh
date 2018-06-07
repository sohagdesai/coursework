#!/bin/bash
BASEDIR=/gpfs/gpfsfpo
HOSTNAME=$( hostname | cut -d'.' -f1)
DESTDIR=$BASEDIR/$HOSTNAME
echo $DESTDIR

echo "==== getting files on $HOSTNAME in directory $DESTDIR ===="
cd $DESTDIR
if [[ "gpfs1" = $HOSTNAME ]]; then
    files=$( seq 0 33 ) 
    #echo $files
elif [[ "gpfs2" = $HOSTNAME ]]; then
    files=$( seq 34 66 ) 
    #echo $files
elif [[ "gpfs3" = $HOSTNAME ]]; then
    files=$( seq 67 99 ) 
    #echo $files
fi

for i in $files
do
    echo "now getting file number $i..."
    wget http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20090715-$i.csv.zip
done

cd $BASEDIR
exit 1
