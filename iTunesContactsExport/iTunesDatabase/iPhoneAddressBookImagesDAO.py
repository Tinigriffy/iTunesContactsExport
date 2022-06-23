import sqlite3
from enum import IntEnum

class iPhoneAddressBookImagesDAO:

    class ImageQuality(IntEnum):
        ORIGNALE=1
        LOWEST_THUMNAIL=2
        HIGHEST_THUMBNAIL=3

    def __init__ (self,path:str):
        self.con = sqlite3.connect(path,uri=True)
        self.con.row_factory = sqlite3.Row
        

    def fetchImages(self,personId:int,quality:ImageQuality=ImageQuality.HIGHEST_THUMBNAIL):
        try:
            cur=self.con.cursor()
            if (quality==self.ImageQuality.ORIGNALE):
                row=cur.execute('''SELECT data as image FROM abfullsizeimage where record_id=?''', (personId,)).fetchone()
            elif (quality==self.ImageQuality.LOWEST_THUMNAIL):
                row=cur.execute('''SELECT min(format), data as image FROM ABThumbnailImage where record_id=?''', (personId,)).fetchone() 
            else :
                row=cur.execute('''SELECT max(format), data as image FROM ABThumbnailImage where record_id=?''', (personId,)).fetchone() 
            if(row):
                return row['image']
            return None
        finally:
            if cur is not None:
                cur.close()