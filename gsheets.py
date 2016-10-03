__author__ = 'Justin'

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from time import strftime
import html_scraper
# from datetime import datetime, timedelta

COL_TIME = 1
COL_TITLE= 2
COL_ARTIST = 3


class GSheets(object):
    def __init__(self):
        sheetname = "TheHaikuza - 24HR Playlist"
        self.cellref = 'B3'
        self.firstrow = 6

        # path = '/home/pi/Python/Haikuza/'
        path = ''
        fname = path + 'Haiku Generator-4a140671aca6.json'
        json_key = json.load(open(fname))
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

        self.gc = gspread.authorize(credentials)
        self.wks = self.gc.open(sheetname).sheet1
        self.lastrow = len(self.wks.col_values(1))

    def get_gsheet_song(self):

        timenow = strftime("%H:%M")

        currow = self.get_row()

        gs_time = self.wks.cell(currow, COL_TIME).value

        # if timenow:
        if timenow == gs_time:
            timenow_full = strftime("%a, %d %b %Y %H:%M:%S")

            gs_title = self.wks.cell(currow, COL_TITLE).value
            gs_artist = self.wks.cell(currow, COL_ARTIST).value
            self.wks.update_acell(self.cellref, currow)  # Update Last row tweeted cell
            self.wks.update_acell('B2', timenow_full)  # Update time of last tweet cell

        else:
            print "Current time %s does not match %s (row %d)" %(timenow, gs_time, currow)
            gs_title = None
            gs_artist = None

        # print gs_title, gs_artist
        return gs_title, gs_artist

    def get_row(self):
        # cellind = 'B2'
        # firstrow = self.headers + 1
        # lastrow = 52
        lastrow_used = int(self.wks.acell(self.cellref).value)

        if lastrow_used >= self.lastrow or lastrow_used < self.firstrow:
            currow = self.firstrow
        else:
            currow = lastrow_used + 1

        # print lastrow_used, currow
        return currow

    def import_radio(self):
        songs = html_scraper.scrape_virginradio()

        numradio = len(songs.artist)

        print "Songs on Virgin Radio: %d \nNum time slots: %d" %(numradio, self.lastrow)

        j = 0

        for i in range(self.firstrow, self.lastrow + 1):
            self.wks.update_cell(i, COL_TITLE, songs.title[j])
            self.wks.update_cell(i, COL_ARTIST, songs.artist[j])
            j += 1

        timenow = strftime("%a, %d %b %Y %H:%M:%S")
        self.wks.update_acell('B1', timenow)

if __name__ == '__main__':
    gs = GSheets()
    # gs.get_gsheet_song()

    gs.import_radio()
