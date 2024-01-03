#/bin/bash

FOLDERNAME="super-impt-stuff"
DIR="$PWD/$FOLDERNAME"
if [ ! -d "$DIR" ];
then
        mkdir $FOLDERNAME
        chmod 777 $FOLDERNAME
fi

cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 30 > $FOLDERNAME/priv-key
cp info.cgi.valid info.cgi
chmod 777 info.cgi
chmod 777 /usr/lib/cgi-bin