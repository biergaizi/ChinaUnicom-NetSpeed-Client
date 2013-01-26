ChinaUnicom-NetSpeed-Client
===========================

A cross-platform and open source replacement of China Unicom Net Speed Client.

Versions
--------------------------
This project has two version of programs. One is for GUI users, another one  is for CLI users.

1. `main_gui.py` -- GUI version
2. `main_cli.py` -- CLI version

GUI version needs Python 3 and PyQt 4 runtime. CLI version can run under both Python2 and Python 3.

Dependencies
-------------------------
### GUI ###
1. Python 3
2. PyQt 4
3. Beautiful Soup 4

### CLI ###
1. Python 2.7 or Python 3
2. Beautiful Soup 4

Usage
--------------------------
### GUI ###
GUI version is very user-friendly, it doesn't need any manual. But it doesn't have any English translation， you can help me to do it, thanks a lot.

### CLI ###

1. `./main_cli.py info` will show the information about your net speed.
2. `./main_cli.py up` will speed up your connection.
3. `./main_cli.py down` will slow down your connection.


中国联通带宽客户端
===========================
在某些情况下，只有使用联通沃宽客户端才可获得较高网速，但此客户端不跨平台。本程序是其跨平台的替代品。

版本
---------------------------
本程序分两个版本，一个是图形界面版本，另一个是命令行版本。

1. `main_gui.py` -- 图形界面版本
2. `main_cli.py` -- 命令行版本

图形界面版本使用 PyQt 编写，仅支持 Python 3；命令行版本同时支持 Python 2.7 和 Python 3。

依赖关系
---------------------------
### 图形版本 ###
1. Python 3
2. PyQt 4
3. Beautiful Soup 4

### 命令行版本 ###
1. Python 2.7 或 Python 3
2. Beautiful Soup 4

用法
---------------------------
### 图形版本 ###
图形版本的界面足够友好，不需要任何手册与说明。但是它缺失英文翻译，欢迎帮助我进行翻译工具，非常感谢。

### 命令行版本 ###

1. `./main_cli.py info` 将显示网速信息。
2. `./main_cli.py up` 将会提速带宽。
3. `./main_cli.py down` 将会恢复原始带宽。
