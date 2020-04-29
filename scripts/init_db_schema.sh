name=$(cat $0)
mysql -u $1 -p $2 ${name} < $4
echo "success" > $5
