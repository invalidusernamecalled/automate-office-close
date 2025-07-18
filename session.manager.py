import tempfile
import base64
from io import BytesIO
import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import win32event
import win32api
import winerror
import sys

mutex_name = "Global\\0yET524bK1Ez0yET0yET524bK1Ez524bK1Ez"  # Unique name across the system
mutex = win32event.CreateMutex(None, False, mutex_name)

# Check if mutex already exists
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    print("Another instance is already running.")
    sys.exit(0)

def fix_ppm_for_tkinter(ppm_data: bytes) -> bytes:
    marker = b'\n255\n'
    header_end = ppm_data.find(marker)
    if header_end == -1:
        raise ValueError("Invalid PPM header (missing '255')")
    return ppm_data[:header_end + len(marker)] + ppm_data[header_end + len(marker):]

def photoimage_from_base64_ppm(base64_str: str) -> tk.PhotoImage:
    ppm_data = base64.b64decode(base64_str)
    fixed_data = fix_ppm_for_tkinter(ppm_data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ppm") as temp:
        temp.write(fixed_data)
        temp.flush()
        return tk.PhotoImage(file=temp.name)

save_icon_base64 = '''
UDYKMzIgMzIKMjU1Cjqc1zil2DGRvi+KtOzy9fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+Z7H2S+KtDSWxDql2Diq1AAAAAAAAAAAAAAAAAAAAAAAAAAAADmk2Tql2TKRvzCKte3y9fr6+p3G2kaWvEaWvEaWvNjn7vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+p7H2jCKtTSWxTql2Tml2Dmm2QAAAAAAAAAAAAAAAAAAAAAAADmk2Tql2TKRvzCKte3y9fr6+pHA1jCKtTCKtTCKtdTk7fr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+p7H2jCKtTSWxTql2Tql2Tml2Dqn2QAAAAAAAAAAAAAAAAAAADmk2Dql2TKRvzCKte3y9fr6+pHA1jCKtTCKtTCKtdTk7fr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+p7H2jCKtTSWxTql2Tql2Tql2Tqk2Tml2AAAAAAAAAAAAAAAADmk2Dql2TKRvzCKte3y9fr6+pHA1jCKtTCKtTCKtdTk7fr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+p7H2jCKtTSWxTql2Tql2Tql2Tql2Tml2TWf1AAAAAAAAAAAADmk2Dql2TKRvzCKte3y9fr6+pHA1jCKtTCKtTCKtdTk7fr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+p7H2jCKtTSWxTql2Tql2Tql2Tql2Tql2Tmk2D9/vwAAAAAAADmk2Dql2TKRvzCKte3y9fr6+pHA1jCKtTCKtTCKtdTk7fr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vj595jI0DCOrTWavTqnzzqnzzqnzzqnzzql1jql2Tik2AAAAAAAADmk2Dql2TKRvzCKtdvo7/r6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+nzgdkDUN0DUN0DUN0DUN0DUN0DUN0DUNz7JXDql2Tmk2AAAAAAAADmk2Dql2TKRvzCKtVSewaTK3KjM3qjM3qjM3qjM3qjM3qjM3qjM3qjM3qjM3qjM3qjM3qjM3qjM3lPSVkDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tqk2QAAAAAAADmk2Dql2TOSwDCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTCKtTzGTkDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tig0jKRvjKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvDKPvD3HUEDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2Tql2T7LVUDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2Uaq25PN6pzR65zR65zR65zR65zR65zR65zR65zR65zR65zR65zR65zR65zR65zR65zR61HTWEDUN0DUN0DUN0DUN0DUN0DUN0DUNz/PRjql2Tql2QAAAAAAADmk2Dql2bLc8P///////////////////////////////////////////+767mDYWF3aVl3aVl3aVkXVPEDUN0DUN0DUN0DUN0DUN0DUN0DUNz/TOT/NTT/NTT7TNj/ONjmk2Dql2cfl9P////7+/vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+oLZfT/TNkDUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUNz/RNjzFNjmk2Dql2cfl9P////n5+d/f39/f39/f39/f39/f39/f39/f39/f39/f39/f39fe1lTQTUDUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUNz/TNj3HNQAAADmk2Dql2cfl9P///////////////////////////////////////////////////9DwzkHQOEDUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUNz7HSTO7MwAAADmk2Dql2cfl9P////39/fT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09JDZjD/TNkDUN0DUN0DUN0DUN0DUN0DUN0DUN0DUN0DUNz/PNzusrwAAAAAAADmk2Dql2cfl9P////r6+ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5uLm4mHSWkDUN0DUN0DUN0DUN0DUN0DUN0DUN0DUNz/TNjy3fjql2QAAAAAAADmk2Dql2cfl9P///////////////////////////////////////////////////////////9713UXQPUDUN0DUN0DUN0DUN0DUN0DUN0DUN13TWDql1Dql2QAAAAAAADmk2Dql2cfl9P////z8/O3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7Z7Ymj/SNkDUN0DUN0DUN0DUN0DUN0TQO9fy2Dql2Tql2QAAAAAAADmk2Dql2cfl9P////z8/O3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7e3t7ezt7HHWaz/TNkDUN0DUN0DUNz/SNqTkoPv9/jql2Tql2QAAAAAAADmk2Dql2cfl9P///////////////////////////////////////////////////////////////////+r46kzQREDUN0DUNz/TN2zWZf3+/Pv9/jql2Tqk2AAAAAAAADmj1jql2bOfXuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLuOdLqumKT/RNkDUN0fKNMyeKeOdLuCdMTql2Tmk1wAAAAAAADmdzTmj1myenYCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchoCchki5ZD/PNliteICchoCchn+chzmk1zmczgAAAAAAADqcxDiYxjiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDiZyDicvDuwcziZyDiZyDiZyDiZyDiZxjWUyQAAAAAAAA==
'''
restore_icon_base64 = '''
UDYKMzIgMzIKMjU1CgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANBgArFABAHQBJIgBJIgBAHQAsFAANBgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAwJBHQR3NgaUQh2eUziqaEWvckWvcjiqaB2eUwaUQgR3NgJBHQAIAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAARAHAmLPSmjWGzAi6HXtbTfw7Xfw7Xfw7Xfw7Xfw7Tfw6HXtWzAiymjWAmLPQRAHAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEOBgtzMSCfTXPDjqTYtKXYtKXYtKXYtKbYtKbZtKbZtKbYtKXYtKXYtKXYtKTYtHPDjiCfTQtzMQEOBgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIWCRGHNzqqXI3On5bSppfSpZjTpYnMm2m/iGa9h2a9h2q/iIvNnJnTpZjTpZjTpZfSpZbSpo3OnzqqXBGHNwIXCQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIPBRWJNkCtXIfLl4rMmIvNl23Ah4XKobrhzPH59f////////D49Lfgy4PJn3DBh43Ol4zOl4vNl4rNmIfLl0CtXBWJNgIPBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAABABZ4LjSoTXvGiX/Iin3HiHTDkN7x5/////////////7+/uf059Xt1NPs0+Ly4tbt4HLDjYHJiILJiYHJin/IinvGiTSoTRZ4LgABAAAAAAAAAAAAAAAAAAAAAAAAAA5FGSaiPWi+dXXEfnXEfIXKnfv9/P////////3+/cfnxI7OiYHJe4HJe4HJe4DIe4fLg7Tfs3rGkXrGfHrGfXjFfXbEfmm+dSaiPQ5FGQAAAAAAAAAAAAAAAAAAAAIIAyWXNUewUm3AcnDBcnvGjvz9/f////////b79ZvUkXzGbnzHbn3Hbn3HbnzHbnzGbnvGb3rGb4jMgHnFenXDcHLDcXDCcm3AckewUiWXNQIIAwAAAAAAAAAAAAAAABNIGC+mOF66YWm+Z2a9aub07P////////3+/JjTiXjFY3nFYnrGYnrGYnrGYnrGYnnFYnjFY3fEY3XEZHPDZGi+Zm7BfGzAZmm/Z166YS+mOBNIGAAAAAAAAAAAAAAAACiGLD2sPGK8XWa9XJzUof///////////8Plt3XEWHfEWHjFV3nFV3nGV3nGV3nFV3jFV3fEWHXEWHTDWHDCWaLXrd7x5WG7X2a9XGO8XT2sPCiGLAAAAAAAAAAAAAUPBDipNUmxQGG7U2S8Utft3P////////7+/YTKYnXETXfFTXjFTXnGTHnGTHnGTHnGTHjFTXfFTXXETXPDTnTDcPv9/P///6PXr2O8UmG7U0mxQDipNQUPBAAAAAAAABIzDz+tM1C0PmC7Sma9Ufz+/f///////+Xz3HXERHfERHnFQ3rGQ3vGQ3vGQ3vGQ3vGQ3rGQ3nFQ3fERGu/SNbt3f////////z9/G7AcGC7SlC0Pj+tMxIzDwAAAAAAAB1MFkavMUSvPkGtSmC7Zf///////////8PlwU6zRk+0RnTDPX3HOn7IOn/IOn/IOn7IOn3HOnzHOnnFO53Vn////////////////9ju4Fq4R1S1OUawMR1MFgAAAAAAACRYGE2yL4zNdP////////////////////////////L56ojMQIHJMoLJMoPKMoPKMoLJMoHJMoDIM3jFWvj8+v///////////////////5rUole3NE2yLyRYGAAAAAAAACdZF1O1Llq4Ls3pvf///////////////////////6rabYXKK4bLK4jMK4jMKojMKojMK4fLK33HMNDr1v////////////////////////r8+2W9WFO1LidZFwAAAAAAACVPE1m4LF+6KnfEQfT68P///////////////9bttYjMJovNJY3OJI7OJI/PJI/PJI7OJI3OJJLQMqraYqjZY93wyv///////////6nagJPRZ3rGTVm4LCVPEwAAAAAAABs3DV+6Kma9KWzAKKfZd/////////////X77ZXSNI/PIZHQIJTRIJXSH5bSH5bSH5XSH5TRIJHQII/PIYvNItjuzv///////////37IOWzAJ2a9KF+6Khs3DQAAAAAAAAgRA2W8KWzAJ3LCJXnFJNrvwP///////7bgbpLQHpbSHZnTHJvUG53VG53VG53VG53VG5vUG5nTHJbSHYjMLvf7+f///////+7443nFJHLCJWzAJ2W8KQkRAwAAAAAAAAAAAFaaIHHCJXjFJH7IIpPQOvj8897xu5XRHJnTG53VGqHWGaPXGKXYGKbZF6bZF6XYGKPXGKHWGZ3VGafZh////////////8fnm3/IInjFJHHCJVaaHwAAAAAAAAAAAAAAADFVEHbEJH7HIoTKIIvNHrnhb6LXNJvUGqHXGKXYF6naFqzbFq7cFa/cFa/cFa7cFazbFqnaForNPO738v////////v995jTOYXKIH7HInfEJDFVEAAAAAAAAAAAAAAAAAYKAXO4IIPKIYrNH5HQHZfSG53VGp3VM4zOJq3cFbHdFLTfE7bgE7fgErfgErbgE7TfE4jMNtXt3P///////////8fmhJHQHYrNH4PKIXO4IAYKAgAAAAAAAAAAAAAAAAAAADhWDojMH4/PHZbSHJ7VHKXYGqvbGbDdeoDIWZzUHL3iFMDjE8HkE8DjE5TRH4rNb+Pz6v///////////93wqZ/VHZfSHI/PHYjMHzhXDgAAAAAAAAAAAAAAAAAAAAAAAAECAGucF5TRHJvUG6bZIa3cH7PeHbnhHN3whcbm0ZjToJLQgpPQhZzUqdju4v////////////3++9nvjq3cIKbZIZzUG5TRHGucFwECAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4UAoW5GJ/WGazbI7XfKLziJsLlJcjnI9TsQ+73q/z+8/////////////////z+9ev2sM3pSrziJrXfKKzbI6DWGYa5GA4UAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABcfA5C9FazbGLviLsXmNMvoMtHrMdbtL9rvLt7xMeb0Vur1bun1buLyWdfuNNHrMcvoMsXmNLziLqzbGJC+FRcfAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAVAoWnELfgFMbmLdPsQ9nuQ97xQePzQOf0P+n1Pun1Puf1P+PzQN/xQdnuQ9PsQ8fmLbjgFIWoEBAVAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAICAFBhB7TUDszpFtnuL+PzRuv2Ve/4VfH5VPL5VO/4Vev2VePzRtnuL8zpFrXUDlBhBwICAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoMAFpmBay/CN3wCOb0CO/4EvX6F/X6F+/4Euf0CN3wCKy/CFpmBQoMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUWAEVJAWlsAXx+AH1+AGltAUZJARUWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
'''
delete_icon_base64 = '''
UDYKMzIgMzIKMjU1CgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPZCNfRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvZCNQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRCNfRBNPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRBNPRCNfRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRBNPVWSvduZPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfRGOvdxZ/VNQfRCNfRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRBNPVUSPvCvv7s6/iCefRCNfRDNvRDNvRDNvRDNvRDNvRCNfREN/mVjf7z8vquqfRLP/RCNfRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRCNfVWSvvBvf////////7t6/iCefRCNfRDNvRDNvRDNvRCNfREN/mUjf729f/////8/PqvqfVNQfRCNfRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRBNPd6cf708/////////////7t6/iCefRCNfRDNvRCNfREN/mUjf729f////////////7n5fZlWvRBNPRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRGOfmUjf729f////////////7t6/iCefRBNPREN/mUjf729f////////////7r6vd9c/RDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf729f////////////7s6/iEe/mUjP729f////////////7r6vd8c/RBNPRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf729f////////////7z8v729v////////////7r6vd8c/RBNPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf729f////////////////////////7r6vd8c/RBNPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfREN/mWjv/6+v////////////////7x8Pd9dPRBNPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfREN/mWj//6+v////////////////7y8fiCefRCNPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf729f////////////////////////7t6/iCefRCNfRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf729f////////////7y8f729v////////////7t6/iCefRCNfRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf729f////////////7r6fd+dvmUjP729f////////////7t6/iCefRCNfRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRGOfmVjf729f////////////7r6vd8c/RBNPREN/mUjf729f////////////7t6/iCefRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRBNPd0av7y8f////////////7r6vd8c/RBNPRDNvRCNfREN/mUjf729f////////////7o5/ZpX/RBNPRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRCNfVQRPuzrv/9/f////7r6vd8c/RBNPRDNvRDNvRDNvRCNfREN/mUjf729f/////8/Pqtp/VNQfRCNfRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRCNPVNQfuzrv7p5/d8c/RBNPRDNvRDNvRDNvRDNvRDNvRCNfREN/mUjf7z8vqsp/RLPvRCNfRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRCNPVQQ/ZmXPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRCNfRGOvdxZ/VNQfRCNfRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRCNfRBNPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRBNPRCNfRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPVDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvZDNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPRDNvRDNvRDNvRDNvRDNvRDNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
'''
info_icon_base64 = '''
UDYKNjQgNjQKMjU1CgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqD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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBmCpyWKrYTH2Mz2+c72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+c32+YnK2ieLrhmCpxqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmCqCSJrITH2M32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+YnK2iSKrRmCqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqB2FqXi/0sz2+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+c/4+s/4+s72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+X7D1R2FqhqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBmCp1ytxsby9s72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+cTw9aXc56Tc58Tw9c73+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+cfy9mCwyBmCpxqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBiCpzuYt7bn78/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+b7s8lmrxSKIrCKIq1eqxL7s8s73+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+rfo7z2ZuBiCpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqCCHq43N3M/4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+ovL2xqDqBmDqBmDqBmCqH/E1s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+pDP3iCHqxmDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp1Gmwcfy9s72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+n3D1RiCpxqDqBqDqBaBpme1y8/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+cfy9lapwxiCpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmDqCOJrJrW4s/4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+p/Y5CaLrReBphaBpiWKrZrV4s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+p7Y5COJrBmDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp0yjv8fy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cv1+I7O3U2jv0yjv4vL28v1+M32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9lGmwRiBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBuEqIXI2dD4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+snz98nz9873+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+ozM3BuEqRqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmCpzKSs7Xn7s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+rXm7jGSshmCpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp1Oowsr0+M32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cv0+FirxBeBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmCp3e+0s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+sr0+Mr0+M73+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+oPG1xmDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqB+GqpzX49D4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+q/j7FmrxVeqxKvg6s73+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+pzX4x+GqhqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBmCqCmMr63i68/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cr0+FqsxRWAphWAplapw8r0+M32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+q3h6yiMrhmCqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAABqEqBqDqBqDqBiCpzuYt7/t8873+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kWfvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+b/t8zuYtxiCpxqDqBqDqBuCqQAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cby9kafvBeBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp0afvMby9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cby9kafvBeBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBiCpzyZt8Dt8873+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+cDt8zuYtxiCpxqDqBqDqByCqAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBmCqCmNr67i68/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+q3i6ymMrxmCqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqB+GqpzX49D4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+pzX4x+GqhqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmCp3i/0s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+oPG2BmDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp1Wpw8v1+M32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cv1+FmsxReBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBiCpzOTs7fo7873+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+rbn7zKTsxiCpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBuEqYjJ2tD4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+o7N3ByEqRqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp06kv8fy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9lKnwRiBpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmDqCOJrJrW4s/4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+p7Y5COJrBmDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBeBp1Oowsfy9s72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+cjy91irxBiCpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmDqCGHq5DP3c/4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+pPR3yCHqxmDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBiCpz2auLjo78/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cfy9kafvBeBpxeBp0afvMfy9s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+rnp8D+buRiCpxqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBmCp16vx8fy9s72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+cnz906lwBWAphWApk2kv8nz9832+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+cfy9mSzyRmCqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqB6FqnzC1M32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+pfT4TuYtzqYtpPR3873+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+X7D1R6FqhqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBmCqCWKrYnK2s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+b7t8r7s8s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+Y3N3CWKrRmCqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBmCpyeLronK2s32+c73+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+c73+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+c32+Y3N3CiMrhmCpxqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBmCpySKrX3D1cfy9s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c/3+sfy9n7D1SWKrRmCpxqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBmCqB2FqmCwyLfo79D4+s72+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c72+dD4+rnp8GSzyh6FqhmCqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBmCpzyZuJDP3cfy9tD4+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+dD4+sjy95PR3z+buRmCqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBiCpx+HqlWpw57Y5Mfy9tD4+s/3+s32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c32+c73+tD4+sfy9p/Y5FirxCCHqxiCpxqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqBiCpyOJrFCmwYzM27Xm7sv0+ND4+tD4+s/3+s73+c32+c32+c32+c32+c73+c/3+tD4+tD4+sv1+Lbn747O3VKnwiOJrBiCpxmDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBmDqBiBpxuEqTGSslirxIPG15zX463h67/t88by9sfy9sfy9sby9sDt867i65zX44PG2FqsxTKTsxyEqRiBpxmDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqBqDqBmCpxeBpxmDqB+GqiiMrzuYt0afvEafvEafvEafvDuYtymMrx+GqhmDqBeBpxiCpxqDqBqDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBmCqBiCpxeBpxeBpxeBpxeBpxiCpxmCqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqBqDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABqDqBqDqBqDqBqDqBqDqBuDqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
'''
class SessionManager:
    def __init__(self, root, session_dir="."):
        self.root = root
        self.root.title("Session Restore Manager")
        self.session_dir = session_dir

        # Load icons (must be .ico or converted to .png via PIL if needed)
        self.save_icon = photoimage_from_base64_ppm(save_icon_base64)
        self.delete_icon = photoimage_from_base64_ppm(delete_icon_base64)
        self.restore_icon = photoimage_from_base64_ppm(restore_icon_base64)
        self.info_icon = photoimage_from_base64_ppm(info_icon_base64)


        # Frames
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.left_listbox = tk.Listbox(main_frame, width=40)
        self.left_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_listbox.bind("<<ListboxSelect>>", self.show_session_contents)

        self.right_listbox = tk.Listbox(main_frame, width=60)
        self.right_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Bottom UI
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        button_frame = tk.Frame(bottom_frame)
        button_frame.pack(side=tk.RIGHT)
        self.info_button = tk.Button(
            bottom_frame,
            text="",
            image=self.info_icon,
            compound=tk.LEFT,
            command=lambda: messagebox.showinfo("SRM Info", "Author: github/invalidusernamecalled,\nAuthor: Jinners\n\nIcons: icon-icons.com\nThank you for using SRM !")
        )
        self.info_button.pack(side=tk.LEFT, padx=(0, 5))
        self.info_label = tk.Label(bottom_frame, text="Session info will appear here", anchor="w")
        self.info_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        # Save Session button
        self.save_button = tk.Button(
            button_frame,
            text="Save & Close",
            image=self.save_icon,
            compound=tk.LEFT,
            command=self.save_session
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 5))

        self.restore_button = tk.Button(
            button_frame,
            text="Restore Session",
            image=self.restore_icon,
            compound=tk.LEFT,
            command=self.restore_session
        )
        self.restore_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = tk.Button(
            button_frame,
            text="Delete Session",
            image=self.delete_icon,
            compound=tk.LEFT,
            command=self.delete_session
        )
        self.delete_button.pack(side=tk.LEFT)

        self.session_files = []
        self.load_session_files()

    def load_session_files(self):
        print("Reloading session files...")  # Debug line
        files = sorted(
            [f for f in os.listdir(self.session_dir) if f.startswith("session_list_") and f.endswith(".txt")],
            reverse=True
        )
        self.session_files = files
        self.left_listbox.delete(0, tk.END)
        for f in files:
            self.left_listbox.insert(tk.END, f)
        self.right_listbox.delete(0, tk.END)
        self.info_label.config(text="Session info will appear here")

    def show_session_contents(self, event):
        selection = self.left_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        filename = self.session_files[index]
        full_path = os.path.join(self.session_dir, filename)

        # Show session datetime
        match = re.search(r"session_list_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})", filename)
        if match:
            date, time = match.groups()
            self.info_label.config(text=f"Session: {date} at {time.replace('-', ':')} hrs")
        else:
            self.info_label.config(text="Unknown session format")

        # Load session file
        self.right_listbox.delete(0, tk.END)
        try:
            with open(full_path, "r", encoding="ascii") as f:
                for line in f:
                    path = line.strip().strip('"')
                    if path:
                        self.right_listbox.insert(tk.END, os.path.basename(path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")

    def restore_session(self):
        selection = self.left_listbox.curselection()
        if not selection:
            messagebox.showwarning("No session selected", "Please select a session to restore.")
            return
        filename = self.session_files[selection[0]]
        with open(filename, "r", encoding="ascii") as f:
            for line in f:
                path = line.strip().strip('"')  # Remove newline and quotes
                if path:
                    try:
                        os.startfile(path)
                    except Exception as e:
                        print(f"Failed to open: {path}\n{e}")
        self.root.quit()

    def delete_session(self):
        selection = self.left_listbox.curselection()
        if not selection:
            messagebox.showwarning("No session selected", "Please select a session to delete.")
            return
        index = selection[0]
        filename = self.session_files[index]
        full_path = os.path.join(self.session_dir, filename)

        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{filename}' permanently?")
        if confirm:
            try:
                os.remove(full_path)
                self.load_session_files()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file:\n{e}")

    def show_loading_popup(self, message="Please wait..."):
        progress_win = tk.Toplevel(self.root)
        progress_win.title("")
        progress_win.resizable(False, False)
        progress_win.configure(bg="#eeeeee")
        progress_win.overrideredirect(True)  # No window borders

        # Dimensions
        win_width, win_height = 300, 100
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (win_width // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (win_height // 2)
        progress_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

        label = tk.Label(progress_win, text=message, font=("Arial", 11), bg="#eeeeee")
        label.pack(pady=(15, 5))

        progress = ttk.Progressbar(progress_win, mode="indeterminate", length=250)
        progress.pack(pady=(0, 20))
        progress.start(10)  # Speed of animation

        progress_win.update()
        return progress_win


    def save_session(self):
        # Step 1: Show confirmation dialog
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Confirm Save")
        confirm_popup.geometry("300x150")
        confirm_popup.transient(self.root)
        confirm_popup.grab_set()
        confirm_popup.resizable(False, False)
        confirm_popup.configure(bg="#f0f0f0")

        result = {'confirmed': False, 'close_chrome': False}

        def on_confirm():
            result['confirmed'] = True
            result['close_chrome'] = chrome_var.get()
            result['close_edge'] = edge_var.get()
            confirm_popup.destroy()

        def on_cancel():
            confirm_popup.destroy()
        # Label
        tk.Label(confirm_popup, text="Do you want to save the current session?", bg="#f0f0f0", font=("Arial", 11)).pack(pady=(20, 10))

        # Checkbox
        chrome_var = tk.BooleanVar(value=False)
        edge_var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(confirm_popup, text="Close Chrome as well", variable=chrome_var, bg="#f0f0f0", font=("Arial", 10))
        checkbox.pack()
        tk.Checkbutton(confirm_popup, text="Close Edge as well", variable=edge_var, bg="#f0f0f0", font=("Arial", 10)).pack()

        # Buttons
        button_frame = tk.Frame(confirm_popup, bg="#f0f0f0")
        button_frame.pack(pady=(10, 5))
        tk.Button(button_frame, text="Yes", width=10, command=on_confirm).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="No", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)

        self.root.wait_window(confirm_popup)
        if not result['confirmed']:
            return 
        try:
            loading = self.show_loading_popup("Closing Windows & Saving session...")
            if not os.path.exists("saver.ps1"):
                messagebox.showerror("Error", "Could not find 'saver.ps1'. Please make sure it exists in the same folder.")
                return
            subprocess.run("powershell -executionpolicy bypass -file saver.ps1", shell=True)
            if result['close_chrome']:
                subprocess.run("taskkill /IM chrome.exe", shell=True)
            if result['close_edge']:
                subprocess.run("taskkill /IM msedge.exe", shell=True)
            messagebox.showinfo("Saved", "Session has been saved.")
            self.load_session_files()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session:\n{e}")
        finally:
            loading.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app = SessionManager(root, session_dir=script_dir)
    root.mainloop()
