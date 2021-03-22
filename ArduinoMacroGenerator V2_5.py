# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:37:15 2020

@author: Dipen

V2.5 Higlights:
    Using HID-Project.h instead of Keyboard.h
    Can print now using "Print" before phrase
    can print with along with new line using Println before phrase
"""
from tkinter import *
root=Tk()
root.title("Macro Programmer")

#1st Screen for rows and columns
e1=Entry(root)
e1.insert(0,"Number of Rows")
e1.grid(row=0,column=0)
e2=Entry(root)
e2.insert(0,"Number of Columns")
e2.grid(row=1,column=0)
e3=Entry(root)
e3.insert(0,"Row Pin numbers")
e3.grid(row=2,column=0)
e4=Entry(root)
e4.insert(0,"Column Pin Numbers")
e4.grid(row=3,column=0)
#CharacterString="{{'1','2','3','4','5','6','7','8'},{'9','0','a','b','c','d','e','f'},{'g','h','i','j','k','l','m','n'},{'o','p','q','r','s','t','u','v'},{'w','x','y','z','A','B','C','D'},{'E','F','G','H','I','J','K','L'},{'M','N','O','P','Q','R','S','T'},{'U','V','W','X','Y','Z','`','~'}}"
CharacterList=[['1','2','3','4','5','6','7','8'],['9','0','a','b','c','d','e','f'],['g','h','i','j','k','l','m','n'],['o','p','q','r','s','t','u','v'],['w','x','y','z','A','B','C','D'],['E','F','G','H','I','J','K','L'],['M','N','O','P','Q','R','S','T'],['U','V','W','X','Y','Z','`','~']]

Matrix=""
def code_gen():
    #global inputWindow
    global inputs
    text=Text(inputWindow,height=5,width=32)
    code='''
#include <Keypad.h>
#include "HID-Project.h"
    
const byte ROWS = '''+str(rows)+'''; //rows
const byte COLS = '''+str(cols)+'''; //columns
    
char keys[ROWS][COLS] ='''+Matrix+''';
    
byte rowPins[ROWS] = {'''+row_pins+'''}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {'''+col_pins+'''}; //connect to the column pinouts of the keypad
    
//Create an object of keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
    
void setup(){
   Serial.begin(9600);
   Keyboard.begin();
}
      
void loop(){
    char key = keypad.getKey();// Read the key  
    '''  
    for r in range(rows):
        condition=""
        for c in range(cols):
            condition+= f"if(key=='{CharacterList[r][c]}'){{ \n" 
            temp=inputs[r][c].get().split('+')
            for t in temp:
                if(t.startswith('KEY')):
                    condition+=f"Keyboard.press({t}); \n"
                    continue
                if(t.startswith('MEDIAN') or t.startswith('CONSUMER') or t.startswith('HID_CONSUMER')):
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
                       
                # else:
                #     if("Print" in t):
                #         condition+=f'Keyboard.print("{t[5:]}"); \n'
                #     elif("Println" in t):
                #         condition+=f'Keyboard.println("{t[5:]}"); \n'
                #     else:
                #         condition+=f"Keyboard.press('{t}'); \n"
                    
            condition+=f"Keyboard.releaseAll();\n"
            condition+=f"}}\n"
        code+=condition     
    code+=f"}}\n"
    text.insert(INSERT,code)
    text.grid()
    
def openwindow():
    global e1
    global e2
    global e3
    global e4
    try:
        global rows
        global cols
        rows=int(e1.get())
        cols=int(e2.get())
        
        global row_pins
        global col_pins  
        row_pins=e3.get()
        col_pins=e4.get()
        
        global Matrix
        Matrix="{"
        for i in range(rows):
            Matrix+="{"
            for j in range(cols):
                Matrix+="'"+CharacterList[i][j]+"',"
            Matrix=Matrix[:-1]
            Matrix+="},\n"
        Matrix+="}"
            
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
        l=Label(root,text="Input must be a natural number")
        l2=Label(root,text=E)
        l.grid()
        l2.grid()
        

b1=Button(root,text="Generate Input fields",command=openwindow)
b1.grid(row=4,column=0)

root.mainloop()
