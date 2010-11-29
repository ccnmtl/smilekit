SANDBOX_URL="http://kodos.ccnmtl.columbia.edu:7112"
PROD_URL="http://mysmilebuddy.ccnmtl.columbia.edu"

SITE_URL=$SANDBOX_URL
CACHEFILE_PATH="collection_tool/manifest.cache"
DIRECTORY="smilekit_files"
FILELIST_NAME="filelist.txt"
ERROR_FILE="download_errors.txt"

#initial cleanup:
rm -rf $DIRECTORY
rm $FILELIST_NAME
rm $ERROR_FILE


#retrieve cache:
wget $SITE_URL/$CACHEFILE_PATH -v -O $FILELIST_NAME -o $ERROR_FILE

# basic cleanup. Stolen from http://sed.sourceforge.net/sed1line.txt :
  #align flush left
  sed -i -e 's/^[ \t]*//' $FILELIST_NAME
  #delete blank lines
  sed -i -e '/^$/d'    $FILELIST_NAME
  #delete comments (lines starting with #)
  sed -i -e '/^#/d' $FILELIST_NAME

  #special lines to axe:
  sed -i -e '/^CACHE/d' $FILELIST_NAME
  sed -i -e '/^FALLBACK/d' $FILELIST_NAME
  sed -i -e '/^NETWORK/d' $FILELIST_NAME

#sort lines:
sort  $FILELIST_NAME  -o $FILELIST_NAME


#create a directory
mkdir $DIRECTORY
wget -i $FILELIST_NAME  -B  $SITE_URL -P $DIRECTORY -a $ERROR_FILE

# remove all the successes from the error file:
sed -i -e '/./{H;$!d;}' -e 'x;/ERROR/!d;' $ERROR_FILE

#print problematic urls to stdout:
grep '\-\-' download_errors.txt
