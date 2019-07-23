#!/usr/bin/env python3
import os
import sys 
import re

class Parser:
    def __init__(self,fd):
        self.fd = fd
        self.lineCount = 0
        f = open(sys.argv[1]+'.tmp','w')
        f.close()
        self.file = open(sys.argv[1]+'.tmp','r+')
        self.fd.seek(0)
        line = self.file.write(re.sub('^\\n','',re.sub('[\\n]+','\n',re.sub('//.+','',self.fd.read().replace(' ','')))))
        self.file.seek(0)
        self.totallineCount = len(list(self.file))
        self.file.seek(0)
    def hasMoreCommands(self):
        if self.lineCount < self.totallineCount:
            self.lineCount = self.lineCount + 1
            return True
        else:
            return False
    def advance(self):
        self.currentCommand = self.file.readline() 
    def commandType(self):
        if re.fullmatch('@.+\\n', self.currentCommand):
            return 'A_COMMAND'
        elif re.fullmatch('\(.+\)\\n', self.currentCommand):
            return 'L_COMMAND'
        elif re.fullmatch('[AMD\d]+(=[AMD+\-!|&01]+)?;?[\w]*\\n', self.currentCommand):
            return 'C_COMMAND'
    def symbol(self):
        if re.search('\(', self.currentCommand):
            return self.currentCommand.split('(')[1].split(')')[0]
        else:
            return self.currentCommand.split('@')[1].split('\n')[0]
    def dest(self):
        if re.search('=',self.currentCommand):
            return self.currentCommand.split('=')[0]
        else:
            return ''
    def comp(self):
        destcomp = self.currentCommand.split(';')[0]
        if (re.search('=',destcomp)):
            return self.currentCommand.split('=')[1].split('\n')[0]
        else:
            return destcomp
    def jump(self):
        if re.search(';',self.currentCommand):
           return self.currentCommand.split(';')[1].split('\n')[0]
        else:
            return False
    def __del__(self):
        self.fd.close()
        self.file.close()

class Code:
    @staticmethod
    def dest(mnemonic):
        desttable = {
            'M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'
        }
        if mnemonic == '':
            return '000'
        for i in desttable:
            if i == mnemonic:
                return desttable[i]
            
    @staticmethod
    def comp(mnemonic):
        values = ['101010','111111','111010','001100','110000',
        '001101','110001','001111','110011','011111','110111',
        '001110','110010','000010','010011','000111','000000','010101']
        comp = ['0','1','-1','D','A','!D','!A','-D','-A','D+1','A+1','D-1','A-1','D+A','D-A','A-D','D&A','D|A']
        compM = {
            'M':'4','!M':'6','-M':'8','M+1':'10','M-1':'12','D+M':'13','D-M':'14','M-D':'15','D&M':'16','D|M':'17'
        }
        if re.search('M',mnemonic):
            return '1' + values[int(compM[mnemonic])]
        else:
            return '0' + values[comp.index(mnemonic)]
    
    @staticmethod
    def jump(mnemonic):
        jumptable = {
            'JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'
        }
        if not mnemonic:
            return '000'
        for i in jumptable:
            if i == mnemonic:
                return jumptable[i]

class SymbolTable:
    def __init__(self):
        self.romAddress = 0
        self.ramAddress = 16
        self.symTable = {
            'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576,
            'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7,'R8':8,'R9':9,
            'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15
        }
    def addEntry(self, symbol, address):
        self.symTable[symbol]=address 
    def contains(self, symbol):
        if symbol in self.symTable:
            return True
        else:
            return False 
    def GetAddress(self, symbol):
        return self.symTable[symbol] 

if __name__ == "__main__":
    obj = Parser(open(sys.argv[1], 'r'))
    obj1 = SymbolTable()
    hackfile = open(sys.argv[1].split('.asm')[0] + '.hack','w')
    while obj.hasMoreCommands():
        obj.advance()
        commandType = obj.commandType()
        if (commandType == 'A_COMMAND') or (commandType == 'C_COMMAND'):
            obj1.romAddress = obj1.romAddress + 1
        if commandType == 'L_COMMAND':
            symbol = obj.symbol()
            if not obj1.contains(symbol):   
                obj1.addEntry(symbol,obj1.romAddress)
    obj.file.seek(0)    
    obj.lineCount = 0
    while(obj.hasMoreCommands()):
        obj.advance()
        commandType = obj.commandType()
        if commandType == 'A_COMMAND':
            if not (re.fullmatch('\d+',obj.symbol())):
                symbol = obj.symbol()
                if obj1.contains(symbol):
                    symaddr = obj1.GetAddress(symbol)
                    hackfile.write(bin(symaddr)[2:].zfill(16) + '\n')
                else:
                    obj1.addEntry(symbol,obj1.ramAddress)
                    obj1.ramAddress = obj1.ramAddress + 1
                    symaddr = obj1.GetAddress(symbol)
                    hackfile.write(bin(symaddr)[2:].zfill(16) + '\n')
            else:
                hackfile.write(bin(int(obj.symbol()))[2:].zfill(16) + '\n')
        elif commandType == 'C_COMMAND':
            destmnem = obj.dest()
            compmnem = obj.comp()
            jumpmnem = obj.jump()
            hackfile.write('111' + Code.comp(compmnem) + Code.dest(destmnem) + Code.jump(jumpmnem) + '\n')
    hackfile.close()