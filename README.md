+ the script TRIES to `save` & `close` (& `remember`) all `MS-WORD` and `MS-EXCEL` documents being used at the computer
+ closes and `remembers` `MS-EXPLORER` windows.
+ Session data (list of files) is stored in a txt file in the Same directory.
+ if you would like to `save` & `close` and nothing else, you can simply run `saver.ps1` (powershell script)
+ the python script contains the saving (`remember`) logic and the UI.
+ Anomaly: In some cases files may not be saved before closing but users most likely will be prompted (by Word/Excel) to save them. (See Usage Section & Disclaimer for more info)

`Disclaimer: This software is provided "as is", without any warranty or liability. There is no guarantee of merchantability or fitness for a particular purpose, express or implied. Use at your own risk.`

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
+ Download both scripts in a separate directory, install the dependencies. Run from command prompt `python session.manager.py` or Create Shortcut.
+ The closed files of a particular session can be `RE-OPENED` automatically by selecting the relevant saved session from the list and then clicking `RESTORE SESSION`.
+ the script writes txt files session_list_xxxx-xx-xx_xx-xx.txt in the same directory as the script.
+ keep the scripts in its separate directory due to the risk of over writing
+ the script does not KILL the MS-OFFICE APPS, rather it tries to close them gracefully using COM objects.

#### what each script does:-
+ `saver.ps1---->Tries to get a list of open windows, saves and closes open Word/Excel files using COM objects`
+ `saver.ps1---->Saves the list to session_list_xxxx-xx-xx_xx-xx.txt in the format yyyy-MM-dd_HH-mm and marks it as hidden`
+ `session.manager.py----> Saves/Restores/Displays List of Sessions. Performs actions based on User interactions like executing scripts to save and close windows, etc.`

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
Religious / Spiritual Affirmation / Chant /Incantation:
I am a Christian
AND (I REMAIN)</b> (C) PUNEET BAPNA.
He that needs to GO LET HIM DO SO.
```
------
