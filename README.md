# Minesweeper

### Solving the blocking of keyboard problem
- Try using pynput.keyboard
    - pynput doesnt block terminal window
- Block all terminal input
    - Create a option to use terminal input instead of keyboard
    - Asks for the option at first run of the game and then saves the config to a file
    - If the game is run a second time after the option has been chosen, use previous option
    - Create a options menu to change the input type
- If 'esc' is pressed the terminal window is cleared. Therefore you could press esc before any input, using: keyboard.press_and_release('esc')

*Solution:*
Either make the user or programmatically press the escape key before any terminal input

I would still like to create a option to only use text to play the game