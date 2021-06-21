import string, random

oneChar = random.choice(string.ascii_lowercase)
numbers = random.randrange(1,99999)
jsonname = oneChar + str(numbers)
print(jsonname)
