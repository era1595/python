#A code that allows you to automatically type what you want, as many times as you want. (if you move the mouse cursor to the top-left corner of the screen, the program will stop)
import pyautogui
import time

pyautogui.FAILSAFE = True

x=input("Enter the Data You Want to Print:")
c=int(input("Enter How Many Times You Want to Print:"))
z=float(input("Enter the Typing Speed:"))
y=input("Should the Enter Button Be Pressed After Typing (Y/N):")

print("\nWARNING: The script will take over keyboard control.")
confirmation = input("Are you sure you want to start the writing process? (Y/N): ").strip().upper()

if confirmation == "Y": # Changed from "E" to "Y" for English confirmation
    if y.upper() == "Y":
        print("It will start typing in 5 seconds. To stop, move the mouse to the top-left corner.")
        time.sleep(5)
        for i in range(0,c):
            pyautogui.typewrite(x)
            pyautogui.press("enter")
            time.sleep(z)
        print("Typing Process Finished")
    elif y.upper() == "N":
        print("It will start typing in 5 seconds. To stop, move the mouse to the top-left corner.")
        time.sleep(5)
        for i in range(0,c):
            pyautogui.typewrite(x)
            time.sleep(z)
        print("Typing Process Finished")
    else:
        print("Invalid 'Enter' selection. Operation cancelled.")
else:
    print("The writing process was cancelled by the user.")
