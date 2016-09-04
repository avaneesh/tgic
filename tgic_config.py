
from __future__ import print_function
import ConfigParser

class TGICConfigDB:
    def __init__(self):
        core_dict = TGICConfigDB.parseTGICConfig()
        self.tag_token = core_dict['tag_token']
        self.comment_token = core_dict['comment_token']

    def __repr__(self):
        return "TGIC Config:\n\ttag_token = %s" % (self.tag_token)

    @staticmethod
    def getConfigDict(section):
        '''
            Borrowed from:
            https://wiki.python.org/moin/ConfigParserExamples
        '''
        Config = ConfigParser.ConfigParser()
        Config.read(".tgic.ini")
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
    
    @staticmethod
    def parseTGICConfig():
        core_dict = TGICConfigDB.getConfigDict('Core')
        return core_dict

if __name__ == '__main__':
    configDB = TGICConfigDB()
    print("read Token - ", configDB.tag_token)
