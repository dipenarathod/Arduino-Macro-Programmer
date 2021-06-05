# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:37:15 2020

@author: Dipen

V2.6 Higlights:
    No need to enter number of rows and columns
"""
from tkinter import *
root=Tk()
root.title("Macro Programmer")

#1st Screen for rows, columns
e1=Entry(root)#Entry field Number 1 in root window
e1.insert(0,"Row Pins")#Default text in Entry Field 1
e1.grid(row=0,column=0)#Position of Entry Field 1 in root window
e2=Entry(root)#Entry field Number 2 in root window
e2.insert(0,"Column Pins")#Default text in Entry Field 2
e2.grid(row=1,column=0)#Position of Entry Field 2 in root window
# e4=Entry(root)
# e4.insert(0,"Column Pin Numbers")
# e4.grid(row=3,column=0)
#CharacterString="{{'1','2','3','4','5','6','7','8'},{'9','0','a','b','c','d','e','f'},{'g','h','i','j','k','l','m','n'},{'o','p','q','r','s','t','u','v'},{'w','x','y','z','A','B','C','D'},{'E','F','G','H','I','J','K','L'},{'M','N','O','P','Q','R','S','T'},{'U','V','W','X','Y','Z','`','~'}}"
CharacterList=[['1','2','3','4','5','6','7','8'],#Character Matrix for Keypad Mapping
               ['9','0','a','b','c','d','e','f'],
               ['g','h','i','j','k','l','m','n'],
               ['o','p','q','r','s','t','u','v'],
               ['w','x','y','z','A','B','C','D'],
               ['E','F','G','H','I','J','K','L'],
               ['M','N','O','P','Q','R','S','T'],
               ['U','V','W','X','Y','Z','`','~']]

Matrix=""#This will store the extracted matrix from CharacterList depending on the number of rows and columns
profileNames=""

def code_gen():
    #global inputWindow
    global inputs
    global code
    code="""
#include <Keypad.h>
#include "HID-Project.h"
    
int profile_index=0;//To select profile
const byte ROWS = """+str(rows)+"""; //rows
const byte COLS = """+str(cols)+"""; //columns

char keys[ROWS][COLS] ={"""+Matrix+"""};
    
byte rowPins[ROWS] = {"""+row_pins+"""}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {"""+col_pins+"""}; //connect to the column pinouts of the keypad
    
//Create an object of keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
    
void setup(){
   Serial.begin(9600);
   Keyboard.begin();
}
      
void loop(){
    char key = keypad.getKey();// Read the key  
    """  
    #profile_code="if(profile_index=={m})"
    for r in range(rows):
        condition=""
        for c in range(cols):
            condition+= f"if(key=='{CharacterList[r][c]}'){{ \n" 
            temp=inputs[r][c].get().split('+')
            for t in temp:
                if(t.startswith('KEY')):
                    condition+=f"Keyboard.press({t}); \n"
                    continue
                if(t.startswith('MEDIA') or t.startswith('CONSUMER') or t.startswith('HID_CONSUMER')):
                    condition+=f"Consumer.write({t});\n"
                    continue
                if(t.startswith('SYSTEM') or t.startswith('HID_SYSTEM') or t.startswith('HID_APPLICATION') or t.startswith('HID_D_PAD')):
                    condition+=f"System.write({t});"
                    continue
                if(t.startswith("Println")):
                    condition+=f'Keyboard.println("{t[7:]}"); \n'
                    continue
                if(t.startswith("Print")):
                    condition+=f'Keyboard.print("{t[5:]}"); \n'
                    continue
                else:
                    condition+=f"Keyboard.press('{t}'); \n"
                    continue
                       
            condition+=f"Keyboard.releaseAll();\n"
            condition+=f"}}\n"
        code+=condition     
    code+=f"}}\n"
    text=Text(inputWindow,height=5,width=32)
    text.insert(INSERT,code)
    text.grid()
                       
    
def openwindow():
    try:
        global rows
        global cols
        global number_of_pins
        global code
        rows=len(e1.get().split(','))
        cols=len(e2.get().split(','))
        
        global row_pins
        global col_pins  
        row_pins=e1.get()
        col_pins=e2.get()
                
        #Matrix Extraction
        global Matrix
        for i in range(rows):
            Matrix+="{"
            for j in range(cols):
                #Matrix+="'"+CharacterList[i][j]+"',"
                Matrix+=f"'{CharacterList[i][j]}',"
            Matrix=Matrix[:-1]#Removes the extra comma
            Matrix+="},\n"
        global inputs
        inputs=[]
        global inputWindow
        inputWindow=Toplevel(root)
        inputWindow.title("Enter Inputs")
        for i in range(rows):
            temp_col=[]
            for j in range(cols):
                temp_col.append(Entry(inputWindow))
                temp_col[j].grid(row=i,column=j)
            inputs.append(temp_col)
        b2=Button(inputWindow,text="generate code",command=code_gen)
        b2.grid()  
              
    except Exception as E:
        l=Label(root,text=E)#
        l2=Label(root,text=E)
        l.grid()
        l2.grid()

b1=Button(root,text="Generate Input fields",command=openwindow)
b1.grid(row=4,column=0)        
root.mainloop()
