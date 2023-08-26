
from __future__ import print_function
#-------------------------------------------
# imports
#-------------------------------------------
import os
from tabnanny import verbose 
import unittest
from olunicodenormalizer import Normalizer
norm=Normalizer(allow_english=False)
ennorm=Normalizer(allow_english=True)
#-------------------------------------------
# unittestcase
#-------------------------------------------
class TestWordCleaner(unittest.TestCase):
    def test_values(self):
        '''
            test known failure cases
        '''
   
        self.assertEqual(norm('ᱵᱤᱨᱵᱟ.ᱛᱟ')["normalized"],'ᱵᱤᱨᱵᱟᱱᱛᱟ')
        
        self.assertEqual(norm('ᱵᱟᱨ')["normalized"],'ᱵᱟᱨ')
      
        self.assertEqual(norm('ᱦᱟᱛᱟᱱᱜᱞᱟᱥᱤᱨ')["normalized"],'ᱡᱩᱨᱚᱣ')

        self.assertEqual(norm('ᱢᱟᱨᱮ')["normalized"],'ᱡᱩᱨᱚᱣᱜᱮ')
       

        self.assertEqual(norm('ᱟᱨᱦᱩ.')["normalized"],'ᱡᱟᱥᱛᱤ')

        self.assertEqual(norm('ᱴᱮᱭᱜᱟ')["normalized"],'ᱴᱤᱭᱜᱟᱠ')
    
        self.assertEqual(norm('ᱟᱨᱤᱪᱦᱟᱞᱤ')["normalized"],'ᱟᱨᱤᱪᱟᱞᱤ')
 
        self.assertEqual(norm('ᱡᱟᱜᱟ')["normalized"],'ᱫᱤᱥᱚᱢ')
       
        self.assertEqual(norm('ᱛᱟᱦᱤᱱ ᱠᱟᱱᱟᱭᱮ')["normalized"],'ᱦᱟᱤᱱ')
       
        self.assertEqual(norm('ᱞᱟᱜᱮ')["normalized"],'ᱞᱟᱜᱮ')
       
        self.assertEqual(norm('ᱭᱟ')["normalized"],'ᱭᱟ')

   
        self.assertEqual(norm('ᱡᱚᱢ')["normalized"],'ᱱᱮᱭᱟᱨᱮ')
        
        self.assertEqual(norm('ᱱᱮᱛᱣᱚᱨᱠ')["normalized"],'ᱱᱮᱛᱣᱚᱨᱠ')
        
        
        self.assertEqual(norm('ᱫᱩᱱᱫᱩ')["normalized"],'ᱫᱩ.ᱫᱩ')
       
        self.assertEqual(norm('ᱢᱮᱫᱴᱮᱱ')["normalized"],'ᱢᱮᱫᱴᱮ')
        
       
        self.assertEqual(norm('ᱠᱦᱚᱭᱮ')["normalized"],'ᱱᱟᱨᱤᱠᱦᱚᱭᱮ')
        
        self.assertEqual(norm('ᱯᱚᱥᱴᱜᱨᱟᱫᱩᱜᱟᱴᱮ')["normalized"],'ᱯᱚᱥᱴᱜᱨᱟᱫᱩᱜᱟᱴᱮ')
        
        self.assertEqual(norm('ᱞᱟᱭᱱᱮ')["normalized"],'ᱞᱟᱭ.ᱮ')
        
        self.assertEqual(norm('ᱴᱩᱨᱟᱱᱴ')["normalized"],'ᱟᱜᱮᱨ')
        
        
        
        
        
        ### case: multiple folas
        self.assertEqual(norm('ᱟᱱᱫᱫᱫᱫ')["normalized"],'ᱵᱟᱱᱜ')

        ### case: complex roots
        self.assertEqual(norm('ᱠᱩᱠᱢᱩ')["normalized"],'ᱠᱩᱠᱢᱩ')
        

        # Dummy Non-Olchiki,Numbers and Space cases/ Invalid start end cases
        # english
        self.assertEqual(norm('ASD1234')["normalized"],None)
        self.assertEqual(ennorm('ASD1234')["normalized"],'ASD1234')
        # random
        self.assertEqual(norm('ᱱᱮᱭᱟᱜᱮ')["normalized"],'ᱛ')
        self.assertEqual(norm('ᱜᱩᱱᱨᱩ')["normalized"],"ᱥᱩᱨ")
        # Ending
        self.assertEqual(norm("ᱟᱱᱟᱨᱤ")["normalized"],"ᱟ.ᱟᱨᱤ")

        #--------------------------------------------- insert your assertions here----------------------------------------
        '''
            ###  case: give a comment about your case
            ## (a) invalid text==(b) valid text <---- an example of your case
            self.assertEqual(norm(invalid text)["normalized"],expected output)
                        or
            self.assertEqual(ennorm(invalid text)["normalized"],expected output) <----- for including english text
            
        '''
        # your case goes here-
        
    def test_types(self):
        '''
            test the invalid input types
        '''
        # int
        self.assertRaises(TypeError,norm,123)
        # float
        self.assertRaises(TypeError,norm,123.456)
        # boolean
        self.assertRaises(TypeError,norm,True)
        # complex
        self.assertRaises(TypeError,norm,3+4j)
        # list
        self.assertRaises(TypeError,norm,['ᱵᱤᱨᱵᱟᱱᱛᱟ','ᱡᱩᱨᱚᱣ'])

        
        
        


        
        
        
                


                
                