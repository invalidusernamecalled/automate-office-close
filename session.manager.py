import base64
from io import BytesIO
import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
from PIL import Image, ImageTk
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

save_icon_base64 = '''
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC2UlEQVR42u3X70sTcRzA8R70VIIe9Sfkk/LX5m1uuwK1oowikxEZRfUon1QQPaiMHhRoVFYMk9uUumloUrQiIlMr3dTUndva7tQ2MVth3hKZ6a1tn+4O/Gpsu3bXxCd+4f1g38H3++L7PTZug5bwZWFWuja3rtO2veaFbWZu3sZxnOIsDkZcp8DU06a10uewVs/mDVJDQzKk1spAXl0X5NS8BHZuHiKRCJjto1Bq6kDR30LC/D+zOEbFdQpMvSCsq7HSIU0zs1cK4E8GqOv2Cp9RnilWCWAJsaBtYfQpAHRgNQEokmF5yNa1AaCTYPyqRs+WtQCg+P368equjasCWOQWoL6Pgpxb7aBqeAvaFuffWb0iAiPpkykBY99/ogXldmniAuzwFKbM0H906RTepwSUW94BOTAOjwf9sjvkqpAE4M7SpQfyVwIg/263APivdPb96QDEEgBYk4s/hU7Iu92hOL3jgHJAJjJ8PLwOWAesA5QDSlvH4N7QNBAjPxR30G1UDng+PgtyRigSguO0ESpHK1Aln3TSALcG8KEyMYNbPYYPq9sRwPE1DMKIx+Np//lcYy7zi6rRBnLCR9RxXa+6PAHAcRwEAoG08vm9UE6Vyd1cROsdqofoChBAwaBmh2EnhckCGBx7IP9N/qakgFgsBuFwWFZ3mJtpXwXuLISiJ0/RQ5gAEO42GAzKajI4CSdcR9I6et2rK8DvlwqgfPjnP0MJpZcEVLqN/OYeaUA0GgWWZRVloRsAdyW/imKqCHxztLD56gFm2Bk46z2T8DwIKHKqCX7H4tKATIzpxWnYRxWvuPdCqPKehlg8ugwg6RWAR16/MGlrPAZfzNsyUltztvBDIwJ2DRTAoCVbnJ8w54oADemLLQPMQySPgCqLGa4S1zPW7tenAHeqwdh+Ec1VEzeEzUFDDH9AAC3Rk4XV22uxB322jEZ02IqenU/ynd2kut+PXs/+AAU4yE8khmP8AAAAAElFTkSuQmCC
'''
restore_icon_base64 = '''
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
'''
delete_icon_base64 = '''
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAApZJREFUeNrVl01PE0EYx+HSD7BQj/0UIlGwBEqIUah7kB7QxIvWaIwJgZj4elD0ZPUifgVConjQHsBoognUs/gFCpIWqon0Zbd2yz7+Nzwh3WX2ZdhCwiS/y+7O8//P7DzzzHQcy1ZNnIqAEyDGREHksEW7wEWQAVnwE+SZVZDld0mgtFNYAbfBd1AH5EMd5LiPEka4E8TBJ2AAksTgvv3S4tpQjyU+ATYAhWQdjFsxZUZ/GWztBRnqoergyeCi+BZ9Wp8VQSqo+AD41RqsljpP+p1rPsJsdOQM6ZM3qDY26DSxBuJBFtySTfzSOTK+fSHzd4nqT+5xUBfx4V76N5shs1KmxsI8VS8MOL9f9FyYvHKbHJCskRtfPxNxM/84TDjFX0Ncq+1+3GxS4/28cyaaIO0m3g1yraPX70+SWa2wvNCEWJybWdgg7fqEc/2sgG6RAXVfno+cFgdmEwjsLl7aIv3RlNs+kRQZyABi/EdnrYmZB3j3Qiz+cMorc56J9vYsICkTlTKeaVLiTNZWO7iYrAKSNCEvDlgr2mogBvKAfE28eUnUaOwX3/6Lfz7tLw5YK3ZAA6/EBsrbnB3yBsL/AnGKevEDREMvQoyaF6G0iY8gEi4NS5ukP75rS0MJE09F+0BSuBHNZrzy3NUgmxCJ62DU7ci1YtuKp29Z0+wm7j9LxQJpN686M2MZdAUrRuowGR8WiHZ2ROL+xejdnLAYBS/HSCkrgGXC3CwIxEUmuBy/nUM5jsuVYzbRD9ZsJtQEaekrYQ8kedAX9FQ0DoptPJIVgNoRtNV2T8QpsA4oJHmgaonezoMcy8+CxRDH8iXQ146LSRrkJC4my9xHaffVbAw897iazYBRoBzF5TTqvJwey5v2fy10IdScBh/wAAAAAElFTkSuQmCC
'''
info_icon_base64 = '''
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
'''
class SessionManager:
    def __init__(self, root, session_dir="."):
        self.root = root
        self.root.title("Session Restore Manager")
        self.session_dir = session_dir

        # Load icons (must be .ico or converted to .png via PIL if needed)
        self.save_icon = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(save_icon_base64))))
        self.delete_icon = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(delete_icon_base64))))
        self.restore_icon = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(restore_icon_base64))))
        self.info_icon = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(info_icon_base64))))


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
            text="Save Session",
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
            confirm_popup.destroy()

        def on_cancel():
            confirm_popup.destroy()
        # Label
        tk.Label(confirm_popup, text="Do you want to save the current session?", bg="#f0f0f0", font=("Arial", 11)).pack(pady=(20, 10))

        # Checkbox
        chrome_var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(confirm_popup, text="Close Chrome as well", variable=chrome_var, bg="#f0f0f0", font=("Arial", 10))
        checkbox.pack()

        # Buttons
        button_frame = tk.Frame(confirm_popup, bg="#f0f0f0")
        button_frame.pack(pady=(10, 5))
        tk.Button(button_frame, text="Yes", width=10, command=on_confirm).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="No", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)

        self.root.wait_window(confirm_popup)
        if not result['confirmed']:
            return 
        try:
            loading = self.show_loading_popup("Saving session...")
            subprocess.run("powershell -executionpolicy bypass -file saver.ps1", shell=True)
            if result['close_chrome']:
                subprocess.run("taskkill /IM chrome.exe", shell=True)
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
