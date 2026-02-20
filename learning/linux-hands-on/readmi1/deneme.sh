#/bin/bash
read -p "bir dosya ismi girin" file_name
if [[ -f $file_name ]]
then
echo "$file_name isimde dosya var"
else
touch $file_name; echo "$file_name isminde dosya olusturuldu"
fi
