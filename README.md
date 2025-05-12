**PICO y PLACA CALCULATOR** <br>
**Description:** <br>
It is a calculator that allows the user to input 3 data entries:<br>

**How It Works:** <br>
The user inputs three data information:<br>
-Vehicle license plate<br>
-A date<br>
-A time<br>

And depending on the following restrictions:<br>
**Day	    |   Plates that are not allowed to circulate** <br>
Monday    |   Plates ending in 1 and 2<br>
Tuesday	  |   Plates ending in 3 and 4<br>
Wednesday	|   Plates ending in 5 and 6<br>
Thursday	|   Plates ending in 7 and 8<br>
Friday	  |   Plates ending in 9 and 0<br>

It displays a message to confirm whether or not the vehicle is restricted by 'Pico y Placa'.<br>

**The project uses the following technologies:** <br>
**Backend:** Python with the Flask framework<br>
**Frontend:** HTML with Bootstrap<br>
I chose these technologies because they are simple to use, easy to deploy, and Python <br>
allows for fast development — from simple scripts to more robust applications.<br>

**Challenges:** <br>
One of the main challenges I faced was my limited knowledge of testing, so automated tests were not implemented.<br>

**How to Run Project:** <br>
Follow these steps to run the project locally. It is recommended to use a virtual environment to manage dependencies.<br>

**1) Clone the Repository:** <br>
-git clone https://github.com/RicardoVaca109/PicoandPlacaCalculator.git<br>
-cd PicoandPlacaCalculator<br>

**2) Create a virtual enviroment:** <br>
On the root project path in terminal put the next command<br>
*macOS and Linux:<br>
-python3 -m venv venv<br>
<br>
*Windows<br>
-python -m venv venv<br>
<br>
**3) Activate virtual enviroment:** <br>
On the root project path in terminal put the next command:<br>
*macOs:<br>
source venv/bin/activate<br>
<br>
*Linux:<br>
cd venv/bin/activate<br>
<br>
*Windows:<br>
(Command Prompt)<br>
cd venv/Scripts/activate <br>
or<br>
(Windows PowerShell)<br>
cd venv/Scripts/Activate.ps1<br>
   
**4) Install Dependencies:** <br>
Run the following commands on the root project folder outside venv folder  
  
*pip install -r requirements.txt  

These installs all the dependencies needed in order to run de project properly  
   
**5) Run the application:**  
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



