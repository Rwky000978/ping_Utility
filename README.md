Ping Status Checker
This simple Python script uses the Tkinter GUI library to create a graphical interface for checking the status of specified servers through the ping command. The script allows users to input a list of IP addresses, and it continuously pings each IP in the list, displaying the response time and status (Online/Offline) in a user-friendly interface.

Prerequisites
Python 3.x
Tkinter library (usually included in standard Python installations)
Usage
Clone the repository or download the script.
Open the script in a text editor and add the IP addresses you want to monitor to the data array.
Run the script using the command: python script_name.py
The GUI window will display the status of the specified IP addresses, updating every second.
Generating Executable (Windows)
You can generate an executable (.exe) file from the script using auto-py-to-exe. Follow these steps:

Install auto-py-to-exe using the command: pip install auto-py-to-exe
Run the following command to open the GUI for auto-py-to-exe: auto-py-to-exe
Load the script, configure options if needed, and click "Convert .py to .exe."
The executable file will be generated in the output directory.

Note
The script uses threading to ping multiple IP addresses simultaneously, providing real-time updates.
The scrolledtext module is utilized to handle longer output, allowing for easier reading.
The script automatically updates the status every second.
Feel free to customize the script to suit your needs and contribute to its development. If you encounter any issues or have suggestions, please create an issue in the repository. Happy pinging :)
