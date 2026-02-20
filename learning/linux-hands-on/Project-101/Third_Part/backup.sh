#!/bin/bash

#crontab -e yapiyoruz
#sonra acilan yere */5 * * * * /home/ec2-user/backup.sh


backup_files="/home/ec2-user/data" #/etc /boot /usr"
dest_backup="/mnt/backup"
backup_name=$(date +%F-%H-%M)
hostname=$(hostname -s)
archive_file="$hostname-$backup_name.tgz"

sudo tar -czf $dest_backup/$archive_file $backup_files

