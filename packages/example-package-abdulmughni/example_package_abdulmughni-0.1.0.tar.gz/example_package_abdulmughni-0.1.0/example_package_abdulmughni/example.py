class Person:
    def __init__ (self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.seconds = 0
    def __str__(self):
        return f"Name:{self.name}\nAge: {self.age},\nGender: {'Male' if self.gender == 'M' else 'Female'}"
    def calculate_seconds(self):
        self.seconds = self.age * 365 * 24 * 3600


p = Person("Abdul", 15, 'M')

p.calculate_seconds()

print(p)
print(p.seconds)

        