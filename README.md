#Linux users importer

this little python script creates/updates users from a csv file

##How to use it:
- create a csv file with 3 columns (**user,password,group**) separated by comma, escaping char is ```"```, ex:
```
user,password,group
user1,pwd1,group1
user1,"passwordWithcomma,ex",group1
```
- run the script with root privilege
```
sudo ./import_users.py -i users.csv
```