import base64
import vobject
from datetime import datetime

class vCardBuilderInterface:
    def build (self)->vobject.vCard: pass
    def N(self,family:str,given:str,additional:str,prefix:str,suffix:str):pass
    def FN(self,family:str,given:str):pass
    def ORG(self,orgName:str):pass
    def UID(self,uid:str):pass
    def NICKNAME(self,nickname:str):pass
    def BDAY(self,birthday:str):pass
    def ANNIVERSARY(self,birthday:str):pass
    def TITLE(self,title:str):pass
    def PHOTO(self,photo):pass
    def NOTE(self,note:str):pass
    def EMAIL(self,type:str,mail:str):pass
    def RELATED(self,type:str,value:str):pass
    def TEL(self,type:str,tel:str):pass
    def URL(self,type:str,url:str):pass
    def ADR(self,type:str,street:str, city:str, region:str, code:str, country:str, box:str=None, extended:str=None): pass

class vCardBuilder(vCardBuilderInterface):
    def __init__(self) -> None:
        super().__init__()
        self.card=vobject.vCard()

    def build (self) -> vobject.vCard:
        return self.card

    def __addSingleAttributTimestamp(self,key:str,value) -> vCardBuilderInterface:
        if key and value:
            if isinstance(value,str):
                value=float(value)
            value=datetime.fromtimestamp(value).strftime('%Y%m%dT%H%M%S')       
            self.card.add(key).value=value
        return self

    def __addSingleAttribut(self,key:str,value:str) -> vCardBuilderInterface:
        if key and value:
            self.card.add(key).value=value
        return self

    def __addSingleAttributWithType(self,key:str,type:str, value:str) -> vCardBuilderInterface:
        if key and value:
            node=self.card.add(key)
            node.value=value
            if type :
                node.type_param=type
        return self

    def N(self,family:str,given:str,additional:str,prefix:str,suffix:str) -> vCardBuilderInterface:
        self.card.add('n')
        self.card.n.value=vobject.vcard.Name(family=family or '',given=given or '',additional=additional or '', prefix=prefix or '',suffix=suffix or'')
        return self

    def FN(self,family:str,given:str) -> vCardBuilderInterface:
        self.card.add('fn')
        fn=''
        if given:
            fn=given
        if family:
            fn=fn+" "+family
        self.card.fn.value=fn
        return self

    def ORG(self,orgName:str) -> vCardBuilderInterface:
        return self.__addSingleAttribut('org',orgName)

    def UID(self,uid:str) -> vCardBuilderInterface:
        return self.__addSingleAttribut('uid',uid)
    
    def REV(self,timestamp) -> vCardBuilderInterface:
        return self.__addSingleAttributTimestamp('rev',timestamp)

    def NICKNAME(self,nickname:str) -> vCardBuilderInterface:
        return self.__addSingleAttribut('nickname',nickname)

    def BDAY(self,birthdaytimestamp) -> vCardBuilderInterface:
        return self.__addSingleAttributTimestamp('bday',birthdaytimestamp)

    def ANNIVERSARY(self,birthdaytimestamp) -> vCardBuilderInterface:
        return self.__addSingleAttributTimestamp('anniversary',birthdaytimestamp)

    def TITLE(self,title:str) -> vCardBuilderInterface:
        return self.__addSingleAttribut('title',title)

    def PHOTO(self,photo) -> vCardBuilderInterface:
        if not photo:
            return self
        if isinstance(photo,bytes):
            photo=base64.b64encode(photo)
            photo=photo.decode('utf-8')
            return self.__addSingleAttributWithType('PHOTO;ENCODING=B','JPEG',photo)
        return self.__addSingleAttributWithType('PHOTO','JPEG',photo)
 
    def NOTE(self,note:str) -> vCardBuilderInterface:
        return self.__addSingleAttribut('note',note)
    
    def EMAIL(self,type:str,mail:str) -> vCardBuilderInterface:
        return self.__addSingleAttributWithType('email',type, mail)

    def RELATED(self,type:str,value)-> vCardBuilderInterface:
        return self.__addSingleAttributWithType('related',type,value)

    def TEL(self,type:str,tel:str) -> vCardBuilderInterface:
        return self.__addSingleAttributWithType('tel',type,tel)
    
    def URL(self,type:str,url:str) -> vCardBuilderInterface:
        return self.__addSingleAttributWithType('url',type,url)
    
    def ADR(self, type:str, street:str, city:str, region:str, code:str, country:str, box:str=None, extended:str=None)-> vCardBuilderInterface:
        return self.__addSingleAttributWithType('adr',type,vobject.vcard.Address(street or '', city or '', region or '', code or '', country or '', box or'', extended or ''))