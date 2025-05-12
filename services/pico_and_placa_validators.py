# Import neccesary Libraries
from datetime import datetime, time

# Function to validate if last digit of the plate matches the Pico y Placa restriction rules
def validate_plate_by_day(plate: str, day_of_week: str) -> bool:
    # Convert input date and extract weekday
    date_captured = datetime.strptime(day_of_week, "%Y-%m-%d").weekday()
    
    # Extract last digit of the input plate (assuming it's a number)
    last_plate_digit = int(plate[-1])
    
    # Pico and Placa last digit rules for days of the week  
    pico_placa_restrictions ={
        0 : [1, 2], # Monday
        1 : [3, 4], # Tuesday
        2 : [5, 6], # Wednesday
        3 : [7, 8], # Thursday
        4 : [9, 10], # Friday
    } 
    
    return date_captured in pico_placa_restrictions and \
        last_plate_digit in pico_placa_restrictions[date_captured]
     

def validate_weekday(date_to_string: str ) -> bool:
    # Convert input date and extract weekday
    date_captured = datetime.strptime(date_to_string, "%Y-%m-%d")
    
    # Extract weekday
    week_day = date_captured.weekday() 
    
    #Define Pico and Placa weekdays 
    allowed_days = range(0, 5)
    
    # Return Tru if week_day is in range of allowed_days
    return week_day in allowed_days

    
def validate_hour(time_to_string: str) -> bool:
    # Convert input hour 
    time_captured = datetime.strptime(time_to_string, "%H:%M").time()
    
    # Morning Schedule
    morning_start_schedule = time(6,0)
    morning_end_schedule = time(9,30)
    
    # Afternoon Schedule
    afternoon_start_schedule = time(16,0)
    afternoon_end_schedule = time(20,0)
    
    # Checks the schedules and return True or False depending of the condition
    if (morning_start_schedule <= time_captured <= morning_end_schedule or 
        afternoon_start_schedule <= time_captured <= afternoon_end_schedule
        ):
        return True
    return False