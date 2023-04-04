# -*- coding: utf-8 -*-

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


__VERSION__ = "0.23.2"
__DESC__ = "Utility for outdated packages automatic detection"
__AUTHOR__ = "ksot1k"
__URL__ = "https://github.com/ksotik/upddetect"
__LOGO__ = """
                                                            ___                           ___     
              ,-.----.        ,---,      ,---,            ,--.'|_                       ,--.'|_   
         ,--, \    /  \     ,---.'|    ,---.'|            |  | :,'                      |  | :,'  
       ,'_ /| |   :    |    |   | :    |   | :            :  : ' :                      :  : ' :  
  .--. |  | : |   | .\ :    |   | |    |   | |   ,---.  .;__,'  /     ,---.     ,---. .;__,'  /   
,'_ /| :  . | .   : |: |  ,--.__| |  ,--.__| |  /     \ |  |   |     /     \   /     \|  |   |    
|  ' | |  . . |   |  \ : /   ,'   | /   ,'   | /    /  |:__,'| :    /    /  | /    / ':__,'| :    
|  | ' |  | | |   : .  |.   '  /  |.   '  /  |.    ' / |  '  : |__ .    ' / |.    ' /   '  : |__  
:  | : ;  ; | :     |`-''   ; |:  |'   ; |:  |'   ;   /|  |  | '.'|'   ;   /|'   ; :__  |  | '.'| 
'  :  `--'   \:   : :   |   | '/  '|   | '/  ''   |  / |  ;  :    ;'   |  / |'   | '.'| ;  :    ; 
:  ,      .-./|   | :   |   :    :||   :    :||   :    |  |  ,   / |   :    ||   :    : |  ,   /  
 `--`----'    `---'.|    \   \  /   \   \  /   \   \  /    ---`-'   \   \  /  \   \  /   ---`-'   
                `---`     `----'     `----'     `----'               `----'    `----'             
"""

__HELP__ = BColors.BOLD + "usage: upddetect [options]" + BColors.ENDC + """
Options:
-s: detect only security updates
-d: detect only dist updates
-a: detect all updates
-j: work silently, display json when finished
-v: show version"""
