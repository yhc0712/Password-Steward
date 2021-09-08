# Password Steward (PWS)

Password Steward is an application to generate simple or complex passwords to meet the standards that the website or software you're using requires and store them for further access.

## Table of Contents (optional)

1. How to Install

2. How to Use Password Steward

3. Description

## 1. How to install (Optional)

sth sth


## 2. How to use Password Steward

sth sth


## 3. Description

This application, Password Steward (PWS), was created as a final project of taking the python class (PYON345) in training programs provided by CSIE, National Taiwan University.

### Built using **Python 3.9.6**

#### Python Standard Libraries used
>check out [Python Standard Library](https://docs.python.org/3/library/)
*   **random**
*   **string**

#### Other Python Libraries used

* [**PyQt6**](https://www.qt.io/)

#### Custom Python Libraries

*   **validator** : a module that helps validate user input to check whether the input serves the purposes of the questions asked, functions defined as follows:

    1. ***val(question)*** : to determine whether a question is a yes/no question and whether the user's response meets the type of input variable requested by the question

        The function takes one parameter. *Question* is what the user reads before entering his/her response. The suffix of the *question* is used by this function to determine the type of answer it is looking for. Given the purpose of this project, if the suffix of the *question* is (Y/N), the function checks if the response is "y" or "n", regardless of its case. If not, the function checks if the response is a natural number.

        The function returns user's response if it is valid, after automatically changing all input strings to uppercase letters.

        For example:

        `val("How many sandwiches do you want?")` asks for a response of natural number. If a user enters "abc", the function rejects the answer and the user will be asked to enter another responese until it meets the requirement.

        `val("Do you need any napkins? (Y/N)")` if the user enters "y", the function returns `"Y"`.

    2. ***pw_len_check(length, combination)*** : to determine whether the count of requested types of characters exceed the digits of the password, if so, ask the user to modify his/her response.
    
        The function takes two parameters. *Length* is the digits of the password requested by the user. *Combination* is the number of types of characters (numbers, uppercase letters, lowercase letters, or symbols) the user needs.

        The function returns "again" if it detects an impossible combination, and `None` if a possible combination.

        For example:

        The user requested a three-digit password with all types of characters (numbers, uppercase letters, lowercase letters, and symbols, combination = 4) `pw_len_check(3, 4)`, making the application impossible to process because the models assign 1 count first to each of the type of characters if the user's response is "Y" to that kind of character.

    3. ***determinator(dictionary, length_needed_to_assign)*** : to determine the numbers of characters to be used by each type of characters requested by the user for the password combination

        The function takes two parameters. *Dictionary* is a dictionary with type of character, e.g. lowercase letters, as *key* and digits of characters to be used by that type of character in the password as *value*. `dictionary = {'num' : 3, 'lowercase letters' : 2}` *Length_needed_to_assign* is the remaining digits needed by the password after assigning 1 to each type of characters requested by the user.
        
        The function returns a dictionary, with summation of values equal to the digits the user needs for his/her password.

        For example:

        The user needs a 8-digit password with numbers, uppercase letters, and lowercase letters.
        `dictionary = {'numbers' : 1, 'uppercase' : 1, 'lowercase' : 1}`
        length_needed_to_assign = 8 - 3 = 5, 3 is the summation of the values in the dictionary
        `determinator(dictionary, 5)`

        Determinator returns `{'numbers' : 3, 'uppercase' : 2, 'lowercase' : 3}` results might vary given that this function utilizes randint from python's random library.

    4. ***generator(dictionary)*** : to generate a password according to the requests entered by the user, using random library and string library

        The function takes one parameter. *Dictionary* is a dictionary with types of characters, e.g. lowercase letters, as *key* and digits of characters to be used by that type of character in the password as *value*, where the summation of the values is the length of the password requested by the user.

        The function returns a string, the password generated.

### Graphic User Interface with naming of I/O

![Illustration of GUI](/resources/GUI_naming.png "GUI Naming")

The UI python file is named **PWS_Main.py** by Powershell command line `pyuic6 -o PWS_Main.py PWS_MainUI.ui`

The logic python file is named **PWS_Main_logic.py**

A noticeable problem currently encounters connecting logic file to ui file is that, while pyuic6 generates the py file for the ui, an AttributeError occurs in grid layout of radio buttons `AttributeError: type object 'Qt' has no attribute 'AlignHCenter'`. The original code generated by pyuic6 is `QtCore.Qt.AlignHCenter`. To solve the error, add *AlignmentFlag* after *Qt*, becoming `QtCore.Qt.AlignmentFlag.AlignHCenter`. Check [HERE](https://www.mfitzp.com/forum/t/attributeerror-type-object-qt-has-no-attribute-alignment/942)

Here is my concept layout when I first thought about a GUI for this application:
![Concept layout](/resources/GUI_layout_idea.png "sketch of my GUI version 0.1.0")






## Credits

reference tutorials/codes > links
collaborators/team members

* Python class taught by Chang Jie-Fan, starting from July 19th 2021, offered in [台灣大學資訊系統訓練班](https://train.csie.ntu.edu.tw/train/), introduced me to Python and guided me into the world of programming

* [Hillary Nyakundi's article on freecodecamp](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/) taught me how to write a README

* [Python GUI 程式設計 PyQt5 實戰 ISBN：9789864344741](https://www.books.com.tw/products/0010850077?sloc=main)

## Knowledge gained

Being a newbie in the field of programming, I have gained a lot from taking the python class offered by NTU CSIE and building this application. Here's the list:

- Python (beginner's level)

- PyQt 6.1.1

- Markdown

- Git for source control

- Github

- SQL

- Pandas

## License

Licensed under [GNU GPLv3](LICENSE).

    Copyright (C) 2021  CHEN YI-HSUAN

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>