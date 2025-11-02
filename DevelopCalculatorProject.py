""" Note :- Make windows installer setup Inno setup
31-07-2025
Show a custom license page

Add versioning or update support

"""
# Progressing Code
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import customtkinter as ctk
import urllib.request
import os 
import pygame  # For Click Sound
# pyinstaller
import math

def Run():
        icondownloader()
        download_sound()
        a = Calculator()
        a.mainloop()

def icondownloader():
    url = "https://i.postimg.cc/XNRmB6YY/Calculator.png"    # PostImage For direct download link
    filename = "Cal.png"
    if  not os.path.exists(filename):
        urllib.request.urlretrieve(url , filename)

def download_sound():
    if not os.path.exists("click.mp3"):
        url = "https://www.soundjay.com/buttons/button-20.mp3"
        urllib.request.urlretrieve(url , "click.mp3")


class Calculator(tk.Tk):
    def __init__(self): 
        super().__init__()
    

# Basic
        
        self.title("Calculator By ARYAN")
        self.resizable(False , False)
        self.geometry("340x520")
        icon = PhotoImage(file=("Cal.png"))
        self.iconphoto(False , icon)
        self.button_refs = {}  # To store button widgets.  Class Empty Dict
        self.flash_tasks = {}  # Tracks after_id per button
        self.original_colors = {}  # Stores original fg_color

# Entry
        self.expression = "0"
        self.variable = tk.StringVar(value="0")
        self.entry = ctk.CTkEntry(self , textvariable=self.variable , font=("Segoe UI", 24) , justify="right",corner_radius=10,
            height=60, text_color="#ffffff", fg_color= "#000000" , bg_color="#000000")
        self.entry.pack(side="top" ,fill='x', ipadx=20 , ipady=20)


#Button 
        buttons = [
            ("C" , "%" , "CE" , "⌫"),
            ("π", "√", "x²","X" ),
            ("7" , "8" , "9" , "÷"),
            ("4" , "5" , "6" ,"+" ),
            ("1" , "2" , "3" ,"-" ),
            ("." , "0" , "="),

        ]   
        
       # Button Frame Creation and Layout
        for row_buttons in buttons:
            row = tk.Frame(self , bg="#121212")
            row.pack(fill="both", expand=True)
            for button in row_buttons:
                # Default colors
                color = "#1a1a1a"
                hover = "#333333"

                # Custom color logic
                if button in ("C", "⌫", "CE"):
                    color = "#8A0000"  # Dark red
                    hover = "#A52A2A"
                elif button == "=":
                    color = "#006400"  # Dark green
                    hover = "#228B22"
                elif button in ("+", "-", "X", "÷"):
                    color = "#00008B"  # Dark blue
                    hover = "#4169E1"

                # Create the customtkinter button
                btn = ctk.CTkButton(
                    master=row,
                    text=button,
                    command=lambda val=button: self.on_click_btn(val),
                    font=("Segoe UI", 18),
                    width=80,
                    height=60,
                    corner_radius=15,
                    fg_color=color,
                    hover_color=hover,
                    text_color="white",
                )
                btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)
                self.button_refs[button] = btn  # Store reference
                self.original_colors[button] = color



        self.bind("<Key>" , self.presskey)
       
    # Sound

    def play_click_sound(self):
        pygame.mixer.init()
        sound = pygame.mixer.Sound("click.mp3")

        pygame.mixer.Sound.play(sound)



# Function For Response on Clicking Keys.
    def on_click_btn(self , value):
        self.play_click_sound()
        if value == "X":
           value = "*"
        elif value == "÷":
          value = "/"

# Clear     
        if value == "C":
            self.expression = ""
            self.variable.set(self.expression)
# BackSpace
        elif value == "⌫":
            self.expression = self.expression[:-1]
            self.variable.set(self.expression)
# Clear all
        elif value == "CE":
            self.expression = ""
            self.variable.set(self.expression)

# Equal
        elif value == "=":
            try:
                result = eval(self.variable.get())
                if isinstance(result , float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self.variable.set(self.expression)
            except:
                self.expression = "Error"
                self.variable.set(self.expression)
# Percentage                       
        elif value == "%":
            try:
                self.expression += "/100"
                result = str(eval(self.expression))
                self.expression = result
                self.variable.set(result)
        
            except:
                self.expression = ""
                self.variable.set(self.expression)
# PI
        elif value == "π":
            try:
                self.expression = str(eval(self.expression)*math.pi)
                self.variable.set( self.expression)
            except :
                self.expression = "Error"
                self.variable.set(self.expression)
# Square root
        elif value == "√" :
            try:
                result = math.sqrt(eval(self.expression))
                if isinstance(result,float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self.variable.set(self.expression)

            except :
                self.expression = "Error"
                self.variable.set(self.expression)  
        elif value == "x²":
            try:
                self.expression = str(eval(self.expression)**2)
                self.variable.set(self.expression)
            except:
                self.expression = "Error"
                self.variable.set(self.expression)
# Multiple Value Operator Handling
        elif value in "+-*/":
            if self.expression and self.expression[-1] in "+-*/":
                # Replace last operator with the new one
                self.expression = self.expression[:-1] + value
            else:
                self.expression += value
                self.variable.set(self.expression)
# Last End
        else:
            # Replace Starting 0 With Digit
            if self.expression == "0" and value.isdigit():
                self.expression = value

            elif value == ".":
                # Split the current expression by operators to get the current number segment
                operators = "+-*/"
                last_num = ""
                for i in range(len(self.expression) - 1, -1, -1):
                    if self.expression[i] in operators:
                        break
                    last_num = self.expression[i] + last_num
                # If dot already in current number, skip adding another
                if "." in last_num:
                    return
                else:
                    self.expression += value

            else:
                self.expression += value

            self.variable.set(self.expression)


    
# Function For Binding Keyboard Keys With Calculator Keys.
    def presskey(self , event):
        char = event.char
        keysym = event.keysym
        valid_keys = "0123456789+-=/*()."
        key_map = {
            "Return" : "=" ,
            "BackSpace" : "⌫",
            "Escape" : "C"
        }
# Map Key
        key = key_map.get(keysym , char)


# Ignore modifier keys
        if keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock"):
            return
            # Only respond if the key is valid
        if key in self.button_refs:
            self.flash_button(key)



        if keysym == "Return":
            self.on_click_btn("=")
        elif keysym == "BackSpace":
            self.on_click_btn("⌫")
        elif char in valid_keys :
            self.on_click_btn(char)


    def flash_button(self , key):
        btn = self.button_refs.get(key)
        if not btn :
            return
    # Cancel any existing scheduled restore
        if key in self.flash_tasks:
            self.after_cancel(self.flash_tasks[key])
            
        btn.configure(fg_color = "#555555")
        
        # Schedule restore to original color
        def restore():
            btn.configure(fg_color=self.original_colors.get(key, "#1a1a1a"))
            self.flash_tasks.pop(key, None)  # Remove completed task
 # Schedule and store after_id
        after_id = self.after(150, restore)
        self.flash_tasks[key] = after_id



        


Run()





