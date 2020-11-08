#!/usr/bin/env python
# Google Maplist Downloader
# Version: 1.2
# BF2 v1.50
# $c Tema567
# http://github.com/art567/bf2mapdown/

import io
import os
import sys
import csv
import urllib2
from urllib2 import urlopen, URLError, HTTPError

# Define types of rotation
ROTATION_ANY = 0
ROTATION_SMALL = 16
ROTATION_MEDIUM = 32
ROTATION_BIG = 64
ROTATION_LARGE = 128

# URL of Google Docs sheet:
URL = 'https://docs.google.com/spreadsheets/d/1D7wGcD4TLhRF_WUKvXmQ21S3Qn2T7NZovSdt-AglTLA/gviz/tq?tqx=out:csv&sheet={:name:}'

# File to save:
FILE = 'maplist_{:name:}.con'

# Maplist to download:
NAME = 'Wiror'

# Rotation to download:
ROTATION = ROTATION_ANY

class MapItem():
    def __init__(self):
        ''' This is map item constructor '''
        self.id = None
        self.valid = False
        self.mapname = None
        self.gamemode = None
        self.rotation = None
        self.size = None

    def setId(self, data):
        ''' This method sets the map item id '''
        i = data.strip('"').lower().replace(" ", "_")
        self.id = int('%s' % i)

    def setMap(self, data):
        ''' This method sets the map item mapname '''
        m = data.strip('"').lower().replace(" ", "_")
        # check if mapname is valid
        if m == "":
            # map is not valid!
            self.valid = False
            return
        else:
            # correcting gamemode names
            if (m.startswith('great_wall')):
                m = 'greatwall'
            elif (m.startswith('operation_harvest')):
                m = 'operationharvest'
            elif (m.startswith('operation_road')):
                m = 'operationroadrage'
            elif (m.startswith('operation_smoke')):
                m = 'operationsmokescreen'
            elif (m.startswith('wake_i')):
                m = 'wake_island_2007'
            # all looking good?
            self.mapname = str('%s' % m)
            self.valid = True

    def setGameMode(self, data):
        ''' This method sets the map item gamemode '''
        g = data.strip('"').lower().replace(" ", "_")
        # correcting gamemode names
        if (g.startswith('singleplayer') or g.startswith('single') or g.startswith('sp')):
            g = 'sp1'
        elif (g.startswith('conq') or g.startswith('cq') or g.startswith('inf')):
            g = 'gpm_cq'
        elif (g.startswith('coop') or g.startswith('bot')):
            g = 'gpm_coop'
        elif (g.startswith('capture') or g.startswith('ctf')):
            g = 'gpm_ctf'
        elif (g.startswith('death') or g.startswith('dm')):
            g = 'gpm_dm'
        elif (g.startswith('assault') or g.startswith('aas')):
            g = 'gpm_aas'
        elif (g.startswith('secure') or g.startswith('sec')):
            g = 'gpm_sec'
        elif (g.startswith('survival') or g.startswith('surv')):
            g = 'gpm_survival'
        elif (g.startswith('skirmish') or g.startswith('skirm')):
            g = 'gpm_skirmish'
        elif (g.startswith('insurgency') or g.startswith('ins')):
            g = 'gpm_insurgency'
        # all looking good?
        self.gamemode = str('%s' % g)
    
    def setSize(self, data):
        ''' This method sets the map item size '''
        s = data.strip('"').lower().replace(" ", "_")
        try:
            self.size = int('%s' % s)
        except:
            self.size = 0

    def setRotation(self, data):
        ''' This method sets the map item rotation '''
        g = data.strip('"').lower().replace(" ", "_")
        # correcting rotation type
        if (g.startswith('small') or g.startswith('inf') or g.startswith('16')):
            g = '16'
        elif (g.startswith('med') or g.startswith('medium') or g.startswith('32')):
            g = '32'
        elif (g.startswith('full') or g.startswith('big') or g.startswith('64')):
            g = '64'
        else:
            g = '0'
        # all looking good?
        self.rotation = int('%s' % g)

    def getLine(self):
        ''' This method returns BF2 maplist.con-compliant map line '''
        return ('maplist.append "%s" "%s" "%s"' % (self.mapname, self.gamemode, self.size))

    def isValid(self):
        ''' This is simple validation for map '''
        return self.valid

def fopen(infile):
    ''' This method allow us open file from disk into file variable '''
    f = None
    try:
        assert(type(infile) == '_io.TextIOWrapper')
    except AssertionError:
        f = open(infile,'r')
    return f

def dlfile(url):
    ''' This method allow us download file into file variable '''
    f = None
    # Open the url
    try:
        print "Downloading: " + url
        client = urlopen(url)
        f = client.read()

        # Open our local file for writing
        # with open(os.path.basename(url), "wb") as local_file:
        #    local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

    return f

def parse(f):
    ''' This method provides csv - to - con file parser '''
    m_items = []
    csvreader = csv.DictReader(f, delimiter=',',quotechar='|', dialect=csv.excel_tab)
    for row in csvreader:
        m = MapItem()
        m.setId(row['"#Nr"'])
        m.setMap(row['"Mapname"'])
        m.setGameMode(row['"Gamemode"'])
        m.setSize(row['"Mapsize"'])
        m.setRotation(row['"Rotation"'])
        # only append valid map items
        if m.isValid():
            m_items.append(m)
            #print('%s' % m.getLine())
    return m_items

def get_rotation(data):
    ''' This method returns numeric rotation identifier '''
    if ( type(data) is int ):
        n = data
        d = n
        if (d <= 0):
            n = 0
        elif (d > 0) and (d <= 16):
            n = 16
        elif (d > 16) and (d <= 32):
            n = 32
        else:
            n = 64
        return n
    elif ( type(data) is str ):
        s = data.strip('"').lower().replace(" ", "_")
        # correcting rotation type
        if (s.startswith('small') or s.startswith('inf') or s.startswith('16')):
            s = '16'
        elif (s.startswith('med') or s.startswith('medium') or s.startswith('32')):
            s = '32'
        elif (s.startswith('full') or s.startswith('big') or s.startswith('64')):
            s = '64'
        else:
            s = '0'
        # all looking good?
        return int('%s' % s)

def dl_maplist(name, rotation = ROTATION, url = URL, file = FILE ):
    ''' This method downloads single maplist from URL and write out result '''
    global ROTATION_ANY
    input_rot = get_rotation(rotation)
    input_url = url.replace("{:name:}", name.lower())
    out_fname = file.replace("{:name:}", name.lower())
    csvdata = dlfile(input_url)
    #print(csvdata.decode('utf-8'))
    csv = io.BytesIO(csvdata)
    #csv_fname="data.csv"
    #csv=fopen(csv_fname)
    maplist = parse(csv)
    confile = open(out_fname,'w')
    totalnum = 0
    print('Converting to BF2 format: \n - %d map lines found in maplist' % len(maplist))
    for m in maplist:
        if (input_rot == m.rotation or input_rot == ROTATION_ANY):
            totalnum += 1
            confile.write('%s\n' % m.getLine())
            #print('%s' % m.getLine())
    print(' - %d map lines to be used' % totalnum)
    print('Result written to %s' % out_fname)

def main():
    ''' This is main method of the program '''
    global ROTATION_ANY
    print('MapDown started')
    arg = 1
    argc = len(sys.argv)
    while (arg < argc):
        line = sys.argv[arg]
        larr = line.split(':')
        name = larr[0]
        rotation = ROTATION_ANY
        if (len(larr) > 1):
            rotation = larr[1]
        try:
            dl_maplist(name, rotation)
        except:
            pass
        arg += 1
    print('Finished.')

if __name__ == '__main__':
    main()
