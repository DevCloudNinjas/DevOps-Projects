#!/bin/bash

if [[ ${UID} -ne 0 ]]; then
  echo "Du hast keine Root-Benutzerberechtigungen"
  exit 1
fi

CURRENT_DATE=$(date +"%Y%m%d-%H%M")
HOSTNAME=$(hostname)

echo $CURRENT_DATE $HOSTNAME

BACKUP_DIR="/mnt/backup"
mkdir -p $BACKUP_DIR

DIRECTORIES=("/home/ec2-user/data" "/etc" "/boot" "/usr")

for DIR in "${DIRECTORIES[@]}"; do
  DIR_NAME=$(basename "$DIR")
  BACKUP_FILE="${BACKUP_DIR}/${HOSTNAME}_${DIR_NAME}_${CURRENT_DATE}.tgz"

  tar -czf "${BACKUP_FILE}" -C "${DIR}" .

  echo "Backup of ${DIR} completed: ${BACKUP_FILE}"
done

#schreib in terminal crontab -e 
#dan fügt */5 * * * * /mnt/c/Users/Privat/Desktop/AWS/Github_Linux-Hands_on/Project-101/Third_Part/backup_2.sh