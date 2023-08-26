
from __future__ import print_function
#-------------------------------------------
# globals
#-------------------------------------------
from .base import BaseNormalizer,languages

#-------------------------------------------
# cleaner class
#-------------------------------------------

class Normalizer(BaseNormalizer):
    def __init__(self,
                allow_english=False,
                keep_legacy_symbols=False,
                legacy_maps=None):

       
        if legacy_maps=="default":
            legacy_maps=languages["olchiki"].legacy_maps

        self.complex_roots=languages["olchiki"].complex_roots

        super(Normalizer,self).__init__(language="olchiki",
                                        allow_english=allow_english,
                                        keep_legacy_symbols=keep_legacy_symbols,
                                        legacy_maps=legacy_maps)
        #-------------------------------------------------extended ops----------------------
        # assemese 
        self.assamese_map                               =       {'ᱨᱟ':'ᱨ','ᱨᱮ':'ᱵ'}
        self.word_level_ops["AssameseReplacement"]      =       self.replaceAssamese
        # punctuations
        self.punctuations_map                           =   {'"': '"' ,
                                                            '৷' : '।',
                                                            '–' : '-',
                                                            "'" : "'",
                                                            "'" : "'"}
        self.word_level_ops["PunctuationReplacement"]   =       self.replacePunctuations
        
        # to+hosonto case
      
        
        self.valid_consonants_after_to_and_hosonto      =       ['ᱛ','ᱫᱟ','ᱱ','ᱵ','ᱢ','ᱡᱚ','ᱨ'] 
        self.decomp_level_ops["base_olchiki_compose"]    =       self.baseCompose
        self.decomp_level_ops["ToAndHosontoNormalize"]  =       self.normalizeToandHosonto

        # invalid folas 
        self.decomp_level_ops["NormalizeConjunctsDiacritics"]      =       self.cleanInvalidConjunctDiacritics

        # complex root cleanup 
        self.decomp_level_ops["ComplexRootNormalization"]          =       self.convertComplexRoots

        
#-------------------------word ops----------------------------------------------------------------------------- 
    def replaceAssamese(self):
        self.replaceMaps(self.assamese_map)
    
    def replacePunctuations(self):
        self.replaceMaps(self.punctuations_map)
                        
#-------------------------unicode ops-----------------------------------------------------------------------------    
    def cleanConsonantDiacritics(self):
        # consonant diacritics
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-1:
                if d in self.lang.consonant_diacritics and self.decomp[idx+1] in self.lang.consonant_diacritics:
                    # if they are same delete the current one
                    if d==self.decomp[idx+1]:
                        self.decomp[idx]=None
                    elif d in ['.', '-'] and self.decomp[idx+1]=='ᱸ':
                        self.swapIdxs(idx,idx+1)
                    elif d=='.' and self.decomp[idx+1]== '-':
                        self.decomp[idx+1]=None
                    elif d=='-' and self.decomp[idx+1]== '.':
                        self.decomp[idx+1]=None
    
    def fixNoSpaceChar(self):
        # replace
        for idx,d in enumerate(self.decomp):
            if idx==0 and self.decomp[idx] in ["\u1C70","\u1C71"]:
                self.decomp[idx]=None
            else:
                if self.decomp[idx]=="\u1C70":
                    self.decomp[idx]="\u1C71"   
        self.decomp=[x for x in self.decomp if x is not None] 
        # strict
        for idx,d in enumerate(self.decomp):
            if idx>0:
                if self.decomp[idx]=="\u1C71":
                    # last one
                    if idx==len(self.decomp)-1:
                        self.decomp[idx]=None
                    else: 
                        # if previous one is a connector
                        if self.decomp[idx-1]==self.lang.connector:
                            self.decomp[idx]=None
                            self.decomp[idx-1]=None
                        # if previous one is not 'ᱨ'
                        elif self.decomp[idx-1]!='ᱨ':
                            self.decomp[idx]=None
                        else:
                            # if prev='ᱨ' and the prev-1 is not a connector
                            if idx>1 and self.decomp[idx-2]==self.lang.connector:
                                self.decomp[idx]=None
                            # if the next is not a connector
                            elif idx<len(self.decomp)-1 and self.decomp[idx+1]!=self.lang.connector:
                                self.decomp[idx]=None
                            # if the next one to connector is not "ᱡᱚ"
                            elif idx<len(self.decomp)-2 and self.decomp[idx+2]!="ᱡᱚ" and self.decomp[idx+1]!=self.lang.connector:
                                self.decomp[idx]=None
                            else:
                                # the actual allowed case
                                self.decomp[idx-1]+=self.decomp[idx]
                                self.decomp[idx]=None
        self.decomp=[x for x in self.decomp if x is not None] 
        
                
             
##------------------------------------------------------------------------------------------------------    
    def cleanInvalidConnector(self):
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-1:
                if d==self.lang.connector and self.decomp[idx+1]!="ᱡᱚ" and self.decomp[idx-1] not in ['ᱱᱚ','ᱚᱚ']: # exception
                    if self.decomp[idx-1] in self.lang.invalid_connectors  or self.decomp[idx+1] in self.lang.invalid_connectors:
                        self.decomp[idx]=None 
                if d==self.lang.connector and self.decomp[idx-1]=="ᱡᱚ" and self.decomp[idx+1]!="ᱡᱚ":
                    self.decomp[idx]=None
                if d==self.lang.connector and self.decomp[idx-1]=="ᱵ" and self.decomp[idx+1] not in ['ᱷ', 'ᱰ', 'ᱰᱦᱟ', 'ᱵ', 'ᱡᱚ', 'ᱨ', 'ᱞ']:
                    self.decomp[idx]=None

        # handle exception
        self.decomp=[d for d in self.decomp if d is not None]
        word="".join(self.decomp)
        
        if "ᱡᱚᱦᱟᱨ" in word:
            word=word.replace("ᱡᱚᱦᱟᱨ","ᱟᱭ")
        if 'ᱮᱤ' in word:
            word=word.replace('ᱮᱤ',"ᱟᱭ")
        self.decomp=[ch for ch in word]
    
    def convertToAndHosonto(self):
       
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-1:
                # to + hosonto
                if d=='ᱛ' and self.decomp[idx+1]== self.lang.connector:
                    # for single case
                    if  idx<len(self.decomp)-2: 
                        if self.decomp[idx+2] not in self.valid_consonants_after_to_and_hosonto:
                            # replace
                            self.decomp[idx]='ᱛ'
                            # delete
                            self.decomp[idx+1]=None
                            
                        else: 
                            # valid replacement for to+hos double case
                            if idx<len(self.decomp)-3: 
                                if self.decomp[idx+2]=='ᱛ' and self.decomp[idx+3]== self.lang.connector:
                                    if idx<len(self.decomp)-4: 
                                        if self.decomp[idx+4] not in  ['ᱵ','ᱡᱚ','ᱨ']:
                                            # if the next charecter after the double to+hos+to+hos is with in ['ᱛ','ᱫᱟ','ᱱ','ᱢ'] 
                                            # replace
                                            self.decomp[idx]='ᱛ'
                                            # delete
                                            self.decomp[idx+1]=None
                                    if idx<len(self.decomp)-4: 
                                        if self.decomp[idx+4]=='ᱨ':
                                            # delete
                                            self.decomp[idx+3]=None
        
    def swapToAndHosontoDiacritics(self):
        '''
            puts diacritics in right place
        '''
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-1:
                if d=='ᱛ' and self.decomp[idx+1] in self.lang.diacritics:
                    self.swapIdxs(idx,idx+1)
###------------------------------------------------------------------------------------------------------               
    def normalizeToandHosonto(self):
        self.safeop(self.convertToAndHosonto)
        self.safeop(self.swapToAndHosontoDiacritics)
        self.baseCompose()
        
###------------------------------------------------------------------------------------------------------               
##------------------------------------------------------------------------------------------------------               
      
    def cleanVowelDiacriticComingAfterVowel(self):
        
        for idx,d in enumerate(self.decomp):
            # if the current one is a VD and the previous char is a vowel
            if  d in self.lang.vowel_diacritics and self.decomp[idx-1] in self.lang.vowels:
                # if the vowel is not 'ᱚᱚ'
                if self.decomp[idx-1] !='ᱚᱚ':
                    # remove diacritic
                    self.decomp[idx]=None
                # normalization case
                else:
                    self.decomp[idx-1]='ᱛ'+'~'+'ᱨ'

##------------------------------------------------------------------------------------------------------               
    def fixTypoForJoFola(self):
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-1:
                if  d== self.lang.connector and self.decomp[idx+1]=='য়':
                    self.decomp[idx+1]='ᱡᱚ'
        
    def cleanDoubleCC(self):
        # c,cc,c,cc
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-3:
                if  d== self.lang.connector and self.decomp[idx+1] in self.lang.consonants \
                    and self.decomp[idx+2]==self.lang.connector and self.decomp[idx+3] in self.lang.consonants:
                        if self.decomp[idx+3]==self.decomp[idx+1]:
                            self.decomp[idx]=None
                            self.decomp[idx+1]=None    

    
    
    def cleanDoubleRef(self):
        for idx,d in enumerate(self.decomp):
            if idx<len(self.decomp)-3:
                if  d=='ᱨ' and self.decomp[idx+1]==self.lang.connector\
                    and self.decomp[idx+2]=='ᱨ' and self.decomp[idx+3]== self.lang.connector:
                    self.decomp[idx]=None
                    self.decomp[idx+1]=None
        
    def cleanConnectotForJoFola(self):
            for idx,d in enumerate(self.decomp):
                if idx<len(self.decomp)-2:
                    if  d== self.lang.connector and self.decomp[idx+1]=='ᱡᱚ' and self.decomp[idx+2]==self.lang.connector:
                        self.decomp[idx+2]=None
        


    def cleanInvalidConjunctDiacritics(self):
       
        self.safeop(self.fixTypoForJoFola)
        self.safeop(self.cleanDoubleCC)
        self.safeop(self.cleanDoubleRef)
        # self.safeop(self.fixRefOrder)
        # print("".join(self.decomp))
        # #self.safeop(self.fixOrdersForCC)
        #print("".join(self.decomp))
        self.safeop(self.cleanConnectotForJoFola)
        self.baseCompose()
##------------------------------------------------------------------------------------------------------               
    def checkComplexRoot(self,root):
        formed=[]
        formed_idx=[]
        for i,c in enumerate(root):
            if c !='~' and i not in formed_idx:
                r=c
                if i==len(root)-1:
                    formed.append(r)
                    continue
                for j in range(i+2,len(root),2):
                
                    d=root[j]
                    k=r+'~'+d
                    #if k==
                    if k not in self.complex_roots:
                        formed.append(r)
                        break
                    else:
                        if j!=len(root)-1:
                            r=k
                            formed_idx.append(j)
                        else:
                            r=k
                            formed_idx.append(j)
                            formed.append(k)
        return "".join(formed)

        
    
    def convertComplexRoots(self):
        self.fixNoSpaceChar()
        self.decomp=[x for x in self.decomp if x is not None] 
        self.constructComplexDecomp()
        for idx,d in enumerate(self.decomp):
            if d not in self.complex_roots and self.lang.connector in d:
                self.decomp[idx]=self.checkComplexRoot(d) 
        


#-------------------------unicode ops-----------------------------------------------------------------------------               
    
            
    
  
