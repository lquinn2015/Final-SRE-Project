import sys, signal
import pyautogui as pag
import subprocess as sp
import time
import regex

def main():
    # Clean up last runs
    #cmd = 'del data.dmp'
    #sp.run(cmd)

    def clickBox(x,y, rightClick=None):
        if rightClick is None:
            pag.click(start_pos[0] + square[0] * x, start_pos[1] + square[1] * y, _pause=0)
        else:
            pag.click(start_pos[0] + square[0] * x, start_pos[1] + square[1] * y, _pause=0, button='right')

    cmd = 'minesam.exe'
    app = sp.Popen([cmd, '&'])

    time.sleep(1) # load the game

    start_pos = (125,230)
    #start_pos = (0,228)
    square = (20,20)

    pag.click(start_pos[0], start_pos[1], _pause=0)

    time.sleep(1)
    print("Go")

    cmd = 'procdump.exe -ma minesam.exe data'
    sp.run(cmd)

    data = open('data.dmp','rb').read()


    game_settings = ('\x63', '\x1e',  '\x18')  # 99 mines, 30 width, 24 height you need to set this up before hand
    mark = b'\x63' + b'\x00' * 3 + b'\x1e' + b'\x00' * 3 + b'\x18' + b'\x00' * 7 + b'\x10' * 33  # unique board identifier
    src = regex.search(mark, data)

    data = data[src.span()[0]: src.span()[1] + 48*16]  # reads out the game board into a normal array


    """
    How to attact with a debugger to write to memory 
    
    
    """

    board = [] * 30
    x = 0
    y = 0
    c = 0

    data = data[49:] # skip the noise

    for i in range(len(data)): # play the game quick
        nib = data[i]
        if nib == 16:  # new line
            c = c + 1
            if c == 2:
                #print(board[y])
                y = y + 1
                c = 0
                x = -1
        elif nib == 143: # mine block
            #board[y].append("*")
            clickBox(x,y,1)
        elif nib == 15:
            #board[y].append(" ")
            clickBox(x,y)
        x = x + 1

    time.sleep(100)

    app.send_signal(signal.SIGTERM)

if __name__ == '__main__':
    main()