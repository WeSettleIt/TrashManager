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
echo "export TRASHMANAGER_SETTINGS=/home/trashmanager/data/config.py" > ~/.virtualenvs/trash-manager/bin/postactivate
echo "unset TRASHMANAGER_SETTINGS" > ~/.virtualenvs/trash-manager/bin/predeactivate
```

Edit content of `~/data/config.py`.

Change:

* SECRET_KEY
* DATABASE_URI