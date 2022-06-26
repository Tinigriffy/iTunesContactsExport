# A sad IPHone story ...
I wrote this python script after my iPhone had a unrepairable hardware failure and a corrupt iTunes backup that could not be restored on my new iPhone!
I was losing pictures but not that much as I regularly extracts them, but it was a totally different story for the contacts, as iTunes offers no way to extract them and I refuse to send my data to iCloud.
I search for a way to recover my contacts and I found not only many applications that all promise that they will repair and/ore recover you data, but also simple script that extract them from the database of the address book. You just need a backup from iTunes. 
So I decided to write my own version that extracts all the fields I need in a vCard 3.0 format. I do not intend to cover all the cases but i think it is already quite complete, and I hope it will help others. 
I took this opportunity to write it in python, language that I barely know, so i ask for mercy to the experts in Python because I probably do not follow theirs best practice :)

# Install
## prerequisits
- python >=3.9 [prerequisits]([https://www.python.org/downloads/])
- pip
- pipx (optional)
## Intall 
```
    pip install itunescontactsexport
```
or
```
    pip install pipx
    pipx install itunescontactsexport
```
 
# Usage
 There 2 modes to use this script:
 - iTunes mode: You need to have access to the directory of a iTunes backup of your phone. The script will figure out where are the databases of the address book and export the contacts
 - db: You need to provide the path to the address book you want to export and optionally the path to the iamges database of the address book

The image quality refer to the available thumbnail in our thumbnail database:
- originale: it use the originale image with no transformation
- best: use the thumbnail with the highest resolution
- lowest: use the thumbnail with the lowest resolution.
## Backup from iTunes
 ```usage: iTunesContactsExport itunes [-h] [-bday] [-q {best,lowest,orig}] [-o outputFile] backupDir

positional arguments:
  backupDir             Path to the directory of the Itunebackup

optional arguments:
  -h, --help            show this help message and exit
  -bday                 Use BDAY instead of ANNIVERSARY (not iphone friendly
  -q {best,lowest,orig}
                        Image quality: best, lowest, originale
  -o outputFile         Path to export file
```
## Backup from db
 ```usage: iTunesContactsExport db [-h] [-bday] [-q {best,lowest,orig}] [-i imagesDBPath] [-o outputFile] addressBookDBPath

positional arguments:
  addressBookDBPath     Path to the addressbook database

optional arguments:
  -h, --help            show this help message and exit
  -bday                 Use BDAY instead of ANNIVERSARY (not iphone friendly
  -q {best,lowest,orig}
                        Image quality: best, lowest, originale
  -i imagesDBPath       Path to the images database
  -o outputFile         Path to export file
```
# Limitations
The attributs exported to the vcard are:
- uid of the contact
- last modification of the vcard
- Name (Given, middle, Familly)
- Nickname
- job title
- Phones numbers
- Addresses
- emails
- Birthday
- relatives
- images
- Notes
- urls
