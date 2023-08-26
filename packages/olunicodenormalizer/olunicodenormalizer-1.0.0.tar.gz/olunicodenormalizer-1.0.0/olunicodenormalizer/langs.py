
from __future__ import print_function
#--------------------------------------------------------------------------------------------------------------------------------------------
# language classes
#--------------------------------------------------------------------------------------------------------------------------------------------
class english:
    lower                  =    ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    upper                  =    ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    punctuations           =    ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', 
                                 '@', '[', '\\', ']', '^', '_', '`','{', '|', '}', '~']
    numbers                =    ["0","1","2","3","4","5","6","7","8","9"]

    valid                  =    sorted(lower+upper+numbers+punctuations)
#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------
class olchiki:
   
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =    "olchiki"
    nukta                  =   '.'
    vowels                 =   ['ᱚ', 'ᱟ', 'ᱤ', 'ᱩ', 'ᱮ', 'ᱳ']
    consonants             =   ['ᱛ', 'ᱜ', 'ᱝ', 'ᱞ', 'ᱠ', 'ᱡ', 'ᱢ','ᱣ', 'ᱥ', 'ᱦ', 'ᱧ', 'ᱨ', 'ᱪ', 'ᱫ', 'ᱬ', 'ᱭ', 'ᱯ', 'ᱰ', 'ᱱ', 'ᱲ', 
                                'ᱴ', 'ᱵ', 'ᱶ', 'ᱷ']
    vowel_diacritics       =   ['ᱸ', 'ᱹ', 'ᱺ', 'ᱻ', 'ᱼ', 'ᱽ']
    consonant_diacritics   =   []
    numbers                =   ['᱐', '᱑', '᱒', '᱓', '᱔', '᱕', '᱖', '᱗', '᱘', '᱙']
    punctuations           =   ['!', '"', "'", '(', ')', ',', '-', '.', '...', ':', ':-', ';', '<', '=', '>', '?', '[', ']', '{', '}', '।', '৷', '–', '—', '”', '√']
    symbols                =   ['ᱚ']
    connector              =   '.'
    

    non_gylph_unicodes     =   ['\u1C5A', '\u1C5B','\u1C5C','\u1C5D','\u1C5E','\u1C5F','\u1C60 ','\u1C61','\u1C62','\u1C63',
                                '\u1C64','\u1C65', '\u1C66','\u1C67','\u1C68','\u1C69','\u1C6A','\u1C6B','\u1C6C','\u1C6D',
                                '\u1C6E','\u1C6F','\u1C70','\u1C71', '\u1C72','\u1C73','\u1C74','\u1C75','\u1C76', '\u1C77',
                                '\u1C78', '\u1C79','\u1C7A','\u1C7B','\u1C7C', '\u1C7D', '\u1C7E', '\u1C7F','\u1C50','\u1C51','\u1C52','\u1C53','\u1C54',
                                '\u1C55','\u1C56','\u1C57','\u1C58','\u1C59']
    legacy_symbols         =   []
    
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   ['ᱚᱚ','ᱚᱛ','ᱚᱜ','ᱚᱝ','ᱚᱞ','ᱚᱟ','ᱚᱠ','ᱚᱡ','ᱚᱢ','ᱚᱣ','ᱚᱤ','ᱚᱥ','ᱚᱦ','ᱚᱧ','ᱚᱨ','ᱚᱩ','ᱚᱪ','ᱚᱫ','ᱚᱬ','ᱚᱭ','ᱚᱮ','ᱚᱯ','ᱚᱰ', 'ᱚᱱ', 'ᱚᱲ', 'ᱚᱳ', 'ᱚᱴ', 'ᱚᱵ', 'ᱚᱶ', 'ᱚᱷ',
                                'ᱛᱚ','ᱛᱛ','ᱛᱜ','ᱛᱝ','ᱛᱞ','ᱛᱟ','ᱛᱠ','ᱛᱡ','ᱛᱢ','ᱛᱣ','ᱛᱤ','ᱛᱥ','ᱛᱦ','ᱛᱧ','ᱛᱨ','ᱛᱩ','ᱛᱪ','ᱛᱫ','ᱛᱬ','ᱛᱭ','ᱛᱮ','ᱛᱯ','ᱛᱰ', 'ᱛᱱ', 'ᱛᱲ', 'ᱛᱳ', 'ᱛᱴ', 'ᱛᱵ', 'ᱛᱶ', 'ᱛᱷ',
                                'ᱜᱚ','ᱜᱛ','ᱜᱜ','ᱜᱝ','ᱜᱞ','ᱜᱟ','ᱜᱠ','ᱜᱡ','ᱜᱢ','ᱜᱣ','ᱜᱤ','ᱜᱥ','ᱜᱦ','ᱜᱧ','ᱜᱨ','ᱜᱩ','ᱜᱪ','ᱜᱫ','ᱜᱬ','ᱜᱭ','ᱜᱮ','ᱜᱯ','ᱜᱰ', 'ᱜᱱ', 'ᱜᱲ', 'ᱜᱳ', 'ᱜᱴ', 'ᱜᱵ', 'ᱜᱶ', 'ᱜᱷ',
                                'ᱝᱚ','ᱝᱛ','ᱝᱜ','ᱝᱝ','ᱝᱞ','ᱝᱟ','ᱝᱠ','ᱝᱡ','ᱝᱢ','ᱝᱣ','ᱝᱤ','ᱝᱥ','ᱝᱦ','ᱝᱧ','ᱝᱨ','ᱝᱩ','ᱝᱪ','ᱝᱫ','ᱝᱬ','ᱝᱭ','ᱝᱮ','ᱝᱯ','ᱝᱰ', 'ᱝᱱ', 'ᱝᱲ', 'ᱝᱳ', 'ᱝᱴ', 'ᱝᱵ', 'ᱝᱶ', 'ᱝᱷ',
                                'ᱞᱚ','ᱞᱛ','ᱞᱜ','ᱞᱝ','ᱞᱞ','ᱞᱟ','ᱞᱠ','ᱞᱡ','ᱞᱢ','ᱞᱣ','ᱞᱤ','ᱞᱥ','ᱞᱦ','ᱞᱧ','ᱞᱨ','ᱞᱩ','ᱞᱪ','ᱞᱫ','ᱞᱬ','ᱞᱭ','ᱞᱮ','ᱞᱯ','ᱞᱰ', 'ᱞᱱ', 'ᱞᱲ', 'ᱞᱳ', 'ᱞᱴ', 'ᱞᱵ', 'ᱞᱶ', 'ᱞᱷ',
                                'ᱟᱚ','ᱟᱛ','ᱟᱜ','ᱟᱝ','ᱟᱞ','ᱟᱟ','ᱟᱠ','ᱟᱡ','ᱟᱢ','ᱟᱣ','ᱟᱤ','ᱟᱥ','ᱟᱦ','ᱟᱧ','ᱟᱨ','ᱟᱩ','ᱟᱪ','ᱟᱫ','ᱟᱬ','ᱟᱭ','ᱟᱮ','ᱟᱯ','ᱟᱰ', 'ᱟᱱ', 'ᱟᱲ', 'ᱟᱳ', 'ᱟᱴ', 'ᱟᱵ', 'ᱟᱶ', 'ᱟᱷ',
                                'ᱠᱚ','ᱠᱛ','ᱠᱜ','ᱠᱝ','ᱠᱞ','ᱠᱟ','ᱠᱠ','ᱠᱡ','ᱠᱢ','ᱠᱣ','ᱠᱤ','ᱠᱥ','ᱠᱦ','ᱠᱧ','ᱠᱨ','ᱠᱩ','ᱠᱪ','ᱠᱫ','ᱠᱬ','ᱠᱭ','ᱠᱮ','ᱠᱯ','ᱠᱰ', 'ᱠᱱ', 'ᱠᱲ', 'ᱠᱳ', 'ᱠᱴ', 'ᱠᱵ', 'ᱠᱶ', 'ᱠᱷ',
                                'ᱡᱚ','ᱡᱛ','ᱡᱜ','ᱡᱝ','ᱡᱞ','ᱡᱟ','ᱡᱠ','ᱡᱡ','ᱡᱢ','ᱡᱣ','ᱡᱤ','ᱡᱥ','ᱡᱦ','ᱡᱧ','ᱡᱨ','ᱡᱩ','ᱡᱪ','ᱡᱫ','ᱡᱬ','ᱡᱭ','ᱡᱮ','ᱡᱯ','ᱡᱰ', 'ᱡᱱ', 'ᱡᱲ', 'ᱡᱳ', 'ᱡᱴ', 'ᱡᱵ', 'ᱡᱶ', 'ᱡᱷ',
                                'ᱢᱚ','ᱢᱛ','ᱢᱜ','ᱢᱝ','ᱢᱞ','ᱢᱟ','ᱢᱠ','ᱢᱡ','ᱢᱢ','ᱢᱣ','ᱢᱤ','ᱢᱥ','ᱢᱦ','ᱢᱧ','ᱢᱨ','ᱢᱩ','ᱢᱪ','ᱢᱫ','ᱢᱬ','ᱢᱭ','ᱢᱮ','ᱢᱯ','ᱢᱰ', 'ᱢᱱ', 'ᱢᱲ', 'ᱢᱳ', 'ᱢᱴ', 'ᱢᱵ', 'ᱢᱶ', 'ᱢᱷ',
                                'ᱣᱚ','ᱣᱛ','ᱣᱜ','ᱣᱝ','ᱣᱞ','ᱣᱟ','ᱣᱠ','ᱣᱡ','ᱣᱢ','ᱣᱣ','ᱣᱤ','ᱣᱥ','ᱣᱦ','ᱣᱧ','ᱣᱨ','ᱣᱩ','ᱣᱪ','ᱣᱫ','ᱣᱬ','ᱣᱭ','ᱣᱮ','ᱣᱯ','ᱣᱰ', 'ᱣᱱ', 'ᱣᱲ', 'ᱣᱳ', 'ᱣᱴ', 'ᱣᱵ', 'ᱣᱶ', 'ᱣᱷ',
                                'ᱤᱚ','ᱤᱛ','ᱤᱜ','ᱤᱝ','ᱤᱞ','ᱤᱟ','ᱤᱠ','ᱤᱡ','ᱤᱢ','ᱤᱣ','ᱤᱤ','ᱤᱥ','ᱤᱦ','ᱤᱧ','ᱤᱨ','ᱤᱩ','ᱤᱪ','ᱤᱫ','ᱤᱬ','ᱤᱭ','ᱤᱮ','ᱤᱯ','ᱤᱰ', 'ᱤᱱ', 'ᱤᱲ', 'ᱤᱳ', 'ᱤᱴ', 'ᱤᱵ', 'ᱤᱶ', 'ᱤᱷ',
                                'ᱥᱚ','ᱥᱛ','ᱥᱜ','ᱥᱝ','ᱥᱞ','ᱥᱟ','ᱥᱠ','ᱥᱡ','ᱥᱢ','ᱥᱣ','ᱥᱤ','ᱥᱥ','ᱥᱦ','ᱥᱧ','ᱥᱨ','ᱥᱩ','ᱥᱪ','ᱥᱫ','ᱥᱬ','ᱥᱭ','ᱥᱮ','ᱥᱯ','ᱥᱰ', 'ᱥᱱ', 'ᱥᱲ', 'ᱥᱳ', 'ᱥᱴ', 'ᱥᱵ', 'ᱥᱶ', 'ᱥᱷ',
                                'ᱦᱚ','ᱦᱛ','ᱦᱜ','ᱦᱝ','ᱦᱞ','ᱦᱟ','ᱦᱠ','ᱦᱡ','ᱦᱢ','ᱦᱣ','ᱦᱤ','ᱦᱥ','ᱦᱦ','ᱦᱧ','ᱦᱨ','ᱦᱩ','ᱦᱪ','ᱦᱫ','ᱦᱬ','ᱦᱭ','ᱦᱮ','ᱦᱯ','ᱦᱰ', 'ᱦᱱ', 'ᱦᱲ', 'ᱦᱳ', 'ᱦᱴ', 'ᱦᱵ', 'ᱦᱶ', 'ᱦᱷ',
                                'ᱧᱚ','ᱧᱛ','ᱧᱜ','ᱧᱝ','ᱧᱞ','ᱧᱟ','ᱧᱠ','ᱧᱡ','ᱧᱢ','ᱧᱣ','ᱧᱤ','ᱧᱥ','ᱧᱦ','ᱧᱧ','ᱧᱨ','ᱧᱩ','ᱧᱪ','ᱧᱫ','ᱧᱬ','ᱧᱭ','ᱧᱮ','ᱧᱯ','ᱧᱰ', 'ᱧᱱ', 'ᱧᱲ', 'ᱧᱳ', 'ᱧᱴ', 'ᱧᱵ', 'ᱧᱶ', 'ᱧᱷ',
                                'ᱨᱚ','ᱨᱛ','ᱨᱜ','ᱨᱝ','ᱨᱞ','ᱨᱟ','ᱨᱠ','ᱨᱡ','ᱨᱢ','ᱨᱣ','ᱨᱤ','ᱨᱥ','ᱨᱦ','ᱨᱧ','ᱨᱨ','ᱨᱩ','ᱨᱪ','ᱨᱫ','ᱨᱬ','ᱨᱭ','ᱨᱮ','ᱨᱯ','ᱨᱰ', 'ᱨᱱ', 'ᱨᱲ', 'ᱨᱳ', 'ᱨᱴ', 'ᱨᱵ', 'ᱨᱶ', 'ᱨᱷ',
                                'ᱩᱚ','ᱩᱛ','ᱩᱜ','ᱩᱝ','ᱩᱞ','ᱩᱟ','ᱩᱠ','ᱩᱡ','ᱩᱢ','ᱩᱣ','ᱩᱤ','ᱩᱥ','ᱩᱦ','ᱩᱧ','ᱩᱨ','ᱩᱩ','ᱩᱪ','ᱩᱫ','ᱩᱬ','ᱩᱭ','ᱩᱮ','ᱩᱯ','ᱩᱰ', 'ᱩᱱ', 'ᱩᱲ', 'ᱩᱳ', 'ᱩᱴ', 'ᱩᱵ', 'ᱩᱶ', 'ᱩᱷ',
                                'ᱪᱚ','ᱪᱛ','ᱪᱜ','ᱪᱝ','ᱪᱞ','ᱪᱟ','ᱪᱠ','ᱪᱡ','ᱪᱢ','ᱪᱣ','ᱪᱤ','ᱪᱥ','ᱪᱦ','ᱪᱧ','ᱪᱨ','ᱪᱩ','ᱪᱪ','ᱪᱫ','ᱪᱬ','ᱪᱭ','ᱪᱮ','ᱪᱯ','ᱪᱰ', 'ᱪᱱ', 'ᱪᱲ', 'ᱪᱳ', 'ᱪᱴ', 'ᱪᱵ', 'ᱪᱶ', 'ᱪᱷ',
                                'ᱫᱚ','ᱫᱛ','ᱫᱜ','ᱫᱝ','ᱫᱞ','ᱫᱟ','ᱫᱠ','ᱫᱡ','ᱫᱢ','ᱫᱣ','ᱫᱤ','ᱫᱥ','ᱫᱦ','ᱫᱧ','ᱫᱨ','ᱫᱩ','ᱫᱪ','ᱫᱫ','ᱫᱬ','ᱫᱭ','ᱫᱮ','ᱫᱯ','ᱫᱰ', 'ᱫᱱ', 'ᱫᱲ', 'ᱫᱳ', 'ᱫᱴ', 'ᱫᱵ', 'ᱫᱶ', 'ᱫᱷ',
                                'ᱬᱚ','ᱬᱛ','ᱬᱜ','ᱬᱝ','ᱬᱞ','ᱬᱟ','ᱬᱠ','ᱬᱡ','ᱬᱢ','ᱬᱣ','ᱬᱤ','ᱬᱥ','ᱬᱦ','ᱬᱧ','ᱬᱨ','ᱬᱩ','ᱬᱪ','ᱬᱫ','ᱬᱬ','ᱬᱭ','ᱬᱮ','ᱬᱯ','ᱬᱰ', 'ᱬᱱ', 'ᱬᱲ', 'ᱬᱳ', 'ᱬᱴ', 'ᱬᱵ', 'ᱬᱶ', 'ᱬᱷ',
                                'ᱭᱚ','ᱭᱛ','ᱭᱜ','ᱭᱝ','ᱭᱞ','ᱭᱟ','ᱭᱠ','ᱭᱡ','ᱭᱢ','ᱭᱣ','ᱭᱤ','ᱭᱥ','ᱭᱦ','ᱭᱧ','ᱭᱨ','ᱭᱩ','ᱭᱪ','ᱭᱫ','ᱭᱬ','ᱭᱭ','ᱭᱮ','ᱭᱯ','ᱭᱰ', 'ᱭᱱ', 'ᱭᱲ', 'ᱭᱳ', 'ᱭᱴ', 'ᱭᱵ', 'ᱭᱶ', 'ᱭᱷ',                     
                                'ᱮᱚ','ᱮᱛ','ᱮᱜ','ᱮᱝ','ᱮᱞ','ᱮᱟ','ᱮᱠ','ᱮᱡ','ᱮᱢ','ᱮᱣ','ᱮᱤ','ᱮᱥ','ᱮᱦ','ᱮᱧ','ᱮᱨ','ᱮᱩ','ᱮᱪ','ᱮᱫ','ᱮᱬ','ᱮᱭ','ᱮᱮ','ᱮᱯ','ᱮᱰ', 'ᱮᱱ', 'ᱮᱲ', 'ᱮᱳ', 'ᱮᱴ', 'ᱮᱵ', 'ᱮᱶ', 'ᱮᱷ',
                                'ᱯᱚ','ᱯᱛ','ᱯᱜ','ᱯᱝ','ᱯᱞ','ᱯᱟ','ᱯᱠ','ᱯᱡ','ᱯᱢ','ᱯᱣ','ᱯᱤ','ᱯᱥ','ᱯᱦ','ᱯᱧ','ᱯᱨ','ᱯᱩ','ᱯᱪ','ᱯᱫ','ᱯᱬ','ᱯᱭ','ᱯᱮ','ᱯᱯ','ᱯᱰ', 'ᱯᱱ', 'ᱯᱲ', 'ᱯᱳ', 'ᱯᱴ', 'ᱯᱵ', 'ᱯᱶ', 'ᱯᱷ',
                                'ᱰᱚ','ᱰᱛ','ᱰᱜ','ᱰᱝ','ᱰᱞ','ᱰᱟ','ᱰᱠ','ᱰᱡ','ᱰᱢ','ᱰᱣ','ᱰᱤ','ᱰᱥ','ᱰᱦ','ᱰᱧ','ᱰᱨ','ᱰᱩ','ᱰᱪ','ᱰᱫ','ᱰᱬ','ᱰᱭ','ᱰᱮ','ᱰᱯ','ᱰᱰ', 'ᱰᱱ', 'ᱰᱲ', 'ᱰᱳ', 'ᱰᱴ', 'ᱰᱵ', 'ᱰᱶ', 'ᱰᱷ',
                                'ᱲᱚ','ᱲᱛ','ᱲᱜ','ᱲᱝ','ᱲᱞ','ᱲᱟ','ᱲᱠ','ᱲᱡ','ᱲᱢ','ᱲᱣ','ᱲᱤ','ᱲᱥ','ᱲᱦ','ᱲᱧ','ᱲᱨ','ᱲᱩ','ᱲᱪ','ᱲᱫ','ᱲᱬ','ᱲᱭ','ᱲᱮ','ᱲᱯ','ᱲᱰ', 'ᱲᱱ', 'ᱲᱲ', 'ᱲᱳ', 'ᱲᱴ', 'ᱲᱵ', 'ᱲᱶ', 'ᱲᱷ',
                                'ᱱᱚ','ᱱᱛ','ᱱᱜ','ᱱᱝ','ᱱᱞ','ᱱᱟ','ᱱᱠ','ᱱᱡ','ᱱᱢ','ᱱᱣ','ᱱᱤ','ᱱᱥ','ᱱᱦ','ᱱᱧ','ᱱᱨ','ᱱᱩ','ᱱᱪ','ᱱᱫ','ᱱᱬ','ᱱᱭ','ᱱᱮ','ᱱᱯ','ᱱᱰ', 'ᱱᱱ', 'ᱱᱲ', 'ᱱᱳ', 'ᱱᱴ', 'ᱱᱵ', 'ᱱᱶ', 'ᱱᱷ',
                                'ᱳᱚ','ᱳᱛ','ᱳᱜ','ᱳᱝ','ᱳᱞ','ᱳᱟ','ᱳᱠ','ᱳᱡ','ᱳᱢ','ᱳᱣ','ᱳᱤ','ᱳᱥ','ᱳᱦ','ᱳᱧ','ᱳᱨ','ᱳᱩ','ᱳᱪ','ᱳᱫ','ᱳᱬ','ᱳᱭ','ᱳᱮ','ᱳᱯ','ᱳᱰ', 'ᱳᱱ', 'ᱳᱲ', 'ᱳᱳ', 'ᱳᱴ', 'ᱳᱵ', 'ᱳᱶ', 'ᱳᱷ',
                                'ᱴᱚ','ᱴᱛ','ᱴᱜ','ᱴᱝ','ᱴᱞ','ᱴᱟ','ᱴᱠ','ᱴᱡ','ᱴᱢ','ᱴᱣ','ᱴᱤ','ᱴᱥ','ᱴᱦ','ᱴᱧ','ᱴᱨ','ᱴᱩ','ᱴᱪ','ᱴᱫ','ᱴᱬ','ᱴᱭ','ᱴᱮ','ᱴᱯ','ᱴᱰ', 'ᱴᱱ', 'ᱴᱲ', 'ᱴᱳ', 'ᱴᱴ', 'ᱴᱵ', 'ᱴᱶ', 'ᱴᱷ',
                                'ᱵᱚ','ᱵᱛ','ᱵᱜ','ᱵᱝ','ᱵᱞ','ᱵᱟ','ᱵᱠ','ᱵᱡ','ᱵᱢ','ᱵᱣ','ᱵᱤ','ᱵᱥ','ᱵᱦ','ᱵᱧ','ᱵᱨ','ᱵᱩ','ᱵᱪ','ᱵᱫ','ᱵᱬ','ᱵᱭ','ᱵᱮ','ᱵᱯ','ᱵᱰ', 'ᱵᱱ', 'ᱵᱲ', 'ᱵᱳ', 'ᱵᱴ', 'ᱵᱵ', 'ᱵᱶ', 'ᱵᱷ',
                                'ᱶᱚ','ᱶᱛ','ᱶᱜ','ᱶᱝ','ᱶᱞ','ᱶᱟ','ᱶᱠ','ᱶᱡ','ᱶᱢ','ᱶᱣ','ᱶᱤ','ᱶᱥ','ᱶᱦ','ᱶᱧ','ᱶᱨ','ᱶᱩ','ᱶᱪ','ᱶᱫ','ᱶᱬ','ᱶᱭ','ᱶᱮ','ᱶᱯ','ᱶᱰ', 'ᱶᱱ', 'ᱶᱲ', 'ᱶᱳ', 'ᱶᱴ', 'ᱶᱵ', 'ᱶᱶ', 'ᱶᱷ',
                                'ᱷᱚ','ᱷᱛ','ᱷᱜ','ᱷᱝ','ᱷᱞ','ᱷᱟ','ᱷᱠ','ᱷᱡ','ᱷᱢ','ᱷᱣ','ᱷᱤ','ᱷᱥ','ᱷᱦ','ᱷᱧ','ᱷᱨ','ᱷᱩ','ᱷᱪ','ᱷᱫ','ᱷᱬ','ᱷᱭ','ᱷᱮ','ᱷᱯ','ᱷᱰ', 'ᱷᱱ', 'ᱷᱲ', 'ᱷᱳ', 'ᱷᱴ', 'ᱷᱵ', 'ᱷᱶ', 'ᱷᱷ',
                                 ]
    
    # this is a customizeable map : this map is purely based on visual similiarity 
    legacy_maps             =   {'ঀ':'৭',
                                'ᱞ':'᱙',
                                'ᱪ':'᱙',
                                '~':'᱙',
                                '-':'ᱴ',
                                'ᱨᱚ':'ᱨᱮ',
                                '?':'ᱜ'}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------
    nukta_map              =   {'ᱟᱩᱱᱟ':'ᱟᱨ',
                                'ᱵ':'ᱨ.',
                                'ᱫ':'ᱠᱟᱢᱤ',
                                'ᱫᱦ':'ᱫᱷ'}
    diacritic_map           =   {'.':'.',
                                '.':'.',
                                'ᱚᱟ':'ᱛ',
                                '.':'.'}
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C70","\u1C71"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
            * khondo to
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+['ᱴ']+numbers+punctuations)       
    
class devanagari:
    '''
        * vowel and consonant division according to :https://unicode-table.com/en/blocks/devanagari/
        * consonant conjuncts according to: https://en.wikipedia.org/wiki/Devanagari_conjuncts
        * punctuations according to: https://www.learnsanskrit.org/guide/devanagari/numerals-and-punctuation/ 
    '''
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "devanagari"
    nukta                  =   '़'
    vowels                 =   ['ऄ', 'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऌ', 'ऍ', 'ऎ', 'ए', 'ऐ', 'ऑ', 'ऒ', 'ओ', 'औ','ॠ', 'ॡ', 'ॢ', 'ॣ','ॲ','ॳ', 'ॴ', 'ॵ','ॶ', 'ॷ']
    consonants             =   ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'ऩ', 'प', 'फ', 'ब', 
                                'भ', 'म', 'य', 'र', 'ऱ', 'ल', 'ळ', 'ऴ', 'व', 'श', 'ष', 'स', 'ह','क़', 'ख़', 'ग़', 'ज़', 'ड़', 'ढ़', 'फ़', 'य़','ॸ', 'ॹ', 'ॺ']

    vowel_diacritics       =   ['ऺ', 'ऻ','ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॅ', 'ॆ', 'े', 'ै', 'ॉ', 'ॊ', 'ो', 'ौ','ॎ', 'ॏ','ॕ','ॖ', 'ॗ']

    
    consonant_diacritics   =   ['ऀ', 'ँ', 'ं', 'ः']

    numbers                =   ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'] 
    punctuations           =   ['।', '॥', ':', ';', '!', '—', '?', 'ऽ']
    symbols                =   []  
    connector              =   '्'
    
    
    non_gylph_unicodes     =   [] 

    legacy_symbols         =   []      
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
   
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    
    # this is a customizeable map : this map is purely based on visual similiarity 
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------

    nukta_map              =   {'क':'क़',
                                'ख':'ख़',
                                'ग':'ग़',
                                'ज':'ज़',
                                'ड':'ड़',
                                'ढ':'ढ़',
                                'फ':'फ़',
                                'य':'य़',
                                'ळ':'ऴ',
                                'न':'ऩ'}
  
    diacritic_map          =   {'ाे':'ो',
                                'ाै':'ौ',
                                'अा':'आ',
                                'अो':'ओ',
                                'अौ': 'औ',
                                'एे': 'ऐ'}
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)     
    
#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------
class gujarati:
    '''
        * vowel and consonant division according to : https://unicode-table.com/en/blocks/gujarati/
        * consonant conjuncts according to: https://en.wikipedia.org/wiki/Gujarati_script
        * punctuations according to: https://github.com/BengaliAI/syntheticWords/blob/main/coreLib/languages.py
    '''
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "gujarati"
    nukta                  =   '઼'
    vowels                 =   ['અ', 'આ', 'ઇ', 'ઈ', 'ઉ', 'ઊ', 'ઋ', 'ઌ', 'ઍ', 'એ', 'ઐ', 'ઑ', 'ઓ', 'ઔ','ૠ', 'ૡ', 'ૢ', 'ૣ']
    consonants             =   ['ક', 'ખ', 'ગ', 'ઘ', 'ઙ', 'ચ', 'છ', 'જ', 'ઝ', 'ઞ', 'ટ', 'ઠ', 'ડ', 'ઢ', 'ણ', 'ત', 'થ', 'દ', 'ધ', 'ન', 'પ', 'ફ', 'બ', 'ભ', 'મ', 'ય', 'ર', 'લ', 'ળ', 'વ', 'શ', 'ષ', 'સ', 'હ','ૹ']
    vowel_diacritics       =   ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ૃ', 'ૄ', 'ૅ', 'ે', 'ૈ', 'ૉ', 'ો', 'ૌ']
    consonant_diacritics   =   ['ઁ', 'ં', 'ઃ']
    numbers                =   ['૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯']
    punctuations           =   ['ઽ',',',';','।','?','!',':','—',':-',"'",'”','(', ')','{', '}','[',']','√','<','>','=','...','.','-'] 
    symbols                =   ['૱']
    connector              =   '્'
    
    
    # based on unicode range : \u0980-\u09FF
    non_gylph_unicodes     =   ['\u0a80', '\u0a84', '\u0aa9', '\u0ab1', '\u0ab4', '\u0aba', '\u0abb', '\u0ac6', '\u0aca', '\u0ace', '\u0acf', 
                                '\u0ad1', '\u0ad2', '\u0ad3', '\u0ad4', '\u0ad5', '\u0ad6', '\u0ad7', '\u0ad8', '\u0ad9', '\u0ada', '\u0adb', 
                                '\u0adc', '\u0add', '\u0ade', '\u0adf', '\u0ae4', '\u0ae5', '\u0af1', '\u0af2', '\u0af3', '\u0af4', '\u0af5', 
                                '\u0af6', '\u0af7', '\u0af8']

    legacy_symbols         =   []  
    
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    
    # this is a customizeable map : this map is purely based on visual similiarity 
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------
    
    nukta_map              =   {} # NONE

    diacritic_map          =   {'ાે': 'ો',
                                'ાૅ': 'ૉ',
                                'ાૈ': 'ૌ',
                                'અા': 'આ',
                                'અે': 'એ',
                                'અો': 'ઓ',
                                'અૅ': 'ઍ',
                                'અૉ': 'ઑ',
                                'અૈ': 'ઐ',
                                'અૌ': 'ઔ'}
    #---------------------------------------------------normalization maps---------------------------------------------------------
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)     
    
#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------
class odiya:
    '''
        * vowel and consonant division according to : https://unicode-table.com/en/blocks/oriya/
        * consonant conjuncts according to: https://en.wikipedia.org/wiki/Odia_script
        * punctuations according to: https://github.com/BengaliAI/syntheticWords/blob/main/coreLib/languages.py
    '''
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "odiya"
    nukta                  =   '଼'
    vowels                 =   ['ଅ', 'ଆ', 'ଇ', 'ଈ', 'ଉ', 'ଊ', 'ଋ', 'ଌ', 'ଏ', 'ଐ', 'ଓ', 'ଔ','ୠ', 'ୡ']
    consonants             =   ['କ', 'ଖ', 'ଗ', 'ଘ', 'ଙ', 'ଚ', 'ଛ', 'ଜ', 'ଝ', 'ଞ', 'ଟ', 'ଠ', 'ଡ', 'ଢ', 'ଣ', 
                                'ତ', 'ଥ', 'ଦ', 'ଧ', 'ନ', 'ପ', 'ଫ', 'ବ', 'ଭ', 'ମ', 'ଯ', 'ର', 'ଲ', 'ଳ', 'ଵ', 
                                'ଶ', 'ଷ', 'ସ', 'ହ','ଡ଼', 'ଢ଼', 'ୟ','ୱ']
    vowel_diacritics       =   ['ା', 'ି', 'ୀ', 'ୁ', 'ୂ', 'ୃ', 'ୄ', 'େ', 'ୈ','ୋ', 'ୌ','ୢ', 'ୣ']
    consonant_diacritics   =   ['ଁ', 'ଂ', 'ଃ']
    numbers                =   ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯']
    punctuations           =   [',',';','।','?','!',':','—',':-',"'",'”','(', ')','{', '}','[',']','√','<','>','=','...','.','-'] 
    symbols                =   ['୲', '୳', '୴', '୵', '୶', '୷']
    connector              =   '୍'
    
    # based on unicode range : \u0980-\u09FF
    non_gylph_unicodes     =   ['\u0b00', '\u0b04', '\u0b0d', '\u0b0e', '\u0b11', '\u0b12', '\u0b29', '\u0b31', '\u0b34', '\u0b3a', '\u0b3b', 
                                '\u0b45', '\u0b46', '\u0b49', '\u0b4a', '\u0b4e', '\u0b4f', '\u0b50', '\u0b51', '\u0b52', '\u0b53', '\u0b54', 
                                '\u0b58', '\u0b59', '\u0b5a', '\u0b5b', '\u0b5e', '\u0b64', '\u0b65', '\u0b78', '\u0b79', '\u0b7a', '\u0b7b', 
                                '\u0b7c', '\u0b7d', '\u0b7e', '\u0b7f']
    legacy_symbols         =   []  
    
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    
    # this is a customizeable map : this map is purely based on visual similiarity 
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------
    nukta_map              =   {'ଡ':'ଡ଼',
                                'ଢ':'ଢ଼'}
     
    diacritic_map          =   {'ୋ':'ୋ',
                                'ୈା':'ୌ',
                                'ଓୗ':'ଔ',
                                'ଏୗ':'ଐ',
                                'ଅା':'ଆ'}
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)     
        
    
#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------

class tamil:
    '''
        * vowel and consonant division according to : https://unicode-table.com/en/blocks/tamil/
        * consonant conjuncts according to: https://en.wikipedia.org/wiki/Tamil_script
        * punctuations according to: https://github.com/BengaliAI/syntheticWords/blob/main/coreLib/languages.py
    '''
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "tamil"
    nukta                  =   ''  
    vowels                 =   ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ']
    consonants             =   ['க', 'ங', 'ச', 'ஜ', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ன', 'ப', 'ம', 'ய', 'ர', 'ற', 'ல', 'ள', 'ழ', 'வ', 'ஶ', 'ஷ', 'ஸ', 'ஹ']
    vowel_diacritics       =   ['ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை','ொ', 'ோ', 'ௌ']
    consonant_diacritics   =   ['ஂ', 'ஃ']
    numbers                =   ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯','௰', '௱', '௲']
    punctuations           =   [',',';','।','?','!',':','—',':-',"'",'”','(', ')','{', '}','[',']','√','<','>','=','...','.','-']
    symbols                =   ['௳', '௴', '௵','௹','௶', '௷', '௸','௺']
    connector              =   '்' 
    
    # based on unicode range : \u0980-\u09FF
    non_gylph_unicodes     =   ['\u0b80', '\u0b81', '\u0b84', '\u0b8b', '\u0b8c', '\u0b8d', '\u0b91', '\u0b96', '\u0b97', '\u0b98', '\u0b9b', 
                                '\u0b9d', '\u0ba0', '\u0ba1', '\u0ba2', '\u0ba5', '\u0ba6', '\u0ba7', '\u0bab', '\u0bac', '\u0bad', '\u0bba', 
                                '\u0bbb', '\u0bbc', '\u0bbd', '\u0bc3', '\u0bc4', '\u0bc5', '\u0bc9', '\u0bce', '\u0bcf', '\u0bd8', '\u0bd9', 
                                '\u0bda', '\u0bdb', '\u0bdc', '\u0bdd', '\u0bde', '\u0bdf', '\u0be0', '\u0be1', '\u0be2', '\u0be3', '\u0bd1', 
                                '\u0bd2', '\u0bd3', '\u0bd4', '\u0bd5', '\u0bd6', '\u0bd8', '\u0bd9', '\u0bda', '\u0bdb', '\u0bdc', '\u0bdd', 
                                '\u0bde', '\u0bdf', '\u0be0', '\u0be1', '\u0be2', '\u0be3', '\u0be4', '\u0be5', '\u0bfb', '\u0bfc', '\u0bfd', 
                                '\u0bfe', '\u0bff']
    legacy_symbols         =   []  
    
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    # this is a customizeable map : this map is purely based on visual similiarity 
     
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------
     
    nukta_map              =   {} # NONE
     
    diacritic_map          =   {'ொ':'ொ',
                                "ோ":'ோ'} 
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)     
        
    
#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------
class panjabi:
    '''
        * vowel and consonant division according to : https://unicode-table.com/en/blocks/gurmukhi/
        * consonant conjuncts according to: NOT USED
        * punctuations according to: https://github.com/BengaliAI/syntheticWords/blob/main/coreLib/languages.py
    '''
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "panjabi"
    nukta                  =   '਼'
    vowels                 =   ['ਅ', 'ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ','ੲ', 'ੳ']
    consonants             =   ['ਕ', 'ਖ', 'ਗ', 'ਘ', 'ਙ', 'ਚ', 'ਛ', 'ਜ', 'ਝ', 'ਞ', 'ਟ', 'ਠ', 'ਡ', 'ਢ', 'ਣ', 'ਤ', 'ਥ', 
                                'ਦ', 'ਧ', 'ਨ', 'ਪ', 'ਫ', 'ਬ', 'ਭ', 'ਮ', 'ਯ', 'ਰ', 'ਲ', 'ਲ਼', 'ਵ', 'ਸ਼', 'ਸ', 'ਹ','ਖ਼', 
                                'ਗ਼', 'ਜ਼', 'ੜ', 'ਫ਼']
    vowel_diacritics       =   ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', 'ੇ', 'ੈ', 'ੋ', 'ੌ']
    consonant_diacritics   =   ['ਁ', 'ਂ', 'ਃ'] # Not found!
    numbers                =   ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯']
    punctuations           =   [',',';','।','?','!',':','—',':-',"'",'”','(', ')','{', '}','[',']','√','<','>','=','...','.','-']
    symbols                =   []
    connector              =   '੍'
    
    # based on unicode range : \u0980-\u09FF
    non_gylph_unicodes     =   ['\u0a00', '\u0a04', '\u0a0b', '\u0a0c', '\u0a0d', '\u0a0e', '\u0a11', '\u0a12', '\u0a29', '\u0a31', 
                                '\u0a34', '\u0a37', '\u0a3a', '\u0a3b', '\u0a3d', '\u0a43', '\u0a44', '\u0a45', '\u0a46', '\u0a49', 
                                '\u0a4a', '\u0a4e', '\u0a4f', '\u0a50', '\u0a52', '\u0a53', '\u0a54', '\u0a55', '\u0a56', '\u0a57', 
                                '\u0a58', '\u0a5d', '\u0a5f', '\u0a60', '\u0a61', '\u0a62', '\u0a63', '\u0a64', '\u0a65', '\u0a76', 
                                '\u0a77', '\u0a78', '\u0a79', '\u0a7a', '\u0a7b', '\u0a7c', '\u0a7d', '\u0a7e', '\u0a7f']
    legacy_symbols         =   []
    
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    
    # this is a customizeable map : this map is purely based on visual similiarity 
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------
    nukta_map              =   {'ਖ':'ਖ਼',
                                'ਗ':'ਗ਼',
                                'ਜ':'ਜ਼',
                                'ਲ':'ਲ਼',
                                'ਸ':'ਸ਼',
                                'ਫ':'ਫ਼'
                                }
    diacritic_map          =   {'ੇੋ': 'ੌ',
                                'ਾੇ': 'ੀ',
                                'ਾੋ': 'ੀ',
                                'ਅੈ': 'ਐ',
                                'ਅੌ': 'ਔ',
                                'ਅਾ': 'ਆ'}
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)     
        
        
    
#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------
class malayalam:
    '''
        * vowel and consonant division according to: https://unicode-table.com/en/blocks/malayalam/
        * consonant conjuncts according to: Self Generated
        * punctuations according to: https://github.com/BengaliAI/syntheticWords/blob/main/coreLib/languages.py
    '''
    
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "malayalam"
    nukta                  =   '়'
    vowels                 =   ['അ', 'ആ', 'ഇ', 'ഈ', 'ഉ', 'ഊ', 'ഋ', 'ഌ', 'എ', 'ഏ', 'ഐ', 'ഒ', 'ഓ', 'ഔ','ൠ', 'ൡ'] 
    consonants             =   ['ക', 'ഖ', 'ഗ', 'ഘ', 'ങ', 'ച', 'ഛ', 'ജ', 'ഝ', 'ഞ', 'ട', 'ഠ', 'ഡ', 'ഢ', 'ണ', 'ത', 'ഥ', 
                                'ദ', 'ധ', 'ന', 'ഩ', 'പ', 'ഫ', 'ബ', 'ഭ', 'മ', 'യ', 'ര', 'റ', 'ല', 'ള', 'ഴ', 'വ', 'ശ', 'ഷ', 
                                'സ', 'ഹ', 'ഺ']
    vowel_diacritics       =   ['ാ', 'ി', 'ീ', 'ു', 'ൂ', 'ൃ', 'ൄ',     'െ', 'േ', 'ൈ','ൊ', 'ോ', 'ൌ','ൗ','ൢ', 'ൣ']
    consonant_diacritics   =   ['ഀ', 'ഁ', 'ം', 'ഃ', 'ഄ']
    numbers                =   ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯','൘', '൙', '൚', '൛', '൜', '൝', '൞','൰', '൱', '൲','൳', '൴', '൵', '൶', '൷', '൸']
    punctuations           =    [',',';','।','?','!',':','—',':-',"'",'”','(', ')','{', '}','[',']','√','<','>','=','...','.','-']
    symbols                =   ['ഽ', '൏', '൹']

    
    
    connector              =   '്' # There are two other this shit '഻', '഼'
    
    # based on unicode range : \u0980-\u09FF
    non_gylph_unicodes     =   ['\u0d64', '\u0d65', '\u0d50', '\u0d51', '\u0d52', '\u0d53', '\u0d49', '\u0d45', '\u0d11', '\u0d0d']
    legacy_symbols         =   ['ൟ']
    
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    
    # this is a customizeable map : this map is purely based on visual similiarity 
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    
    #---------------------------------------------------normalization maps---------------------------------------------------------
    nukta_map              =   {}
    diacritic_map          =   {} #NONE--<>
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts) 
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
             
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)     
        
        
class sylhetinagri:
    '''
        * according to asif sushmit
    '''
    #-----------------------------------------------------basic-------------------------------------------------------------------
    iden                   =   "sylhetinagri"
    nukta                  =   '' #done
    vowels                 =   ['ꠀ', 'ꠁ', 'ꠃ', 'ꠄ', 'ꠅ'] #done
    consonants             =   ['ꠇ', 'ꠈ', 'ꠉ', 'ꠊ',
                                 'ꠌ', 'ꠍ', 'ꠎ', 'ꠏ',
                                 'ꠐ', 'ꠑ', 'ꠒ', 'ꠓ',
                                 'ꠔ', 'ꠕ', 'ꠖ', 'ꠗ', 'ꠘ',
                                 'ꠙ', 'ꠚ', 'ꠛ', 'ꠜ', 'ꠝ',
                                 'ꠞ', 'ꠟ', 'ꠠ', 'ꠡ', 'ꠢ'] #done
    vowel_diacritics       =   ['ꠣ', 'ꠤ', 'ꠥ', 'ꠦ', 'ꠧ'] #done
    consonant_diacritics   =   ['ꠋ', 'ꠂ', '꠬'] #done
    numbers                =   ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '᱙', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '०', '१', '२', '३', '४', '५', '६', '७', '८', '९']
    punctuations           =   ['।', '॥', ':', ';', '!', '—', '?', 'ऽ', '.', ',']
    symbols                =   ['꠨', '꠩', '꠪', '꠫']
    connector              =   '꠆' #done
    non_gylph_unicodes     =   []
    legacy_symbols         =   []
    non_chars              =   numbers+punctuations+symbols+non_gylph_unicodes+legacy_symbols
    #-----------------------------------------------------basic-------------------------------------------------------------------
    #---------------------------------------------------changeables----------------------------------------------------------------
    conjuncts              =   []
    # this is a customizeable map : this map is purely based on visual similiarity
    legacy_maps            =   {}
    #---------------------------------------------------changeables----------------------------------------------------------------
    #---------------------------------------------------normalization maps---------------------------------------------------------
    nukta_map              =   {}
    diacritic_map           =   {'ꠦꠣ':'ꠧ',
                                'ꠣꠦ':'ꠧ'}
    #---------------------------------------------------normalization maps---------------------------------------------------------
    diacritics             =   sorted(vowel_diacritics+consonant_diacritics)
    used                   =   sorted(vowels+consonants+vowel_diacritics+consonant_diacritics+numbers)
    valid                  =   sorted([' ']+used+punctuations+[connector]+["\u1C71","\u1C70"])
    complex_roots          =   sorted([' ']+vowels+consonants+numbers+punctuations+symbols+conjuncts)
    # these unicodes can not start a word
    invalid_starts         =   sorted(diacritics+[connector])
    # invalid connector cases
    '''
        a connector can not be sorrounded by/ can not come after or before:
            * the vowels
            * the diacritics
            * another connector [double consecutive hosonto]
    '''
    invalid_connectors     =    sorted(invalid_starts+vowels+numbers+punctuations)

#--------------------------------------------------------------------------------------------------------------------------------------------
#############################################################################################################################################
#--------------------------------------------------------------------------------------------------------------------------------------------
languages={}
languages["english"]    =english
languages["olchiki"]     =olchiki
languages["devanagari"] =devanagari
languages["gujarati"]   =gujarati
languages["odiya"]      =odiya
languages["tamil"]      =tamil
languages["panjabi"]    =panjabi
languages["malayalam"]  =malayalam
languages["sylhetinagri"]=sylhetinagri
