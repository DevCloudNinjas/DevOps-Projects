#!/bin/bash
if [[ ${UID} -ne 0 ]]
then
    echo "Please run this script with root priviliges"
    exit 1 #root olmadigi icin programdan cikacak
fi

#Get the username
read -p "Enter username to create: " NAME

#get the description
read -p "Enter a comment to add your username: " DESCRIPTION

#get the password
read -sp "Enter your password" PASSWORD

#create an account
useradd -c ${DESCRIPTION} -m ${$NAME} 2 > /dev/null 
#bi sikinti olursa yani hata falan olursa bana gösterme cöpe at

#check to see if useradd command succeed
if [[ $? -ne 0 ]] #eger önceki kod düzgün calismadiysa
then
    echo "your code is wrong or this username already exist"
    exit 1
fi

#set the password
echo ${PASSWORD} | passwd --stdin ${NAME} # paswordu elinde tutuyor
#sonra istedigimiz isme atiyor

#check to see if useradd command succeed
if [[ $? -ne 0 ]] #eger önceki kod düzgün calismadiysa
then
    echo "this password couldn't set for this user "
    exit 1
fi

#force change to password
passwd -e $NAME #${NAME} yazsak da olur

