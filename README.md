+ the script TRIES to `save` & `close` (& `remember`) all `MS-WORD` and `MS-EXCEL` documents being used at the computer
+ closes and `remembers` `MS-EXPLORER` windows.
+ Session data (list of files) is stored in a txt file in the Same directory.
+ if you would like to `save` & `close` and nothing else, you can simply run `saver.ps1` (powershell script)
+ the python script contains the saving (`remember`) logic and the UI.
+ Anomalies: In some cases files may not be saved, users will most likely be prompted to save them. (See Usage Section & Disclaimer for more info)

#### dependencies to install
+ `winget install python`
+ `pip install pywin32`

#### Running the python script to use the program
+ `python c:\path\to\session.manager.py`


#### Find the location of pythonw/python (optional)
+ `where pythonw`
#### Create Shortcut on Windows (optional)
`"c:\path\to\pythonw" "c:\path\to\session.manager.py"`

#### usage:-
+ The saved(?) & closed files in the session can be `RE-OPENED` automatically by selecting the saved session from the list and then `RESTORE SESSION`.
+ the script writes some txt files session_list_xxxx-xx-xx_xx-xx.txt in the same directory as the script. it is better to store the scripts in a separate directory to avoid over writing of similar name files
+ The script does not use KILL mechanism to close OFFICE, rather it uses COM protocol.
+ Disclaimer: Software is provided AS IS and WITHOUT WARRANTY or LIABILITY for the Authors (without even any implied warranty of merchantibility or usability)

```
      |V|
   .::| |::.
  ::__| |__::
 >____   ____<
  ::  | |  ::
   '::| |::'
      | |
      | |
jgs   |A|
```
------
##### <b>Religious / Spiritual Affirmation / Chant /Incantation: I am a Christian AND (I REMAIN)</b> (C) PUNEET BAPNA. He that needs to GO LET HIM DO SO.
