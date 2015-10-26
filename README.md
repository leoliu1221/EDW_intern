# EDW_intern
Intern code at EDW

Local installation instructions: 
Clone the whole repository
Install python>=2.6
run pip install -r requirements.txt
run python api.py
your local server should be running. 

Deployment steps: (PLEASE SEE EDIT FOR EXTRA STEPS FOR DEPLOYING WITH VIRTUALENV)
1.1. Install mod_wsgi
apt-get install libapache2-mod-wsgi
or
pkg_add -r mod_wsgi
or 
https://code.google.com/p/modwsgi/wiki/InstallationOnWindows if we have windows server

Instructions on deployment

1.2 Install python 2.7 -- just make sure you have pip installed. We are going to need pip in step 3. 

2. cd into  /var/www/ folder on server and git clone https://github.com/leolincoln/EDW_intern.git

3. cd into EDW_intern  and then use pip install -r requirements.txt  #this step we are installing the python package system wide for easy usage. 

4. follow along this:http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/#installing-mod-wsgi

for detail of 4: 
4.1: modify the apache configuration file. 
If not windows machine, then 
<VirtualHost *>
    ServerName example.com

    WSGIDaemonProcess yourapplication user=user1 group=group1 threads=5
    WSGIScriptAlias / /var/www/EDW_intern/api.wsgi

    <Directory /var/www/EDW_intern>
        WSGIProcessGroup EDW_intern
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>

if windows then:
<VirtualHost *>
        ServerName example.com
        WSGIScriptAlias / C:\yourdir\api.wsgi
        <Directory C:\yourdir>
                Order deny,allow
                Allow from all
        </Directory>
</VirtualHost>

Lastly make sure the website works and we will send you the original seed datafiles for key and value confidence calculations
EDIT:
1. if using virtual env make sure pip install -r requirements.txt after activate virtualenv, and make sure virtualenv is under the application folder. 
2. if using virtual env, after step1, you will need to modify the wsgi file by adding import sys;sys.path.insert(0,"flask app root path") before import app as application

Some more examples that i found super useful:
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
