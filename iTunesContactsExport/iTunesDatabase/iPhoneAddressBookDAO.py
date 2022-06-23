import sqlite3
from enum import IntEnum

class iPhoneAddressBookDAO:
    class PropertyType(IntEnum):
        PHONE=3
        EMAIL=4
        ADDRESS=5
        URL=22
        RELATION=23
        SERVICE=46

    def __init__ (self,path:str):
        self.con = sqlite3.connect(path,uri=True)
        self.con.row_factory = sqlite3.Row
        self.curPerson = self.con.cursor()
        
        #convert timestamp from 2001/01/01 00;00;00 to unixepoch timestamp
        self.curPerson.execute("SELECT ROWID as personId, First, Last, Middle, (978303600+CAST(Birthday as float)) as Birthday, Organization, Department, Note, JobTitle, Nickname, Prefix, Suffix, (978303600 + ModificationDate) as ModificationDate, guid, DisplayName, ImageType, ImageHash, PreferredChannel from ABPerson")
        

    def nextPerson(self): 
        return self.curPerson.fetchone()
    
    def __fetchMultivalue(self,personId:int,propertyType:int,format:str):
        try:
            cur=self.con.cursor()
            rows= cur.execute('''select ''' + format + ''' from abmultivalue, abmultivaluelabel 
                        where record_id=? and abmultivalue.property=? and abmultivaluelabel.ROWID=+abmultivalue.label 
                        order by record_id,identifier''', (personId,propertyType)).fetchall()
            return rows
        finally:
            if cur is not None:
                cur.close()

    def __fetchMultiAttributsMultiValue(self,id:int):
        try:
            cur=self.con.cursor()
            rows= cur.execute('''SELECT ABMultiValueEntryKey.value as label, ABMultiValueEntry.value as value
                                FROM ABMultiValueEntry , ABMultiValueEntryKey
                                WHERE parent_id=? and ABMultiValueEntry.key = ABMultiValueEntryKey.ROWID
                                ORDER BY key''', (id,)).fetchall()
            return rows
        finally:
            if cur is not None:
                cur.close()

    def fetchPhones(self,personId:int):
        return self.__fetchMultivalue(personId,self.PropertyType.PHONE,'''
            abmultivalue.value as phone,
            CASE
                WHEN abmultivaluelabel.value = "_$!<Home>!$_" then "home" 
                WHEN abmultivaluelabel.value = "_$!<Work>!$_" then "work" 
                WHEN abmultivaluelabel.value = "_$!<Mobile>!$_" then "cell" 
                WHEN abmultivaluelabel.value = "Mobile" then "cell" 
                WHEN abmultivaluelabel.value = "iPhone" then "cell" 
            ELSE null
            END as type''')

    def fetchMails(self,personId:int):
        return self.__fetchMultivalue(personId,self.PropertyType.EMAIL,'''
            abmultivalue.value as email,
            CASE
                WHEN abmultivaluelabel.value = "_$!<Home>!$_" then "home" 
                WHEN abmultivaluelabel.value = "_$!<Work>!$_" then "work" 
                WHEN abmultivaluelabel.value = "_$!<Other>!$_" then "other" 
            ELSE null
            END as type''')

    def fetchUrls(self,personId:int):
        return self.__fetchMultivalue(personId,self.PropertyType.URL,'''
            abmultivalue.value as url,
            CASE
                WHEN abmultivaluelabel.value = "_$!<Home>!$_" then "home" 
                WHEN abmultivaluelabel.value = "_$!<Work>!$_" then "work" 
                WHEN abmultivaluelabel.value = "_$!<Profile>!$_" then "profile" 
                WHEN abmultivaluelabel.value = "_$!<Other>!$_" then "other" 
            ELSE null
            END as type''')

    def fetchRelations(self,personId:int):
        return self.__fetchMultivalue(personId,self.PropertyType.RELATION,'''
            abmultivalue.value as value,
            CASE
                WHEN abmultivaluelabel.value = "parents" then "parent" 
                WHEN abmultivaluelabel.value = "_$!<Spouse>!$_" then "spouse" 
                WHEN abmultivaluelabel.value = "_$!<Partner>!$_" then "contact" 
                WHEN abmultivaluelabel.value = "_$!<Child>!$_" then "child" 
                WHEN abmultivaluelabel.value = "_$!<Father>!$_" then "parent" 
                WHEN abmultivaluelabel.value = "_$!<Mother>!$_" then "parent" 
                WHEN abmultivaluelabel.value = "Mère" then "parent" 
                WHEN abmultivaluelabel.value = "Mère" then "parent" 
                WHEN abmultivaluelabel.value = "_$!<Sister>!$_" then "sibling" 
                WHEN abmultivaluelabel.value = "_$!<Brother>!$_" then "sibling" 
                WHEN abmultivaluelabel.value = "_$!<Son>!$_" then "child" 
                WHEN abmultivaluelabel.value = "_$!<Daughter>!$_" then "child" 
            ELSE "contact"
            END as type''')    

    def fetchAddressList(self,personId:int):
        return self.__fetchMultivalue(personId,self.PropertyType.ADDRESS,'''
            abmultivalue.UID as id,
            CASE
                WHEN abmultivaluelabel.value = "_$!<Home>!$_" then "home" 
                WHEN abmultivaluelabel.value = "_$!<Work>!$_" then "work" 
            ELSE null
            END as type''')

    def fetchAddressData(self,id:int):
        rows=self.__fetchMultiAttributsMultiValue(id)
        attribList={'Country':None,'Street':None,'ZIP':None,'City':None,'CountryCode':None,'State':None}
        for row in rows:
            attribList[row["label"]]=row["value"]
        return attribList