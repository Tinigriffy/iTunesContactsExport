import argparse
from os import path
import sys

from iTunesContactsExport.iTunesDatabase.iPhoneAddressBookDAO import iPhoneAddressBookDAO
from iTunesContactsExport.iTunesDatabase.iPhoneAddressBookImagesDAO import iPhoneAddressBookImagesDAO
from iTunesContactsExport.iTunesDatabase.iPhoneManifestDAO import iPhoneManifestDAO
from iTunesContactsExport.vCard.vCardBuilder import vCardBuilder

def exportContacts(f,db:iPhoneAddressBookDAO,dbImages:iPhoneAddressBookImagesDAO,bday:bool,quality:iPhoneAddressBookImagesDAO.ImageQuality):
    person=db.nextPerson()
    while person :
        builder=vCardBuilder().N(person['Last'],person['First'],person['Middle'],person['Prefix'],person['Suffix'])\
                                    .FN(person['First'],person['Last'])\
                                    .ORG(person["Organization"])\
                                    .UID(person["guid"])\
                                    .REV(person['ModificationDate'])\
                                    .NICKNAME(person["Nickname"])\
                                    .NOTE(person["Note"])\
                                    .TITLE(person["JobTitle"])
        if bday:
            builder.BDAY(person['Birthday'])
        else:
            builder.ANNIVERSARY(person['Birthday'])

        for mail in  db.fetchMails(person['personId']):
            builder.EMAIL(mail['type'],mail['email'])
    
        for tel in  db.fetchPhones(person['personId']):
            builder.TEL(tel['type'],tel['phone'])

        for url in  db.fetchUrls(person['personId']):
            builder.URL(url['type'],url['url'])

        for relationEntry in db.fetchRelations(person['personId']):
            builder.RELATED(relationEntry['type'],relationEntry['value'])

        for addressEntry in db.fetchAddressList(person['personId']):
            adrAttribs=db.fetchAddressData(addressEntry['id'])
            builder.ADR(addressEntry['type'],adrAttribs['Street'],adrAttribs['City'],adrAttribs['State'],adrAttribs['ZIP'],adrAttribs['CountryCode'])
        
        if(dbImages):
            blob=dbImages.fetchImages(person['personId'],quality)
            if blob:
                builder.PHOTO(blob)

        card=builder.build()                                    
        f.write(card.serialize())
        person=db.nextPerson()
        
def generateDBPath(searchPath:str,filename:str):
    return path.join(searchPath,filename[0:2],filename)

def findDatabases(manifestPath:str):
    try:
        db=iPhoneManifestDAO(manifestPath)
        (dbfile,dbImagesfile)=db.findAddressBookAndImagesDB()
        (searchPath,filename)=path.split(manifestPath)
        return (generateDBPath(searchPath,dbfile),generateDBPath(searchPath,dbImagesfile))
    finally:
        pass

def cmdLineParserBuild()-> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Iphone contacts export')
    subparsers = parser.add_subparsers(help='help for subcommand', dest="subcommand")
    group1=subparsers.add_parser('itunes', help='From a itunes backup directory')
    group1.add_argument('-bday',action='store_true',help="Use BDAY instead of ANNIVERSARY (not iphone friendly")
    group1.add_argument("-q",choices=['best', 'lowest', 'orig'], default='best',help="Image quality: best, lowest, originale")
    group1.add_argument('-o', metavar='outputFile',type=argparse.FileType('w',encoding='utf8'),help="Path to export file")
    group1.add_argument('backupDir',help="Path to the directory of the Itunebackup")
    group2=subparsers.add_parser('db', help='From the addressbook database')
    group2.add_argument('-bday',action='store_true',help="Use BDAY instead of ANNIVERSARY (not iphone friendly")
    group2.add_argument("-q",choices=['best', 'lowest', 'orig'], default='best',help="Image quality: best, lowest, originale")
    group2.add_argument("-i", metavar='imagesDBPath',help="Path to the images database")
    group2.add_argument('-o', metavar='outputFile',type=argparse.FileType('w',encoding='utf8'),help="Path to export file")
    group2.add_argument('addressBookDBPath',  help="Path to the addressbook database")
    return parser
    

def main():

    parser = cmdLineParserBuild()
    args=parser.parse_args()
    
    f=sys.stdout
    if args.subcommand == "itunes":
        manifestPath=path.join(args.backupDir,'Manifest.db')
        (dbfile,dbImagesfile)=findDatabases(manifestPath);
    elif args.subcommand == "db":
        dbfile=args.addressBookDBPath
        dbImagesfile=args.i
    else:
        parser.print_usage()
        exit()
    
    if args.o:
        f=args.o
   
    quality=iPhoneAddressBookImagesDAO.ImageQuality.HIGHEST_THUMBNAIL
    if args.q:
        quality = {
            "orig": lambda quality: iPhoneAddressBookImagesDAO.ImageQuality.ORIGNALE,
            "lowest": lambda quality: iPhoneAddressBookImagesDAO.ImageQuality.LOWEST_THUMNAIL,
            "best": lambda quality:iPhoneAddressBookImagesDAO.ImageQuality.HIGHEST_THUMBNAIL            
        }[args.q]

    try:
        db=iPhoneAddressBookDAO(dbfile)
        dbImages=None
        if dbImagesfile:
            dbImages=iPhoneAddressBookImagesDAO(dbImagesfile)
        exportContacts(f,db,dbImages,args.bday,quality)
    finally:
        if f:
            f.close()

if __name__ == "__main__":
    main()




