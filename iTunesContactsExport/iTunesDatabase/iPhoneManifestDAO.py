import sqlite3

class iPhoneManifestDAO:
    def __init__ (self,path:str):
        self.con = sqlite3.connect(path,uri=True)
        self.con.row_factory = sqlite3.Row

    def findAddressBookAndImagesDB(self):
        try:
            cur=self.con.cursor()
            rows=cur.execute('''SELECT fileID,relativePath FROM Files
                             where relativePath like('Library/AddressBook/AddressBook%')
                             order BY relativePath ASC;''').fetchall()
            if(rows):
                return (rows[0]['fileID'],rows[1]['fileID'])
            return None
        finally:
            if cur is not None:
                cur.close()
