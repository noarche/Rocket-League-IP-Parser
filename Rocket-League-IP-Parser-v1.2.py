import tkinter as tk
from tkinter import filedialog
import os

class Controller:
    def __init__(self, root):
        self.server_array_2d = None
        self.log_file_folder = ""

        root.title("Rocket League IP Parser")
        root.geometry("370x840")  # Change the size to 270x600
        root.resizable(False, True)  # Make the app non-resizable
        root.configure(bg="black")

        self.log_folder_link = tk.Label(root, text="Open Directory Explorer", bg="Gray", fg="yellow", cursor="hand2")
        self.log_folder_link.grid(row=0, column=0, pady=(20, 0))
        self.log_folder_link.bind("<Button-1>", self.open_log_folder)
        self.log_folder_link.config(state=tk.DISABLED)

        github_link = tk.Label(root, text="Visit GitHub Link", bg="Gray", fg="Blue", cursor="hand2")
        github_link.grid(row=1, column=0, pady=(10, 0))
        github_link.bind("<Button-1>", self.open_github_link)

        close_button = tk.Button(root, text="Close App", command=root.destroy, bg="Gray", fg="Red")
        close_button.grid(row=2, column=0, pady=(10, 0))

        open_file_button = tk.Button(root, text="Open Log File", command=self.open_file, bg="Gray", fg="green")
        open_file_button.grid(row=3, column=0, pady=(10, 0))

        self.grid_frame = tk.Frame(root, bg="black")
        self.grid_frame.grid(row=4, column=0, pady=(10, 0))

        self.textbox = tk.Text(self.grid_frame, wrap="none", height=10, width=40, fg="white", bg="black", bd=0, selectbackground="blue")
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add a vertical scrollbar to the textbox
        scrollbar = tk.Scrollbar(self.grid_frame, command=self.textbox.yview)
        scrollbar.grid(row=0, column=1, sticky="nsew")
        self.textbox.config(yscrollcommand=scrollbar.set)

        # Make the app non-resizable
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def open_log_folder(self, event):
        os.system(f'explorer "{self.log_file_folder}"')

    def open_github_link(self, event):
        os.system("start https://github.com/noarche/Rocket-League-IP-Parser")

    def open_file(self):
        try:
            default_path = os.path.join(os.getenv("USERPROFILE"), "Documents", "My Games", "Rocket League", "TAGame", "Logs")
            file_path = filedialog.askopenfilename(initialdir=default_path, title="Open Log File")
            if file_path and file_path.lower().endswith(".log"):
                self.begin_parse(file_path)
        except Exception as e:
            print(f"Error: {e}")

    def begin_parse(self, file_path):
        self.log_folder_link.config(state=tk.DISABLED)
        self.log_folder_link["text"] = ""

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

                # Extract contents between double quotes for the Region attribute
                region_index = temp.find("Region=\"") + 8
                region_sub = temp[region_index: temp.find("\"", region_index)]

                self.server_array_2d.append([server_name_sub, server_game_url_sub, region_sub])

            self.update_grid()
            self.update_textbox()

            self.log_folder_link["text"] = os.path.basename(file_path)
            self.log_file_folder = os.path.dirname(file_path)

        except Exception as e:
            print(f"Error: {e}")

        self.log_folder_link.config(state=tk.NORMAL)

    def update_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for i, server_info in enumerate(self.server_array_2d):
            label1 = tk.Label(self.grid_frame, text=server_info[0], fg="white", bg="black")
            label1.grid(row=i, column=0)

            label2 = tk.Label(self.grid_frame, text=server_info[1], fg="white", bg="black")
            label2.grid(row=i, column=1)

    def update_textbox(self):
        self.textbox.delete(1.0, tk.END)
        for server_info in self.server_array_2d:
            self.textbox.insert(tk.END, f"{server_info[0]} | {server_info[1]} | {server_info[2]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
