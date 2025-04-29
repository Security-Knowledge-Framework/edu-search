# LF search app

Set up a cron job to run this script daily:

Cron (Linux):
crontab -e

Add:
0 8 * * * /usr/bin/python3 /path/to/scrape.py >> /path/to/log.txt 2>&1

## run locally

To create and start a Python virtual environment, you can use the venv module that comes with Python 3. This module creates a self-contained environment 
that can have its own independent set of installed Python packages.

First, navigate to your project directory (or wherever you want the virtual environment to be created):

```bash
cd /path/to/your/project
python3 -m venv env
source env/bin/activate
```

```bash
pip3 install -r requirements.txt
```

```bash
python3 app.py
```

To exit the virtual environment when you're done, you can use the deactivate command:


```bash
deactivate
```

## OR

```bash
docker build -t lf .
```

```bash
docker run -p 5000:5000 lf
```
