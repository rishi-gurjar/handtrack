import requests
import time
import random

def run_script():
    while True:
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        for num in numbers:
                    # Generate a random color in hexadecimal format
            color = "{:06x}".format(random.randint(0, 0xFFFFFF))
            
            
                    # Output the current number and the new color
            print(f"Number: {num}, Color: {color}")
            #print(color)
                    # Wait for 1 second before the next iteration
            time.sleep(5)    
        
        print("PRE GET COLOR:", color)
        send = "http://127.0.0.1:5002/change/" + str(color)
        response = requests.get(send)  # Note the port number

        if response.status_code == 200:
            print("Color changed successfully.")
        else:
            print("Failed to change color.")
