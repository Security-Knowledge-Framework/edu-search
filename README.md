# LF search app

Update this repo and changes are being pushed every 5 min to Prod.

Setup app:

```
sudo apt update
sudo apt install apache2 python3-certbot-apache
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
```

```
pip3 install -r requirements.txt
```

### Cron (Linux):
crontab -e

Add:
```
*/5 * * * * /home/lfeduca1/auto-update.sh
0 8 * * * cd /home/lfeduca1/edu-search/lf-app/app/converter/; /usr/bin/python3 scrape.py >> /tmp/log.txt 2>&1
```

### Apache Config with Static Folder & Reverse Proxy
```
sudo a2enmod proxy proxy_http rewrite headers
```

Ensure this is configured first in /etc/apache2/sites-available/edu-search.conf

```
<VirtualHost *:80>
    ServerName yourdomain.com

    # Static files
    Alias /static/ /home/lfeduca1/edu-search/lf-app/app/static/
    <Directory /home/lfeduca1/edu-search/lf-app/app/static/>
        Require all granted
    </Directory>

    # Proxy Gunicorn app
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    ErrorLog ${APACHE_LOG_DIR}/edu_search_error.log
    CustomLog ${APACHE_LOG_DIR}/edu_search_access.log combined
</VirtualHost>

```

Run:

```
sudo a2ensite edu-search
sudo systemctl reload apache2
```

###  Obtain and Install SSL Certificate

```
sudo certbot --apache -d lfeducation.org
```

Auto-Renew Cron Check
Certbot automatically installs a cron job, but to confirm:
```
sudo systemctl list-timers | grep certbot
```

To test renewal:
```
sudo certbot renew --dry-run
```

## run locally for debug

First, navigate to your project directory (or wherever you want the virtual environment to be created):


```
pip3 install -r requirements.txt
```

```
python3 app.py
```
