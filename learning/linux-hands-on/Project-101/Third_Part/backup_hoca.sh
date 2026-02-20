#!/bin/bash
#sudo kullanicisinin uidsi 0
if [[ ${UID} -ne 0 ]]
then
    echo "Please run this script with root priviliges"
    exit 1 #root olmadigi icin programdan cikacak
fi

#Define the directories that you want to back-up
DIRECTORIES=("/home/ec2-user/data") #"/etc" "/boot" "/usr")

# define where you want to backup
BACKUP_DIR="/mnt/backup"

# Get the current date and time
DATE=$(date +%F_%H_%M)

#get the hostname
HOSTNAME=$(hostname -s)

#create back-up directory if it doesn't exist
if [[ ! -d $BACKUP_DIR ]] #backup_dir mevut degilse
then
    mkdir $BACKUP_DIR
fi

#Print the status message
echo
echo "We will back-up your ${DIRECTORIES[@]} to ${BACKUP_DIR}"
date +%H:%M
echo

for DIR in ${DIRECTORIES[@]}
do
FILENAME=$BACKUP_DIR/${HOSTNAME}-$DATE-$(basename $DIR).tgz

#create a backup file using tar
tar -czvf $FILENAME $DIR

#print the backup file
echo "backup file is creating $FILENAME"
done