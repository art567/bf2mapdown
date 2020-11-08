#!/usr/bin/env python
# Google Maplist Downloader
# Version: 1.0
# BF2 v1.50
# $c Tema567
# http://github.com/art567/mapdown/

import io
import os
import sys
import csv
import urllib2
from urllib2 import urlopen, URLError, HTTPError

# Download Drakosha MapList
URL = 'https://docs.google.com/spreadsheets/d/1_-lk7DWqkx5EqBRygRg_skUVV2JI3EEHCkDqhZ3uHrw/gviz/tq?tqx=out:csv&sheet=0'
FILE = 'maplist_drakosha.con'

class MapItem():
    def __init__(self):
        self.id = None
        self.valid = False
        self.mapname = None
        self.gamemode = None
        self.size = None

    def setId(self, data):
        i = data.strip('"').lower().replace(" ", "_")
        self.id = int('%s' % i)

    def setMap(self, data):
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
        s = data.strip('"').lower().replace(" ", "_")
        try:
            self.size = int('%s' % s)
        except:
            self.size = 0

    def getLine(self):
        return ('maplist.append "%s" "%s" "%s"' % (self.mapname, self.gamemode, self.size))

def fopen(infile):
    f = None
    try:
        assert(type(infile) == '_io.TextIOWrapper')
    except AssertionError:
        f = open(infile,'r')
    return f

def dlfile(url):
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
    m_items = []
    csvreader = csv.DictReader(f, delimiter=',',quotechar='|', dialect=csv.excel_tab)
    for row in csvreader:
        m = MapItem()
        m.setId(row['"#Nr"'])
        m.setMap(row['"Mapname"'])
        m.setGameMode(row['"Gamemode"'])
        m.setSize(row['"Mapsize"'])
        m_items.append(m)
        #print('%s' % m.getLine())
    return m_items

# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
    global URL, FILE
    input_url = URL # 'https://docs.google.com/spreadsheets/d/{key}/gviz/tq?tqx=out:csv&sheet=0'
    out_fname = FILE # 'maplist.con'
    csvdata = dlfile(input_url)
    #print(csvdata.decode('utf-8'))
    csv = io.BytesIO(csvdata)
    #csv_fname="data.csv"
    #csv=fopen(csv_fname)
    maplist = parse(csv)
    confile = open(out_fname,'w')
    print('Converting to BF2 format: %d map lines found' % len(maplist))
    for m in maplist:
        confile.write('%s\n' % m.getLine())
        #print('%s' % m.getLine())
    print('Result written to %s' % out_fname)
    print('Finished.')

if __name__ == '__main__':
    main()
