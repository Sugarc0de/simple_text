# SimpleText 
This program aims to auto-highlight potentially difficult vocabulary from a piece of article/news, based on the English level.

## Setup Flask App

1. Go to http://download.huzheng.org/zh_CN/, download the `lazyworm-ec` dictionary into the `backend` folder.
2. Unzip the `lazyworm-ec.dict.dz` to a file called `lazyword-ec`.
3. Uncomment the code and run `read_stardict.py`, it should generate `lazy_dict_idx.json`.

## Running it

In backend folder, run `python app.py`