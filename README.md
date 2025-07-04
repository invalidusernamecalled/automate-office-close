+ the script TRIES to `Save & close` all `MS-WORD` and `MS-EXCEL` documents open at the computer
+ close `MS-EXPLORER` windows.
+ Session data (list of files) is stored in a txt file.
+ The saved(?) & closed files in the session can be `RE-OPENED` automatically by selecting the saved session from the list and then `RESTORE SESSION`.
+ Anomalies: In some cases files may not be saved, users most likely be prompted to save them. (See Usage Section for more info)
+ SOFTWARE IS PROVIDED AS IS WITHOUT WARRANTY or LIABILITY for the AUTHORS (without even any implied warranty of merchantibility or usability)

#### dependencies to install
+ `winget install python`
+ `pip install pywin32`

#### Running the python script <----- to use the program
+ `python c:\path\to\session.manager.py`


#### Find the location of pythonw/python (optional)
+ `where pythonw`
#### Create Shortcut on Windows (optional)
`"c:\path\to\pythonw" "c:\path\to\session.manager.py"`

#### usage:-
+ the script writes some txt files session_list_xxxx-xx-xx_xx-xx.txt in the same directory as the script. it is better to store the scripts in a separate directory to avoid over writing of similar name files
+ The script does not use KILL mechanism to close OFFICE, rather it uses COM protocol.
