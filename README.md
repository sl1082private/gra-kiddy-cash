$ python3 -m venv kkenv

NOTE: On some versions of Debian/Ubuntu initiating the virtual environment like this currently gives the following error:
Error: Command '['/home/eddie/Slask/tmp/venv/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1

To get around this, use the virtualenv command instead.

$ sudo apt install python-virtualenv
$ virtualenv --python=python3.6 kkenv


$ source kkenv/bin/activate
$ python3 -m pip install --upgrade pip
$ pip install -r requirements.txt 
# create database:
$ sudo su - postgres
postgres@somewhere:~$ createdb -O <user> <db_name>


### UBUNTU 20.04:

## https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

# install python3.6 environment using conda:
conda create -n kkenv python=3.6 pip
conda activate kkenv
pip install -r requirements.txt

# Then do the migrations:
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000.0:8000


## ##########################################
## 24 Nov 2024 (Sebastian)
## To create new database:
# check for existing postgres databases:
psql -d postgres
\l
# create new database
$ sudo su - postgres
postgres@somewhere:~$ createdb -O <user> <db_name>
# make django aware of new database and modify settings.py
modify settings.py and include new database name
# do migratons (check basekets/migrations and consider making a saftey copy (dunno if needed)
conda activate kkenv
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
# connect to project's admin page
http://192.168.178.53/admin
# and create event AND current_event
# then add vendors and kassier
add_vendors.ipynb
kassierer_anlegen.ipynb
print_credentials.ipynb
## ##########################################


# Modify/run add_vendors.ipynb in /home/sebastian/Computing/kra20/vendor_list to create and addvendors to event(s)

# Testing gunicorn (from ~/Computing/kra20/krakiddy):
gunicorn --bind 0.0.0.0:8000 cash_register.wsgi

#Check the Gunicorn socket’s logs by typing:
sudo journalctl -u gunicorn.socket


## Please select a value that is no more than XXX
## If you encounter this error, but the vendor number is good, you have to adjust 
## the correspoding "max_value" in the IntegerField in the file "krakiddy/baskets/forms.py"
## afterwards restart gunicorn
