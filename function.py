from random import randint

def Rock_Paper_Scissors(move):
    m = ['камень', 'бумага', 'ножницы']
    move_bot = m[randint(0, 2)]
    #print(move_bot)
    if move == 'камень' or move == 'Камень':
        if move_bot == 'камень':
            return f'{move_bot}\nничья!'
        elif move_bot == 'бумага':
            return f'{move_bot}\nЯ победил)'
        elif move_bot == 'ножницы':
            return f'{move_bot}\nПоздравляю, ты выиграл!!'
    elif move == 'бумага' or move == 'Бумага':
        if move_bot == 'камень':
            return f'{move_bot}\nПоздравляю ты выиграл!'
        elif move_bot == 'бумага':
            return f'{move_bot}\nничья!'
        elif move_bot == 'ножницы':
            return f'{move_bot}\nя победил)'

    elif move == 'ножницы' or move == 'Ножницы':
        if move_bot == 'камень':
            return f'{move_bot}\nя победил)'
        elif move_bot == 'бумага':
            return f'{move_bot}\nпоздравляю, ты выиграл!'
        elif move_bot == 'ножницы':
            return f'{move_bot}\nничья!'
    else:
        return 'Я пока не знаю такой команды('

