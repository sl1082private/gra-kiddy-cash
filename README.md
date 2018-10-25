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
