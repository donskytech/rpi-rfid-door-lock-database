# rpi-rfid-door-lock-database
Raspberry Pi RFID Door Lock with Database Interface  

![Featured Image](https://user-images.githubusercontent.com/69466026/201009896-1e8e23ca-f5e9-4bb0-ad92-9e40254c0dfa.jpg)


Complete writeup of this project: [Raspberry Pi RFID Door Lock System with Database](https://www.donskytech.com/raspberry-pi-rfid-door-lock-system-with-database/)

## How to run this project in your Raspberry Pi

1.  Clone the project in any available folder in your raspberry pi  
```
git clone https://github.com/donskytech/rpi-rfid-door-lock-database
cd rpi-rfid-door-lock-database
```  
2.  Create virtual environment  
`python -m venv .venv`  
3.  Activate the virtual environment  
`source .venv/bin/activate`  
4.  Install the dependencies
`pip install -r requirements.txt`  
5.  Edit the rfid_door_lock.py and point it to where you installed the REST API Application.  For more details on this then please look at the write up of this project.  
6.  Run the project  
`python rfid_door_lock.py`  
7.  To exit the virtual environment then type this code  
`deactivate`  

For any comments or suggestions or questions then send me a message.  
HAPPY EXPLORING!
