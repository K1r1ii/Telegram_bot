from random import randint

def Rock_Paper_Scissors(move):
    m = ['rock', 'paper', 'scissors']
    move_bot = m[randint(0, 2)]
    #print(move_bot)
    if move == 'rock':
        if move_bot == 'rock':
            return f'{move_bot}\ndraw'
        elif move_bot == 'paper':
            return f'{move_bot}\nbot win!'
        elif move_bot == 'scissors':
            return f'{move_bot}\nuser win!'
    elif move == 'paper':
        if move_bot == 'rock':
            return f'{move_bot}\nuser win!'
        elif move_bot == 'paper':
            return f'{move_bot}\ndraw'
        elif move_bot == 'scissors':
            return f'{move_bot}\nbot win!'

    elif move == 'scissors':
        if move_bot == 'rock':
            return 'bot win'
        elif move_bot == 'paper':
            return 'user win!'
        elif move_bot == 'scissors':
            return 'draw'
