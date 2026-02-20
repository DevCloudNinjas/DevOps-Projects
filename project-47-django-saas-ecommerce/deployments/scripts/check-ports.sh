echo 'Which Port you want to check status ? '

read portnumber

sudo lsof -i :"$portnumber"
