import PySimpleGUI as sg
import os
from pathlib import Path

class Controller:
    def __init__(self):
        self.server_array_2d = []
        self.log_file_folder = ""

        sg.theme('DarkBlack1')

        layout = [
            [sg.Text("Rocket League IP Parser", font=("Helvetica", 16))],
            [sg.Button("Select Log Folder", size=(20, 1))],
            [sg.Text("Log File:", size=(10, 1)), sg.Combo([], size=(50, 1), key='-LOG_FILE-', enable_events=True)],
            [sg.Text("Log Folder:", size=(10, 1)), sg.Text("", size=(50, 1), key='-LOG_FOLDER-')],
            [sg.Multiline("", size=(50, 20), key='-TEXTBOX-', disabled=True, autoscroll=True)],
            [sg.Button("Visit GitHub Link", size=(43, 1)), sg.Button("Close App", size=(20, 1))]
        ]

        self.window = sg.Window("Rocket League IP Parser", layout, finalize=True, no_titlebar=False, alpha_channel=0.9, resizable=True)
        self.window['-TEXTBOX-'].Widget.config(background="black", foreground="white", insertbackground="white")
        
        self.load_logs()

    def load_logs(self, folder_path=None):
        if not folder_path:
            default_path = Path(os.getenv("USERPROFILE"), "OneDrive", "Documents", "My Games", "Rocket League", "TAGame", "Logs")
            folder_path = default_path.as_posix()  # Convert to forward slashes

        self.log_file_folder = folder_path
        self.window['-LOG_FOLDER-'].update(self.log_file_folder)

        # Get all .log files in the directory
        log_files = sorted(Path(self.log_file_folder).glob("*.log"), key=os.path.getmtime, reverse=True)
        log_files = [f.name for f in log_files]  # List of filenames

        if log_files:
            self.window['-LOG_FILE-'].update(values=log_files, value=log_files[0])
            self.begin_parse(Path(self.log_file_folder) / log_files[0])
        else:
            sg.popup("No log files found!")

    def begin_parse(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            temp_list = [line.strip() for line in lines if "GameURL" in line]

            self.server_array_2d = []
            for temp in temp_list:
                server_name_index = temp.find("ServerName=\"") + 12
                server_game_url_index = temp.find("GameURL=\"") + 9

                server_name_sub = temp[server_name_index: temp.find("\"", server_name_index)]
                server_game_url_sub = temp[server_game_url_index: temp.find(":", server_game_url_index)]

                region_index = temp.find("Region=\"") + 8
                region_sub = temp[region_index: temp.find("\"", region_index)]

                self.server_array_2d.append([server_name_sub, server_game_url_sub, region_sub])

            self.update_textbox()
            self.window['-LOG_FOLDER-'].update(file_path.name)

        except Exception as e:
            sg.popup_error(f"Error: {e}")

    def update_textbox(self):
        self.window['-TEXTBOX-'].update("")
        for server_info in self.server_array_2d:
            self.window['-TEXTBOX-'].print(f"{server_info[0]} | {server_info[1]} | {server_info[2]}")

    def select_folder(self):
        folder_path = sg.popup_get_folder("Select Log Folder", default_path=self.log_file_folder)
        if folder_path:
            self.load_logs(folder_path)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Close App":
                break
            elif event == "Select Log Folder":
                self.select_folder()
            elif event == '-LOG_FILE-':
                selected_file = values['-LOG_FILE-']
                if selected_file:
                    self.begin_parse(Path(self.log_file_folder) / selected_file)
            elif event == "Visit GitHub Link":
                os.system("start https://github.com/noarche/Rocket-League-IP-Parser")

        self.window.close()

if __name__ == "__main__":
    app = Controller()
    app.run()
