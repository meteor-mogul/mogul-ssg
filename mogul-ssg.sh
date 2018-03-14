#!/bin/sh

USAGE="Usage: mogul-ssg.sh output_directory app_url"
DEFAULT_APPURL="http://localhost:3000/"

echo "Static Site Generator for Meteor Mogul"

OUTDIR="$1"
if [ "$OUTDIR" = "" ] ; then
	echo $USAGE
	echo "FATAL: Missing output directory argument"
	exit 1
fi
echo "OUTDIR=$OUTDIR"
APPURL="$2"
if [ "$APPURL" = "" ] ; then
	echo $USAGE
	echo "ASSUMING: Using default application URL of $DEFAULT_APPURL"
	APPURL="$DEFAULT_APPURL"
fi
echo "APPURL=$APPURL"
WGET_OPTIONS="--directory-prefix=$OUTDIR --convert-links --convert-file-only --page-requisites --no-host-directories --recursive --level 1 $APPURL"
echo "WGET_OPTIONS=$WGET_OPTIONS"
wget $WGET_OPTIONS
