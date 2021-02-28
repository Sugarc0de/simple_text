# SimpleText 
This program aims to auto-highlight potentially difficult vocabulary from a piece of article/news, based on the English level.

## Setup Flask App

1. Go to http://download.huzheng.org/zh_CN/, download the `lazyworm-ec` dictionary into the `backend` folder.
2. Unzip the `lazyworm-ec.dict.dz` to a file called `lazyword-ec`.
3. Uncomment the code and run `read_stardict.py`, it should generate `lazy_dict_idx.json`.

## Running it

First export your environment setting in terminal
```
export YOURAPPLICATION_SETTINGS=[dev|prod].settings.cfg
```

#### Local development:
```
cd backend && python3 app.py
```

#### EC2 instance:
```
cd backend && gunicorn --bind 127.0.0.1:5000 wsgi:app
```

### Notes:
new way to install scipy language pipeline:
`python -m spacy download en_core_web_sm`
