import os
import datetime
from zipfile import ZipFile

# Original Author - Anurag Rana - https://github.com/anuragrana
#
# Modified by DrCBeatz - https://github.com/drCBeatz/
#
# place in home directory. schedule with task tab on pythonanywhere server.
# https://www.pythoncircle.com/post/360/how-to-backup-database-periodically-on-pythonanywhere-server/
#

BACKUP_DIR_NAME = "mysql_backups"
DAYS_TO_KEEP_BACKUP = 3
FILE_PREFIX = "my_db_backup_"
FILE_SUFFIX_DATE_FORMAT = "%Y%m%d%H%M%S"
USERNAME = "username"
SITENAME = "sitename"
# added above variable SITENAME since your database host address starts with your full pythonanywhere username ('sitename')
# which may be longer than your MySQL username, which is 16 characters max in length.
DBNAME = USERNAME+"$dbname"

# get today's date and time
timestamp = datetime.datetime.now().strftime(FILE_SUFFIX_DATE_FORMAT)
backup_filename = BACKUP_DIR_NAME+"/"+FILE_PREFIX+timestamp+".sql"

os.system("mysqldump --column-statistics=0 -u "+USERNAME+" -h "+SITENAME+".mysql.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces '"+DBNAME+"'  > "+backup_filename)
# add --column-statistics=0 for msqldump 8 (disables column statistics)
# also added --set-gtid-purged=OFF (for innoDB) and --no-tablespaces

# creating zip file
zip_filename = BACKUP_DIR_NAME+"/"+FILE_PREFIX+timestamp+".zip"
with ZipFile(zip_filename, 'w') as zip:
    zip.write(backup_filename, os.path.basename(backup_filename))

os.remove(backup_filename)

# deleting old files

list_files = os.listdir(BACKUP_DIR_NAME)

back_date = datetime.datetime.now() - datetime.timedelta(days=DAYS_TO_KEEP_BACKUP)
back_date = back_date.strftime(FILE_SUFFIX_DATE_FORMAT)

length = len(FILE_PREFIX)

# deleting files older than DAYS_TO_KEEP_BACKUP days
for f in list_files:
    filename = f.split(".")[0]
    if "zip" == f.split(".")[1]:
        suffix = filename[length:]
        if suffix < back_date:
            print("Deleting file : "+f)
            os.remove(BACKUP_DIR_NAME + "/" + f)



# restoring backup
# mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com 'yourusername$dbname'  < db-backup.sql

# reference
# https://help.pythonanywhere.com/pages/MySQLBackupRestore/
