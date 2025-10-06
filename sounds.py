from playsound import playsound

def play_broken_sequence():
    playsound('Звук поломки двигателя или аппарата для театра.mp3')

if __name__ == '__main__':
    for i in range(10):
        play_broken_sequence()
        print(i)