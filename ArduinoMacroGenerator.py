# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:37:15 2020

@author: Dipen
"""
from tkinter import *
root=Tk()
root.title("Macro Programmer")

#1st Screen for rows and columns
e1=Entry(root)
e1.insert(0,"Rows")
e1.grid(row=0,column=0)
e2=Entry(root)
e2.insert(0,"Columns")
e2.grid(row=1,column=0)

#CharacterString="{{'1','2','3','4','5','6','7','8'},{'9','0','a','b','c','d','e','f'},{'g','h','i','j','k','l','m','n'},{'o','p','q','r','s','t','u','v'},{'w','x','y','z','A','B','C','D'},{'E','F','G','H','I','J','K','L'},{'M','N','O','P','Q','R','S','T'},{'U','V','W','X','Y','Z','`','~'}}"
CharacterList=[['1','2','3','4','5','6','7','8'],['9','0','a','b','c','d','e','f'],['g','h','i','j','k','l','m','n'],['o','p','q','r','s','t','u','v'],['w','x','y','z','A','B','C','D'],['E','F','G','H','I','J','K','L'],['M','N','O','P','Q','R','S','T'],['U','V','W','X','Y','Z','`','~']]


def code_gen():
    #global inputWindow
    global inputs
    text=Text(inputWindow,height=5,width=32)
    code='''
#include <Keypad.h>
#include<Keyboard.h>
    
const byte ROWS = 8; //rows
const byte COLS = 8; //columns
    
char keys[ROWS][COLS] = {
      {'1','2','3','4','5','6','7','8'},
      {'9','0','a','b','c','d','e','f'},
      {'g','h','i','j','k','l','m','n'},
      {'o','p','q','r','s','t','u','v'},
      {'w','x','y','z','A','B','C','D'},
      {'E','F','G','H','I','J','K','L'},
      {'M','N','O','P','Q','R','S','T'},
      {'U','V','W','X','Y','Z','`','~'}
};
    
byte rowPins[ROWS] = {2,3,4,5,6,7,8,9}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {10,16,14,15,A0,A1,A2,A3}; //connect to the column pinouts of the keypad
    
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
                if('KEY' in t):
                    condition+=f"Keyboard.press({t}); \n"
                else:
                    condition+=f"Keyboard.press('{t}'); \n"
                    
            condition+=f"Keyboard.releaseAll();\n"
            condition+=f"}}\n"
        code+=condition     
    code+=f"}}\n"
    text.insert(INSERT,code)
    text.grid()
    
def openwindow():
    global e1
    global e2
    try:
        global rows
        global cols
        rows=int(e1.get())
        cols=int(e2.get())
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
        l.grid(row=3,column=0)
        l2.grid(row=4,column=0)
        

b1=Button(root,text="Generate Input fields",command=openwindow)
b1.grid(row=2,column=0)

root.mainloop()
