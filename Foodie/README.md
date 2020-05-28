Introduction:
=============
FoodieBot - a restaurant search bot engages conversation with users. Based on the location, cuisinie and specific budget slots that user chooses, the bot presents Top 5 results on the chat window. If user wishes, Top 10 results will be emailed to the user.

A detailed demonstration of Bot working on Slack can be found on youtube at: https://youtu.be/pk8dYb_sg-U

The chat bot is built on RASA NLU and CORE architecture, running on Python 3.6.0 version. The setup instructions are below. 

Detailed Setup Instructions:
============================
1. Download the RASA_BASE zip file submitted on the portal and Unzip the  RASA_BASE zip file.
2. Open terminal and navigate into the folder of RASA_BASE
3. Execute the command on the terminal -   "conda create -n rasa -y python=3.6"
        This command creates a virtual environment called ‘rasa’ with python 3.6. Execution time - 1 - 1.5 mins.    [*** See the Special-Instructions -1 below ****]
4. After the successful execution of above command, execute - "source activate rasa"
        This command will activate the new python virtual environment called 'rasa'. You can see the python environment name ‘rasa’ in the bash interpreter command line.
5. Now execute the command - "make setupbot"
        This command will install all the packages , associated dependencies into the newly create virtual environment.  It can take unto 3 - 5 mins depending on the internet speed.
6. Now execute the command - "make checkbot"
        This command simply displays the versions of RASA components. The versions displayed must match the following - 
        **** Rasa NLU Version:  0.15.0
        **** Rasa Core Version: 0.14.0
        **** Rasa SDK Version:  0.14.0
7. Now execute the command "make runbot"
    This command will start the chat bot in command line interface mode. 

Special-Instructions:
====================
1. It is assumed, that the python environments on the user system are under 'Anaconda' and hence 'Conda' is used to create new virtual environment. If base python is not under 'anaconda', then please use equivalent 'virtualenv' commands.

Changes being done for Future Release:
======================================
1) Ease the budget slots, location restrictions and allow greater freedom around budgetting to user.
2) Host the RASA action server on EC2 (cloud) for greater reach.
3) Add 'Cuisine Dish' level selection.
4) Changes around more engaging conversations 