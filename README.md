# Password Steward (PWS)

Password Steward is an application to generate simple or complex passwords to meet the standards required by the website or software you're using and store them for further access.

## Table of Contents (optional)

1. How to Install

2. How to Use Password Steward

3. Description

4. Credits

5. Knowledge Gained

6. License

## 1. How to install

Clone the repository from [github](https://github.com/yhc0712/Password-Steward)

Start the program by executing `PWS_Main_logic.py`

Or just click the `PWS.exe` to run the program.

## 2. How to use Password Steward

Caution: the database used to store uid and password information is unencrypted due to my lack of knowledge of cryptography. 

When you open the program for the first time, register an account so that your password. Password Steward requires a password for at least 4 digits. And you'd better not store your PWS's password in PWS.

When you login PWS for the first time, go ahead and press Generate New Password and follow the instructions on the screen. Press **Run** to generate a password and press **Copy** to copy the generated password to your clipboard.
    
>!!! Remember to press **Save** button on the right hand side so that you can look up the password in the future. !!!

If you want to look up your stored passwords, select **Lookup/Update** in the menu. There you can select your stored apps and select UIDs in case you have multiple UIDs for the same application. Press **Check** and your password stored in PWS then pops up in the *Password* line. Press **Update** to update the password, **Copy** to copy the password, and **Back** to return to the PWS menu.

## 3. Description

This application, Password Steward (PWS), was created as a final project of taking the python class (PYON345) in training programs provided by CSIE, National Taiwan University.

### Built using **Python 3.9.6**

#### Python Standard Libraries used
>check out [Python Standard Library](https://docs.python.org/3/library/)
*   **random**
*   **string**
*   **sys**
*   **math**

#### Other Python Libraries used

* [**PyQt6**](https://www.qt.io/)

* [**Sqlite3**](https://www.sqlite.org/index.html)

#### Custom Python Libraries

*   **validator** : a module that helps validate user input to check whether the input serves the purposes of the questions asked, functions defined as follows:

    1. ***val(question)*** : (used in building prototype) to determine whether a question is a yes/no question and whether the user's response meets the type of input variable requested by the question

        The function takes one parameter. *Question* is what the user reads before entering his/her response. The suffix of the *question* is used by this function to determine the type of answer it is looking for. Given the purpose of this project, if the suffix of the *question* is (Y/N), the function checks if the response is "y" or "n", regardless of its case. If not, the function checks if the response is a natural number.

        The function returns user's response if it is valid, after automatically changing all input strings to uppercase letters.

        For example:

        `val("How many sandwiches do you want?")` asks for a response of natural number. If a user enters "abc", the function rejects the answer and the user will be asked to enter another responese until it meets the requirement.

        `val("Do you need any napkins? (Y/N)")` if the user enters "y", the function returns `"Y"`.

    2. ***pw_len_check(length, combination)*** : (used in building prototype) to determine whether the count of requested types of characters exceed the digits of the password, if so, ask the user to modify his/her response.
    
        The function takes two parameters. *Length* is the digits of the password requested by the user. *Combination* is the number of types of characters (numbers, uppercase letters, lowercase letters, or symbols) the user needs.

        The function returns `"again"` if it detects an impossible combination, and `None` if a possible combination.

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

I currently encounters a noticeable problem when connecting logic file to ui file, that while pyuic6 generates the py file for the ui, an `AttributeError` occurs in grid layout of radio buttons `AttributeError: type object 'Qt' has no attribute 'AlignHCenter'`. The original code generated by pyuic6 is `QtCore.Qt.AlignHCenter`. To solve the error, add *AlignmentFlag* after *Qt*, becoming `QtCore.Qt.AlignmentFlag.AlignHCenter`. Check [HERE](https://www.mfitzp.com/forum/t/attributeerror-type-object-qt-has-no-attribute-alignment/942)

Here is my concept layout when I first thought about a GUI for this application:
![Concept layout](/resources/GUI_layout_idea.png "sketch of my GUI version 0.1.0")






## 4. Credits

* Python class taught by Chang Jie-Fan, starting from July 19th 2021, offered in [?????????????????????????????????](https://train.csie.ntu.edu.tw/train/), introduced me to Python and guided me into the world of programming

* [Hillary Nyakundi's article on freecodecamp](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/) taught me how to write a README

* [Python GUI ???????????? PyQt5 ?????? ISBN???9789864344741](https://www.books.com.tw/products/0010850077?sloc=main) as a reference book in Chinese about PyQt so that I can quickly use the things I need without learning the whole stuff. This book provides instructions based on PyQt5, thus I have devoted some time in porting from PyQt5 to PyQt6, which is what I used in my program.

* [Stack Overflow question 1](https://stackoverflow.com/questions/55432518/pyqt5-passing-a-name-form-login-to-main-window)

* [Stack Overflow question 2](https://stackoverflow.com/questions/11812000/login-dialog-pyqt)

* [How to use PyQt MessageBox by Fahmida Yesmin](https://linuxhint.com/use-pyqt-qmessagebox/)

* [Stack Overflow question 3](https://stackoverflow.com/questions/65735260/alternative-to-qmessagebox-yes-for-pyqt6)

* [Codecademy SQL Cheatsheet](https://www.codecademy.com/learn/learn-sql/modules/learn-sql-manipulation/cheatsheet)

* [Software icon](https://icon-icons.com/download/31761/ICO/512/)

* [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe/blob/master/README.md)

## 5. Knowledge gained

Being a newbie in the field of programming, I have gained a lot from taking the python class offered by NTU CSIE and building this application. Here's the list:

- Python (beginner's level)

- PyQt 6.1.1

- Sqlite3

- Markdown

- Git for source control

- Github

- SQL

- Microsoft Visual Studio Code

- Jupyter Notebook in VS Code, it annoyed me when I had to use jupyter notebook in a browser

## 6. License

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
