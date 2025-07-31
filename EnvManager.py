from PyQt6.QtCore import QSize
from  PyQt6.QtWidgets import QApplication, QButtonGroup, QMainWindow, QPushButton, QVBoxLayout, QWidget

import sys 
import os
import subprocess

windowXSize = 50
windowYSize = 50

categories = []
commands = []
buttons = []

def readVar(var, varName):
    if varName in line:
        return line[line.index("=")+1:]
    else:
        return var

with open(os.path.expanduser("~/.config/EnvManager/EnvManager.conf")) as config:
    bracketDepth = 0
    for line in config:
        if '#' in line:
            line = line[0:line.index('#')-1]
        line = line.strip()
        windowXSize = int(readVar(windowXSize, "windowXSize"))
        windowYSize = int(readVar(windowYSize, "windowYSize"))

        if bracketDepth > 0:
            if "[" in line:
                bracketDepth += 1
            if "]" in line:
                bracketDepth -= 1
            if "=[" in line:
                categories.append(line[:line.index('=')])
                commands.append([])
                if line.index('[') != len(line)-1:
                    if ']' in line:
                        commands[len(categories)-1].append(line[line.index('[') + 1 : line.index(']')])
                    else:
                        commands[len(categories)-1].append(line[line.index('[') + 1:])
            elif ']' in line and bracketDepth <= 1:
                if line.index(']') != 0:
                    commands[len(categories)-1].append(line[:line.index(']')])
            elif bracketDepth > 1:
                commands[len(categories)-1].append(line)

        if "[Categories]" in line:
            bracketDepth += 1
    
    for sectionIndex, section in enumerate(commands):
        for commandIndex, command in enumerate(section):
            newCommand = []
            quote = False
            lastArg = -1
            command = command.strip()
            for index, char in enumerate(command):
                if (char == "\"" or char == "'"):
                    quote = not quote
                if char == " " and quote == False :
                    newCommand.append(command[lastArg + 1:index])
                    lastArg = index
                if index == len(command)-1:
                    newCommand.append(command[lastArg + 1:index + 1])

            for argIndex, args in enumerate(newCommand):
                newCommand[argIndex] = args.replace("\"", "")
                newCommand[argIndex] = newCommand[argIndex].replace("'", "")

            commands[sectionIndex][commandIndex] = newCommand

    print(categories)
    print(commands)



class MainWindow(QMainWindow):
    buttonGroup = QButtonGroup()
    def __init__(self):
        super().__init__()
        
        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle("EnvManager")
        for index, source in enumerate(categories):
            buttons.append(QPushButton(source))
            self.buttonGroup.addButton(buttons[index], index)
            layout.addWidget(buttons[index])

        self.setFixedSize(QSize(windowXSize, windowYSize))
        
        self.buttonGroup.idClicked.connect(self.buttonVeryClicked)

        widget.setLayout(layout)

        self.setCentralWidget(widget)


    def buttonVeryClicked(self, button_id):
        self.hide()
        for command in commands[button_id]:
            subprocess.Popen(command)
        print("Clicked")
        self.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
