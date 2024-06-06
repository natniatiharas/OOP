class Laptop:
    def __init__(self, brand, model, battery_capacity):
        self.brand = brand
        self.model = model
        self.battery_capacity = battery_capacity
        self.power = 0
    
    def charge(self, hours):
        if self.power < 100:
            self.power += hours * 60 * 1 
            if self.power > 100:
                self.power = 100
            print(f"{self.brand} {self.model} charging {self.power}%")
    
    def play_game(self, hours):
        power_consumption = hours * 60  
        if self.power >= power_consumption:
            self.power -= power_consumption
            print(f"{self.brand} {self.model} playing game for {hours} hour.")
            print(f"Current battery: {self.power}%")
        else:
            print(f"Battery is not capable to play game for {hours} hour.")
            print(f"Current battery: {self.power}%")

    def coding(self, duration):
        power_consumption = duration * 60/10 * 1  
        if self.power >= power_consumption:
            self.power -= power_consumption
            print(f"{self.brand} {self.model} coding for {duration} hour.")
            print(f"Current battery: {self.power}%")
        else:
            self.power = 0
            print(f"Battery is not capable to code for {duration} hour.")
            print(f"Current battery: {self.power}%")

    def browsing(self, duration):
        power_consumption = duration * 60/10 * 2
        if self.power >= power_consumption:
            self.power -= power_consumption
            print(f"{self.brand} {self.model} browsing for {duration} hour.")
            print(f"Current battery: {self.power}%")
        else:
            print(f"Battery is not capable to browse {duration} hour.")
            print(f"Current battery: {self.power}%")


    def play_audio(self, duration):
        power_consumption = duration * 60/10 * 5  
        if self.power >= power_consumption:
            self.power -= power_consumption
            print(f"{self.brand} {self.model} playing audio {duration} hour.")
            print(f"Current battery: {self.power}%")

        else:
            self.power = 0
            print(f"Battery is not capable to play audio {duration} hour.")
            print(f"Current battery: {self.power}%")



laptop = Laptop("HP", "Athlon", 20)

laptop.charge(2)  
laptop.play_game(1)  
laptop.browsing(1)  
laptop.charge(20/60)  
laptop.coding(2)  
laptop.play_audio(2)  
