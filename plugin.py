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
from random import randint
from time import sleep

# Argumente
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

# sleep(float(addon_handle * 30) / 100)

# Addon-Pfad auslesen
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')

#komm_path = addon_path + '\data\plugin.opened'

# def komm_aufbauen():
    # f = open(komm_path, 'w')
    # f.close()
    # while not os.path.isfile(komm_path):
        # pass

# def komm_beenden():
    # os.remove(komm_path)
    # while os.path.isfile(komm_path):
        # pass

# Warten bis andere Plugin-Ausfuehrungen beendet sind
# while os.path.isfile(addon_path + '\data\plugin.opened'):
    # pass

# komm_aufbauen()

# Lokale Datenbank
# localdb_path = addon_path + '\data\plugin.localdb.json'
# Database = localdb.load_db(localdb_path)

# Lokale Datenbank
log_path = addon_path + '\data\plugin.log.txt'

log.log(log_path, 'Start')

# Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# Inhalt setzen
xbmcplugin.setContent(addon_handle, 'audio')

# Kodi Sprache
language = xbmc.getLanguage(xbmc.ISO_639_1).upper()

def exit():
    # komm_beenden()
    sys.exit(0)

def addzerotime(strTime):
    if len(strTime) == 1:
        return '0' + strTime
    else:
        return strTime

def format_ms(ms):
    milliseconds = float(int(ms))
    minutes = int(milliseconds / float(60000))
    seconds = int((milliseconds - (minutes * float(60000))) / 1000)
    return str(minutes) + 'min ' + addzerotime(str(seconds)) + 'sec'
    
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
    
# https://www.youtube.com/watch?v=Tj0rO7P6TH0
# https://youtu.be/Tj0rO7P6TH0
def getYoutubeVidID(url):
    if url.find('youtu.be') == -1:
        return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
    else:
        temp = dict()
        temp['v'] = url.replace('https://youtu.be/', '')
        return temp

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
req = sys.argv[2]
param = getParams('plugin://getInfo_AudioDB' + req)

if not 'request' in param:
    log.log(log_path, 'Fehler: Der Parameter \'request\' fehlt!')
    exit()
    
# artistid=111282
# artistname=adele
# artistmbid=bfcc6d75-a6a5-4bc6-8282-47aec8531818
# albumid=2110394
# albummbid=058eb23b-5830-4ee6-9137-c73faded21c1
# trackid=34575152
# trackmbid=0a8e8d55-4b83-4f8a-9732-fbb5ded9f344

GET_LOCAL = False   
API_URL = ''
API_Key = 1

if param['request'] == 'getAlbumDetails': # Content
    if 'artistname' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/searchalbum.php?s=' + param['artistname'] # Content
    elif 'artistid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/album.php?i=' + param['artistid'] # Content   
elif param['request'] == 'getTrackDetails': # Content
    if 'albumid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/track.php?m=' + param['albumid'] # Content
elif param['request'] == 'getArtistDiscography': # Content
    if 'artistname' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/discography.php?s=' + param['artistname'] # Content
    elif 'artistmbid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/discography-mb.php?s=' + param['artistmbid'] # Content
elif param['request'] == 'getMusicVideos': # Content
    if 'artistid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/mvid.php?i=' + param['artistid'] # Content
    elif 'artistmbid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/mvid-mb.php?i=' + param['artistmbid'] # Content
elif param['request'] == 'getTop10Tracks': # Content
    if 'artistname' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/track-top10.php?s=' + param['artistname'] # Content
    elif 'artistmbid' in param:
        API_URL = 'http://www.theaudiodb.com/api/v1/json/' + str(API_Key) + '/track-top10-mb.php?s=' + param['artistmbid'] # Content

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

def getAlbumDetails(dat):
    #Daten vorhanden?
    if dat['album'] == None:
        log.log(log_path, '[' + req + '] Fehler: Der Aufruf getAlbumDetails hat keinen Datensatz zurueckgegeben!')
        exit()
    
    for val in dat['album']:
        #DirectoryItem erzeugen
        url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
        li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')

        for k, v in val.iteritems():
            li.setProperty(k, NoneToStr(v))
        
		# Sprache > 'strDescription'
        if 'strDescription' + language in val:
            if NoneToStr(val['strDescription' + language]) != '':
                li.setProperty('strDescription', val['strDescription' + language])
            else:
                if 'strDescriptionEN' in val:
                    li.setProperty('strDescription', NoneToStr(val['strDescriptionEN']))
                else:
                    li.setProperty('strDescription', 'Keine Beschreibung vorhanden!')
        elif 'strDescriptionEN' in val:
            li.setProperty('strDescription', NoneToStr(val['strDescriptionEN']))
        else:
            li.setProperty('strDescription', 'Keine Beschreibung vorhanden!')

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def getTrackDetails(dat):
    #Daten vorhanden?
    if dat['track'] == None:
        log.log(log_path, '[' + req + '] Fehler: Der Aufruf getTrackDetails hat keinen Datensatz zurueckgegeben!')
        exit()
        
    for val in dat['track']:
        #DirectoryItem erzeugen
        url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
        li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')

        for k, v in val.iteritems():
            li.setProperty(k, NoneToStr(v))
        
        if 'intDuration' in val:
            if NoneToStr(val['intDuration']) != '':
                li.setProperty('strDuration', format_ms(val['intDuration']))

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def getArtistDiscography(dat):
    #Daten vorhanden?
    if dat['album'] == None:
        log.log(log_path, '[' + req + '] Fehler: Der Aufruf getArtistDiscography hat keinen Datensatz zurueckgegeben!')
        exit()
        
    for val in dat['album']:
        #DirectoryItem erzeugen
        url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
        li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')

        for k, v in val.iteritems():
            li.setProperty(k, NoneToStr(v))
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def getMusicVideos(dat):
    #Daten vorhanden?
    if dat['mvids'] == None:
        log.log(log_path, '[' + req + '] Fehler: Der Aufruf getMusicVideos hat keinen Datensatz zurueckgegeben!')
        exit()
        
    for val in dat['mvids']:
        #DirectoryItem erzeugen
        url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
        li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')

        for k, v in val.iteritems():
            li.setProperty(k, NoneToStr(v))

        youtube = getYoutubeVidID(val['strMusicVid'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + youtube['v'], listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def getTop10Tracks(dat):
    #Daten vorhanden?
    if dat['track'] == None:
        log.log(log_path, '[' + req + '] Fehler: Der Aufruf getTop10Tracks hat keinen Datensatz zurueckgegeben!')
        exit()
        
    for val in dat['track']:
        #DirectoryItem erzeugen
        url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
        li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')

        for k, v in val.iteritems():
            li.setProperty(k, NoneToStr(v))
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

if param['request'] == 'getAlbumDetails':
    getAlbumDetails(data)
elif param['request'] == 'getTrackDetails':
    getTrackDetails(data)
elif param['request'] == 'getArtistDiscography':
    getArtistDiscography(data)
elif param['request'] == 'getMusicVideos':
    getMusicVideos(data)
elif param['request'] == 'getTop10Tracks':
    getTop10Tracks(data)

log.log(log_path, 'Ende')
# exit()