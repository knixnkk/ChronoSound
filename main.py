import customtkinter
from CTkTable import CTkTable
import json
import os
from tkinter import filedialog
import threading
from datetime import datetime, timedelta
import pygame
from PIL import Image, ImageTk


db = "new_database.json"
data = {}

def loadDB(database):
    global data
    if os.path.isfile(database):
        with open(database, 'r') as file:
            data = json.load(file)
    else:
        # Initialize the new database structure
        data = {
            "last-check": "",
            "PreMatchPath": "",
            "PreMatchStatus": "disable",
            "PostMatchPath": "",
            "PostMatchStatus": "disable",
            "SystemtimePath" : "",
            "Store_data": []
        }
        saveDB(database)

def saveDB(database):
    if os.path.isfile(database):
        with open(database, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        with open(database, 'w+') as file:
            json.dump(data, file, indent=4)

def open_new_window(row):
    new_window = customtkinter.CTkToplevel(root)
    new_window.title("ตั้งค่าเวลา")
    new_window.geometry("300x200")

    label = customtkinter.CTkLabel(new_window, text="ตั้งค่าเวลา (HH:MM):", font=("Arial", 15))
    label.pack(pady=10)
    
    time_entry = customtkinter.CTkEntry(new_window, placeholder_text="00:00", font=("Arial", 15))
    time_entry.pack(pady=10)
    
    def confirm_time():
        time_value = time_entry.get()
        try:
            datetime.strptime(time_value, "%H:%M")
            data["Store_data"][row - 1]["Time"] = time_value  
            saveDB(db)  
            update_cell(row, 1, time_value)  
            new_window.destroy()  
        except ValueError:
            print("Invalid time format. Please use HH:MM.")
            customtkinter.CTkLabel(new_window, text="Invalid time format. Use HH:MM.").pack(pady=5)

    confirm_button = customtkinter.CTkButton(new_window, text="ยืนยัน", command=confirm_time, font=("Arial", 15))
    confirm_button.pack(pady=10)

def open_file_dialog(row):
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio files", "*.mp3 *.wav *.aac *.flac *.ogg"),
                  ("MP3 files", "*.mp3"),
                  ("WAV files", "*.wav"),
                  ("AAC files", "*.aac"),
                  ("FLAC files", "*.flac"),
                  ("OGG files", "*.ogg"),
                  ("All files", "*.*")]
    )
    if file_path:
        file_name = os.path.basename(file_path)
        data["Store_data"][row - 1]["Audio Path"] = file_path
        saveDB(db)
        update_cell(row, 3, file_name)

def update_cell(row, column, new_value):
    if new_value == "ปิด":
        table.insert(row, column, new_value, text_color="red")
    elif new_value == "เปิด":
        table.insert(row, column, new_value, text_color="green")
    else:
        table.insert(row, column, new_value, text_color="black")

def on_cell_click(e):
    row = e['row']
    column = e['column']
    value = e['value']
    if row == 0:
        return
    if column == 0:
        return
    elif column == 1:
        open_new_window(row)
    elif column == 2:
        open_file_dialog(row)
    elif column == 4:
        new_value = 'เปิด' if value == 'ปิด' else 'ปิด'
        update_cell(row, column, new_value)
        data["Store_data"][row-1]["Enable/Disable"] = new_value  # Update the data list
        saveDB(db)
    else:
        print(f"Cell clicked: Row {row}, Column {column}, Value {value}")

def add_row():
    next_index = len(data["Store_data"]) + 1
    new_row = {
        "Index": next_index,
        "Time": "00:00",
        "Audio Select": "Select Audio",
        "Audio Path": "",
        "Enable/Disable": "ปิด"
    }
    data["Store_data"].append(new_row)
    table.add_row([new_row["Index"], new_row["Time"], new_row["Audio Select"], new_row["Audio Path"], new_row["Enable/Disable"]])
    saveDB(db)
    update_table_row(next_index)

def update_table_row(row_index):
    """Ensure that the text color is properly set for all columns in the new row."""
    row = data["Store_data"][row_index - 1]
    table.insert(row_index, 0, row["Index"], text_color="black")
    table.insert(row_index, 1, row["Time"], text_color="black")
    table.insert(row_index, 2, "เลือกเสียง", text_color="black")
    table.insert(row_index, 3, os.path.basename(row["Audio Path"]), text_color="black")
    
    if row["Enable/Disable"] == "ปิด":
        table.insert(row_index, 4, "ปิด", text_color="red")
    elif row["Enable/Disable"] == "เปิด":
        table.insert(row_index, 4, "เปิด", text_color="green")
        
def delete_row():
    if data["Store_data"]:
        data["Store_data"].pop()  # Remove last row
        table.delete_row(len(data["Store_data"]) + 1)
        saveDB(db)

# Initialize pygame mixer
pygame.mixer.init()

def play_audio(audio_path):
    try:
        if audio_path.lower().endswith('.wav'):
            sound = pygame.mixer.Sound(audio_path)
            sound.play()
        else:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing audio: {e}")

def get_duration(audio_path):
    try:
        if audio_path.lower().endswith('.wav'):
            sound = pygame.mixer.Sound(audio_path)
            duration = sound.get_length()
            return duration
        else:
            pygame.mixer.music.load(audio_path)
            duration = pygame.mixer.music.get_length()
            return duration
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0 
        
def check_timer():
    loadDB(db)
    current_time = datetime.now().strftime('%H:%M')  
    msg = ""
    def play_sequentially(sounds):
        try:
            for sound_file in sounds:
                print(sound_file)
                if sound_file.split('.')[-1] == "wav":
                    sound = pygame.mixer.Sound(sound_file)
                    sound.play()
                    while pygame.mixer.get_busy(): 
                        continue
                else: 
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        continue
        except Exception as e:
            print(f"Error during playback: {e}")
    
    for row in data["Store_data"]:
        sound_list = []
        match_time_obj = datetime.strptime(row["Time"], "%H:%M")
        if data["last-check"] != current_time:
            if row["Time"] == current_time:
            
                if (data["PreMatchStatus"] == "enable") and (row["Enable/Disable"] == "เปิด"):
                        sound_list.extend([data["PreMatchPath"]])

                if (row["Enable/Disable"] == "เปิด"):
                    SystemtimePath = data["SystemtimePath"]
                    Hours = match_time_obj.strftime("%H")
                    Minute = match_time_obj.strftime("%M")
                    if SystemtimePath:
                        sound_list.extend([
                                os.path.join(SystemtimePath, "time.wav"),
                                os.path.join(SystemtimePath, f"{str(int(Hours))}.wav"),
                                os.path.join(SystemtimePath, "hour.wav"),
                                os.path.join(SystemtimePath, f"{Minute}.wav"),
                        ])
                        if Minute != "00":
                            sound_list.extend([
                                os.path.join(SystemtimePath, "min.wav"),
                                row["Audio Path"]
                            ])
                        else:
                            sound_list.extend([
                                row["Audio Path"]
                            ])
                    else:
                        sound_list.extend([
                            row["Audio Path"]
                        ])

                if (data["PostMatchStatus"] == "enable") and (row["Enable/Disable"] == "เปิด"):
                    sound_list.extend([data["PostMatchPath"]])
                """
                the sound list should be like 
                [
                    data["PreMatchPath"], 
                    os.path.join(SystemtimePath, "time.wav"),
                    os.path.join(SystemtimePath, f"{Hours}.wav"),
                    os.path.join(SystemtimePath, "hour.wav"),
                    os.path.join(SystemtimePath, f"{Minute}.wav"),
                    os.path.join(SystemtimePath, "min.wav"),
                    data["PostMatchPath"]
                ]
                """
                play_sequentially(sound_list)
                #print(match_time_obj.strftime("%H:%M:%S"), current_time == match_time_obj.strftime("%H:%M"))
    data["last-check"] = current_time
    saveDB(db)
    root.after(1000, check_timer)


# Settings window code
def open_settings_window():
    settings_window = customtkinter.CTkToplevel(root)
    settings_window.title("Settings")
    settings_window.minsize(width=400, height=300)

    def prebox_event():
        print("prebox_event triggered, current value:", prevar_var.get())
        data["PreMatchStatus"] = prevar_var.get()
        saveDB(db)
        
    def postbox_event():
        print("postbox_event triggered, current value:", post_var.get())
        data["PostMatchStatus"] = post_var.get()
        saveDB(db)
        
    def select_pre_sound():
        pre_sound_path = filedialog.askopenfilename(
            title="Select Pre Sound File",
            filetypes=[("Audio files", "*.mp3 *.wav *.aac *.flac *.ogg")]
        )
        if pre_sound_path:
            pre_sound_label.configure(text="Pre Sound Path: " + os.path.basename(pre_sound_path))  # Display selected file name
            data["PreMatchPath"] = pre_sound_path
            saveDB(db)
            
    def select_post_sound():
        post_sound_path = filedialog.askopenfilename(
            title="Select Post Sound File",
            filetypes=[("Audio files", "*.mp3 *.wav *.aac *.flac *.ogg")]
        )
        if post_sound_path:
            post_sound_label.configure(text="Post Sound Path: " + os.path.basename(post_sound_path))  # Display selected file name
            data["PostMatchPath"] = post_sound_path
            saveDB(db)
            
    def select_system_sound():
        system_sound_path = filedialog.askdirectory(
            title="Select System Sound Folder"
        )
        if system_sound_path:
            system_sound_label.configure(text="System Path: " + os.path.basename(system_sound_path))  # Display selected file name
            data["SystemtimePath"] = system_sound_path
            saveDB(db)
            
    select_systemtime_button = customtkinter.CTkButton(settings_window, text="เลือกโฟลเดอร์เสียงนาฬิกา", command=select_system_sound, font=("Arial", 15))
    select_systemtime_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    prevar_var = customtkinter.StringVar(value=data["PreMatchStatus"])
    prebox = customtkinter.CTkCheckBox(settings_window, text="เสียงออดหน้า", command=prebox_event, variable=prevar_var, onvalue="enable", offvalue="disable", font=("Arial", 15))
    prebox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
    post_var = customtkinter.StringVar(value=data["PostMatchStatus"])
    postbox = customtkinter.CTkCheckBox(settings_window, text="เสียงออดหลัง", command=postbox_event, variable=post_var, onvalue="enable", offvalue="disable", font=("Arial", 15))
    postbox.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    
    select_pre_button = customtkinter.CTkButton(settings_window, text="เลือกเสียงออดหน้า", command=select_pre_sound, font=("Arial", 15))
    select_pre_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    select_post_button = customtkinter.CTkButton(settings_window, text="เลือกเสียงออดหลัง", command=select_post_sound, font=("Arial", 15))
    select_post_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    pre_sound_label = customtkinter.CTkLabel(settings_window, text=f"Pre Sound Path: {os.path.basename(data.get('PreMatchPath', '')) or 'None'}", font=("Arial", 15))
    pre_sound_label.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    post_sound_label = customtkinter.CTkLabel(settings_window, text=f"Post Sound Path: {os.path.basename(data.get('PostMatchPath', '')) or 'None'}", font=("Arial", 15))
    post_sound_label.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
    
    system_sound_label = customtkinter.CTkLabel(settings_window, text=f"System Sound Path: {os.path.basename(data.get('SystemtimePath', '')) or 'None'}", font=("Arial", 15))
    system_sound_label.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
    
    close_button = customtkinter.CTkButton(settings_window, text="Close", command=settings_window.destroy)
    close_button.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

loadDB(db)
root = customtkinter.CTk()
root.title("ออดโรงเรียนปิยะมหาราชาลัย")
root.wm_iconbitmap('assets/logo.ico')

headers = ["Index", "Time", "Audio Select", "Audio Path", "Enable/Disable"]
values = [headers] + [list(row.values()) for row in data["Store_data"]]
table = CTkTable(
    master=root,
    row=len(values),
    column=len(headers),
    values=values,
    colors=["#D6C0B3", "#E4E0E1"],
    header_color="#AB886D",
    color_phase="horizontal",
    corner_radius=0,
    command=on_cell_click,
    font=("Arial", 15)
)

add_row_button = customtkinter.CTkButton(root, text="Add Row ( เพิ่มแถว )", command=add_row, font=("Arial", 20))
add_row_button.grid(row=0, column=0, padx=10, pady=2, sticky="ew")


delete_row_button = customtkinter.CTkButton(root, text="Delete Row ( ลบแถว )", command=delete_row, font=("Arial", 20))
delete_row_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

setting_button = customtkinter.CTkButton(root, text="Setting ( ตั้งค่าระบบ )", command=open_settings_window, font=("Arial", 20))
setting_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

table.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

for i, row in enumerate(data["Store_data"]):
    table.insert(i + 1, 0, row["Index"], text_color="black")
    table.insert(i + 1, 1, row["Time"], text_color="black")
    table.insert(i + 1, 2, "เลือกเสียง", text_color="black")
    table.insert(i + 1, 3, os.path.basename(row["Audio Path"]), text_color="black")
    if row["Enable/Disable"] == "ปิด":
        table.insert(i + 1, 4, "ปิด", text_color="red")
    elif row["Enable/Disable"] == "เปิด":
        table.insert(i + 1, 4, "เปิด", text_color="green")
check_timer()
root.mainloop()
