downloadwebpage
===============

a simple crawler to download webpages and organise the resources
and auto-backup the webpage file with css,js,images,change the links of the original html to redirect to the resources.


usage：
downloadwebpage.py -u url -d backuptime -o backup-directory

the directory will be this:
/backup-directory/back-up-timestamp
index.html
css/
js/
images/
