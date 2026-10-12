import random

def checkdigit(CardNum):
    digits = CardNum.replace(" ","").replace("-","")
    if not digits.isdigit():
        return "Invalid Input"
    payload = digits[:-1]
    newdigits = payload[::-1]
    total=0
    for index,num in enumerate(newdigits):
        digit = int(num)
        if index % 2 ==0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return (10 - total % 10 ) % 10

def validity(CardNum):
    return int(CardNum[-1]) == checkdigit(CardNum)

def generatecard():
    Card="4"
    for i in range(14):
        Card += str(random.randint(1,9))
    RealCard = Card + str(checkdigit(Card + "1"))
    return RealCard[0:4]+"-"+RealCard[4:8]+"-"+RealCard[8:12]+"-"+RealCard[12:]

options1 = ["gen", "make", "create"]
options2 = ["val", "check", "test"]

intent = input("What would you like to do? Create or check a string? :").strip().lower()
if any(word in intent for word in options1):
    print(generatecard())
elif any(word in intent for word in options2):
    CardNum = input("Enter the card number : ")
    print(validity(CardNum))
else:    
    print("Invalid intent")