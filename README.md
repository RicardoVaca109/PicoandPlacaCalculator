**PICO y PLACA CALCULATOR**
**Description:**
It is a calculator that allows the user to input 3 data entries:

**How It Works:**
The user inputs three data information:
-Vehicle license plate
-A date
-A time

And depending on the following restrictions:
**Day	    |   Plates that are not allowed to circulate**
Monday    |   Plates ending in 1 and 2
Tuesday	  |   Plates ending in 3 and 4
Wednesday	|   Plates ending in 5 and 6
Thursday	|   Plates ending in 7 and 8
Friday	  |   Plates ending in 9 and 0

It displays a message to confirm whether or not the vehicle is restricted by 'Pico y Placa'.

**The project uses the following technologies:**
**Backend:** Python with the Flask framework
**Frontend:** HTML with Bootstrap
I chose these technologies because they are simple to use, easy to deploy, and Python 
allows for fast development — from simple scripts to more robust applications.

**Challenges:**
One of the main challenges I faced was my limited knowledge of testing, so automated tests were not implemented.

**How to Run Project:**
Follow these steps to run the project locally. It is recommended to use a virtual environment to manage dependencies.

**1) Clone the Repository:**
-git clone https://github.com/RicardoVaca109/PicoandPlacaCalculator.git
-cd PicoandPlacaCalculator

**2) Create a virtual enviroment:**
On the root project path in terminal put the next command
*macOS and Linux:
-python3 -m venv venv

*Windows
-python -m venv venv

**4) Activate virtual enviroment:**
On the root project path in terminal put the next command:
*macOs:
source venv/bin/activate

*Linux:
cd venv/bin/activate

*Windows:
(Command Prompt)
cd venv/Scripts/activate 
or
(Windows PowerShell)
cd venv/Scripts/Activate.ps1
   
**5) Install Dependencies:**
Run the following commands on the root project folder outside venv folder

*pip install -r requirements.txt

These installs all the dependencies needed in order to run de project properly
   
**6) Run the application:**
Then in the same path run the following:
*macOS and Linux:
python3 app.py

*Windows:
python app.py

**Once the server is up run the application in http://localhost:5000**

**How to use the Project:**
When the server is up you should go to the http://localhost:5000 in order to enter the application.
You will see a user interface with three input fields:
-Vehicle license plate
-Date
-Time
Fill in all three fields, then click the "Calcular Pico y Placa" button. The application will display a 
message indicating whether or not the vehicle is restricted from circulating based on the Pico y Placa rules.



