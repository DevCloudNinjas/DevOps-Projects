#!/bin/bash

if [[ ${UID} -ne 0 ]]; then
  echo "Du bist kein Root-Benutzer. Versuchen Sie es erneut mit sudo."
  exit 1
fi

read -p "Dein Accountname: " USERNAME
read -p "Dein Beschreibung: " DESCRIPTION
read -sp "Dein Passwort: " PASSWORD
read -p "Möchtest du ein Home-Verzeichnis erstellen? (Y/n): " CHOICE

if [[ ${CHOICE} == 'Y' || ${CHOICE} == 'y' ]]; then
  useradd -c "${DESCRIPTION}" -m ${USERNAME} 2> /dev/null
else
  useradd -c "${DESCRIPTION}" ${USERNAME}
fi

echo "${USERNAME}:${PASSWORD}" | chpasswd

if [[ $? -ne 0 ]]; then
  echo "Es gibt ein Problem mit dem Passwort."
  exit 1
fi

passwd -e ${USERNAME}
