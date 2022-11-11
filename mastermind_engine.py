import random

NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
_my_number = []

def zagadka_chislo():
    global _my_number
    _my_number.append(random.sample(NUM, 4))


def proverka_chisla(number):
    bulls, cows = 0, 0
    gift = ''
    for i in number:
        if i.isdigit() is not True or len(number) != 4:
            return ValueError("Ход - четырехзначное число")
    set_number = set(number)
    if len(number) != len(set_number):
        return "Цифры не должны повторяться!"
    else:
        for num in enumerate(_my_number[0]):
            for num_user in enumerate(list(number)):
                if num[0] == num_user[0] and num[1] == num_user[1]:
                    bulls += 1
                elif num[1] == num_user[1]:
                    cows += 1

    if bulls == 3:
        gift = 'Сильный ход!'
    elif cows > 1 and bulls > 1 or bulls > 2:
        gift = 'Очень сильный ход!'
    elif 2 < cows < 5 or bulls == 1:
        gift = 'Хороший ход!'
    return f"Быков: {bulls}, Коров: {cows}\n{gift}"
