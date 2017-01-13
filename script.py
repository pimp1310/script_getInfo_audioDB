import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
import re
import json
from resources.lib import localdb
from resources.lib import log
import time
import os

# Addon-Pfad auslesen
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')

# komm_path = addon_path + '\data\script.opened'

# def komm_aufbauen():
    # f = open(komm_path, 'w')
    # f.close()
    # while not os.path.isfile(komm_path):
        # pass

# def komm_beenden():
    # os.remove(komm_path)
    # while os.path.isfile(komm_path):
        # pass

# Warten bis andere Script-Ausfuehrungen beendet sind
# while os.path.isfile(komm_path):
    # pass

# komm_aufbauen()

# Lokale Datenbank laden
# localdb_path = addon_path + '\data\script.localdb.json'
# Database = localdb.load_db(localdb_path)

# Lokale Datenbank
log_path = addon_path + '\data\script.log.txt'

log.log(log_path, 'Start')

# Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# Kodi Sprache
language = xbmc.getLanguage(xbmc.ISO_639_1).upper()

# Window ID
windowid = 10135
xbmcgui.Window(windowid).clearProperties()

def exit():
    # komm_beenden()
    sys.exit(0)

def getParams(url):
    return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))

def NoneToStr(str):
    if str == None:
        return ''
    else:
        return str

def GetJASONFromUrl(URL):
    #Internetseite laden
    sock = urllib.urlopen(URL)
    source = sock.read()
    sock.close()

    # Json Daten einlesen
    return json.loads(source)

# Parameter auswerten
req = '?' + sys.argv[1]
param = getParams('script://' + sys.argv[0] + req)

# Wenn kein Request uebergeben wird script beenden
if not 'request' in param:
    exit()


# artistid=111282
# artistname=adele
# artistmbid=bfcc6d75-a6a5-4bc6-8282-47aec8531818
# albumid=2110394
# albummbid=058eb23b-5830-4ee6-9137-c73faded21c1
# trackid=34575152
# trackmbid=0a8e8d55-4b83-4f8a-9732-fbb5ded9f344


# Window(Home)
API_URL = ''
API_Key = 1
if param['request'] == 'getArtistDetails': 
    if 'artistname' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/search.php?s=' + param['artistname']
    elif 'artistid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/artist.php?i=' + param['artistid']
    elif 'artistmbid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/artist-mb.php?i=' + param['artistmbid']
elif param['request'] == 'getAlbumDetails':
    if 'artistname' in param and 'albumname' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/searchalbum.php?s=' + param['artistname'] + '&a=' + param['albumname']
    elif 'albumid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/album.php?m=' + param['albumid']
    elif 'albummbid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/album-mb.php?i=' + param['albummbid']
elif param['request'] == 'getTrackDetails':
    if 'artistname' in param and 'trackname' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/searchtrack.php?s=' + param['artistname'] + '&t=' + param['trackname']
    if 'trackid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/track.php?h=' + param['trackid']
    elif 'trackmbid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/track-mb.php?i=' + param['trackmbid']

# Script beenden sollte die URL nicht initialisiert sein
data = None
if API_URL == '':
    log.log(log_path, '[' + req + ']\t\t Fehler: Fuer die uebergebenen Parameter konnte keine passende API gefunden werden!')
    exit()
# else:
    # Aufruf vorhanden?
    # if req in Database['requests']:
        # Timestamp noch aktuell (7 Tage = 604800)
        # diff = time.time() - Database['requests'][req]['timestamp']
        # if diff > 604800:
            # Neue Daten laden da vorhandene Daten zu alt
            # log.log(log_path, '[' + req + ']\t\t Die Daten in der DB sind zu alt!')
            # tmp = GetJASONFromUrl(API_URL)
            # localdb.update(Database, req, tmp)
            # localdb.sav_db(localdb_path, Database)
            # data = Database['requests'][req]
        # else:
            # LocalDB benutzen
            # log.log(log_path, '[' + req + ']\t\t Daten aus DB geladen!')
            # data = Database['requests'][req]
    # else:
        # Neue Daten laden da noch nicht vorhanden
        # log.log(log_path, '[' + req + ']\t\t Daten in DB nicht gefunden!')
        # tmp = GetJASONFromUrl(API_URL)
        # localdb.update(Database, req, tmp)
        # localdb.sav_db(localdb_path, Database)
        # data = Database['requests'][req]


data = GetJASONFromUrl(API_URL)


def getArtistDetails(dat):
    #Daten vorhanden?
    if dat['artists'] == None:
        exit()

    #Properties setzen
    for k, v in dat['artists'][0].iteritems():
        xbmcgui.Window(windowid).setProperty('Artist_' + k, NoneToStr(v))
        
	# Sprache
    if 'strBiography' + language in dat['artists'][0]:
        if NoneToStr(dat['artists'][0]['strBiography' + language]) != '':
            xbmcgui.Window(windowid).setProperty('Artist_strBiography', dat['artists'][0]['strBiography' + language])
        else:
            if 'strBiographyEN' in dat['artists'][0]:
                xbmcgui.Window(windowid).setProperty('Artist_strBiography', NoneToStr(dat['artists'][0]['strBiographyEN']))
            else:
                xbmcgui.Window(windowid).setProperty('Artist_strBiography', 'Keine Biografie vorhanden!')
    elif 'strBiographyEN' in dat['artists'][0]:
        xbmcgui.Window(windowid).setProperty('Artist_strBiography', NoneToStr(dat['artists'][0]['strBiographyEN']))
    else:
        xbmcgui.Window(windowid).setProperty('Artist_strBiography', 'Keine Biografie vorhanden!')
		
def getAlbumDetails(dat):
    #Daten vorhanden?
    if dat['album'] == None:
        exit()

    #Properties setzen
    for k, v in dat['album'][0].iteritems():
        xbmcgui.Window(windowid).setProperty('Album_' + k, NoneToStr(v))
        
	# Sprache
    if 'strDescription' + language in dat['album'][0]:
        if NoneToStr(dat['album'][0]['strDescription' + language]) != '':
            xbmcgui.Window(windowid).setProperty('Album_strDescription', dat['album'][0]['strDescription' + language])
        else:
            if 'strDescriptionEN' in dat['album'][0]:
                xbmcgui.Window(windowid).setProperty('Album_strDescription', NoneToStr(dat['album'][0]['strDescriptionEN']))
            else:
                xbmcgui.Window(windowid).setProperty('Album_strDescription', 'Keine Beschreibung vorhanden!')
    elif 'strDescriptionEN' in dat['album'][0]:
            xbmcgui.Window(windowid).setProperty('Album_strDescription', NoneToStr(dat['album'][0]['strDescriptionEN']))
    else:
        xbmcgui.Window(windowid).setProperty('Album_strDescription', 'Keine Beschreibung vorhanden!')

def getTrackDetails(dat):
    #Daten vorhanden?
    if dat['track'] == None:
        exit()

    #Properties setzen
    for k, v in dat['track'][0].iteritems():
        xbmcgui.Window(windowid).setProperty('Track_' + k, NoneToStr(v))
		
# Entsprechenden Funktionen aufrufen
if param['request'] == 'getArtistDetails':
    getArtistDetails(data)
elif param['request'] == 'getAlbumDetails':
    getAlbumDetails(data)
elif param['request'] == 'getTrackDetails':
    getTrackDetails(data)

log.log(log_path, 'Ende')
# exit()