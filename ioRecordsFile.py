'''
Created on 18 de Jul de 2012

@author: gil
'''

class RWFile(object):
    '''
    classdocs
    '''


    def __init__(self,fileName):
        '''
        Constructor
        '''
        self.openFileName = fileName



    def reedFileToStr(self):
        try:
            in_file = open(self.openFileName, "rt")
            text = in_file.read()
            in_file.close()
            return text
        except:
            return "ERR"
    def writeStrToFile(self,strToWrite):
        out_file = open(self.openFileName, "wt")
        out_file.write(strToWrite)
        out_file.close()
            