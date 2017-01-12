import sys
import json
import os
from resources.lib import log
import xbmcaddon
import time

# Addon-Pfad auslesen
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')

# Lokale Datenbank
log_path = addon_path + '\data\localdb.log.txt'

def load_db(path):
    if os.path.isfile(path):
        with open(path, 'r+') as fp:
            return json.load(fp)
    else:
        d = dict()
        d['requests'] = dict()
        return d

def sav_db(path, db):
    with open(path, 'w+') as fp:
        json.dump(db, fp)

def update(db, req, dat):
    if req in db['requests']:
        # Updaten
        log.log(log_path, '[LOCALDB]\t[' + req + ']\t\t Daten fuer Request aktualisiert!')
        db['requests'][req] = dat
        db['requests'][req]['timestamp'] = time.time()
    else:
        # Hinzufuegen
        log.log(log_path, '[LOCALDB]\t[' + req + ']\t\t Neuer Request hinzugefuegt!')
        db['requests'][req] = dat
        db['requests'][req]['timestamp'] = time.time()