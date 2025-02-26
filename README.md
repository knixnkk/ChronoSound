# ChronoSound

## Description
ChronoSound is a Python-based audio scheduling system that allows users to set up customizable alerts and play specific sounds at scheduled times. Built using CustomTkinter for a modern UI and pygame for audio playback, this tool is ideal for reminders, automated announcements, or timed notifications.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/knixnkk/ChronoSound.git
   cd https://github.com/knixnkk/ChronoSound.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the project with:
```sh
python main.py
```

To compile the project into an executable using PyInstaller, run:
```sh
pyinstaller --noconfirm --onedir --windowed --add-data "your-customtkinter-location" --icon="assets/logo.ico" -w -F --add-binary "assets/logo.ico;." "main.py"
```

## ✨ Features  
- ⏰ **Scheduled Audio Playback** – Set specific times for sounds to play.  
- 🕒 **Real-Time Clock** – Displays an updated clock in the UI.  
- 🎚 **Adjustable Volume** – Control the playback volume for each alert.  
- 🔁 **Loop & Repeat Sounds** – Set alarms to repeat as needed.  
- 📂 **File Selection** – Easily browse and choose audio files.  
- ✅ **User-Friendly UI** – Modern interface for ease of use.  


## Author
knixnkk - [GitHub Profile](https://github.com/knixnkk)

