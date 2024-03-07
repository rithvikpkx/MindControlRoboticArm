import serial

# Define the COM port and baud rate
COM_PORT = 'COM5'  # Change this to the appropriate COM port
BAUD_RATE = 9600

# Open the serial port
ser = serial.Serial(COM_PORT, BAUD_RATE)

try:
    while True:
        # Prompt the user to enter a number
        user_input = input("Enter a number (1 to 5 or 99): ")
        
        # Check if the input is valid
        if user_input.isdigit():
            num = int(user_input)
            if num in [1, 2, 3, 4, 5, 99]:
                # Write the number to the serial port
                ser.write(str(num).encode())
                print(f"Sent: {num}")
            else:
                print("Invalid input. Please enter a number between 1 and 5 or 99.")
        else:
            print("Invalid input. Please enter a valid number.")

finally:
    # Close the serial port
    ser.close()
