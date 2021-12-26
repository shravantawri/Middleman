# Middleman

Warehouse ERP System


# DATABASE SETUP STEPS:
1. `create user middleman;`

2. `ALTER USER middleman SUPERUSER;`

3. `CREATE DATABASE middleman_development;`

https://blog.theodo.com/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/

python manage.py db migrate
python manage.py db upgrade



## Setup in ubuntu
1. `apt update`
2. `apt install python3-pip`
3. `pip3 install virtualenv`
4. `cd Middleman`
5. `virtualenv test_venv`
6. `source test_venv/bin/activate`
7. `pip3 install -r requirements.txt`
8. `flask run --host=0.0.0.0`
9. install postgres on ubuntu
10. `sudo apt-get install wget ca-certificates`
11. `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
12. `sudo sh -c echo "deb http://apt.postgresql.org/pub/repos/apt/ 'lsb_release -cs'-pgdg main" >> /etc/apt/sources.list.d/pgdg.list`
13. `sudo apt-get update`
14. `sudo apt-get install postgresql postgresql-contrib`
15. `sudo su - postgres`
16. `psql`
17.  SETUP DATABASE
18. `35.203.12.200:5000`

