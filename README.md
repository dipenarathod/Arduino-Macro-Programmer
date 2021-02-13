# Macro Programmer for HID compatible microcontrollers (eg: Atmega 32u4 based boards)
C code generator + GUI to easily generate HID programs for HID compatible microcontrollers 

Supports upto a 64 Key keyboard with a 8x8 layout.

Connect keyboard matrix to the following pins on your microcontroller:

For Rows:2,3,4,5,6,7,8,9. Connect only the number of pins that are required(eg: If your keyoard matrix only has 3 rows, connect the 3 pins to pin no. 2,3,4 of your microcontroller) 

For Columns:10,16,14,15,A0,A1,A2,A3. Connect only the number of pins that are required(eg: If your keyoard matrix only has 3 columns, connect the 3 pins to pin no. 10,16,14 of your microcontroller) 

The above mentioned values can be found on lines 44 and 45.
