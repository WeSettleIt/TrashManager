# TrashManager
Taking out the trash.

## Production
```
mkvirtualenv trash-manager
git clone https://github.com/WeSettleIt/TrashManager.git
cd TrashManager
pip install -r requirements.txt
cd ..
mkdir data
cp TrashManager/config.py TrashManager/trash-manager.db data
```

Edit content of `~/data/config.py`.

Change:

* SECRET_KEY
* DATABASE_URI

Edit wsgi.py file and add this:

```
import os

os.environ['TRASHMANAGER_SETTINGS'] = "/home/trashmanager/data/config.py"
```

## Database
```
sqlite3 my_database.sqlite < export.sqlite3.sql
```

or 

```
sqlite3> .read export.sqlite3.sql
```

