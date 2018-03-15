#!/bin/sh

USAGE="Usage: mogul-ssg.sh output_directory [app_url]"
DEFAULT_APPURL="http://localhost:3000/"

>&2 echo "Static Site Generator for Meteor Mogul"

OUTDIR="$1"
if [ "$OUTDIR" = "" ] ; then
	>&2 echo $USAGE
	>&2 echo "FATAL: Missing output directory argument"
	exit 1
fi
>&2 echo "OUTDIR=$OUTDIR"
APPURL="$2"
if [ "$APPURL" = "" ] ; then
	>&2 echo $USAGE
	>&2 echo "NOTICE: Using default application URL of $DEFAULT_APPURL"
	APPURL="$DEFAULT_APPURL"
fi
>&2 echo "APPURL=$APPURL"
WGET_OPTIONS="--directory-prefix=$OUTDIR --convert-links --convert-file-only --page-requisites --no-host-directories --recursive --level 1 $APPURL"
>&2 echo "WGET_OPTIONS=$WGET_OPTIONS"
wget $WGET_OPTIONS
python ./staticify-spa.py $OUTDIR
