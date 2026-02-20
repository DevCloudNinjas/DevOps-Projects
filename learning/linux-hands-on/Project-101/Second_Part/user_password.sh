#!/bin/bash

read -p "Accountname girin: " USERNAME
read -p "Comment girin: " DESCRIPTION
read -p "Home directory ister misiniz Y/N" SECIM
if [ $SECIM == "Y" ]  || [ $SECIM == "y" ]
then
useradd -m -c "$DESCRIPTION" $USERNAME
else
useradd -c "$DESCRIPTION" $USERNAME
fi
passwd $USERNAME
passwd -e $USERNAME #Force the user to change their password at first login
