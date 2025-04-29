# LF search app

Set up a cron job to run this script daily:

Cron (Linux):
crontab -e

Add:
*/5 * * * * /home/lfeduca1/auto-update.sh
0 8 * * * /usr/bin/python3 /path/to/scrape.py >> /tmp/log.txt 2>&1

## run locally

First, navigate to your project directory (or wherever you want the virtual environment to be created):


```bash
pip3 install -r requirements.txt
```

```bash
python3 app.py
```
