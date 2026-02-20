
echo 'Which Port you want to check status ? '

read portnumber

lsof -i tcp:"$portnumber"
#or
lsof -t -i tcp:"$portnumber" | xargs kill

echo 'PORT DELETED SUCCESSFULLY '