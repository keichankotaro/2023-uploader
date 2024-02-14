import os
import hashlib
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread
from tkinter import messagebox
from time import sleep

class FileUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("アップローダー")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.enable_close)
        
        self.file_list = []
        self.upload_progress = 0  # アップロード進捗を追跡

        # 表のヘッダ
        headers = ["結果", "ファイル名", "チェックサム", "メッセージ"]
        self.tree = ttk.Treeview(root, columns=headers, show="headings", height=10)
        for header in headers:
            self.tree.heading(header, text=header)
            # Set column width based on content
            if header == "結果":
                self.tree.column(header, width=40)  # Adjust width for two full-width characters
            elif header == "チェックサム":
                self.tree.column(header, width=240)  # Adjust width for 32 half-width characters
            elif header == "ファイル名":
                self.tree.column(header, width=240)
            elif header == "メッセージ":
                self.tree.column(header, width=360)
        self.tree.grid(row=0, column=0, columnspan=4, pady=10, sticky='nsew')  # Use sticky to expand in all directions
        
        # ボタン
        self.select_folder_button = tk.Button(root, text="フォルダを選択", command=self.select_folder)
        self.select_folder_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')  # Use sticky to expand in all directions

        self.update_button = tk.Button(root, text="更新", command=lambda: [Thread(target=self.update_files).start()], state=tk.DISABLED)
        self.update_button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')  # Use sticky to expand in all directions

        self.upload_button = tk.Button(root, text="一括アップロード", command=lambda: [Thread(target=self.upload_files()).start()], state=tk.DISABLED)
        self.upload_button.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')  # Use sticky to expand in all directions

        # プログレスバー
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("red.Horizontal.TProgressbar", background="red")
        style.configure("yellow.Horizontal.TProgressbar", background="yellow")
        style.configure("green.Horizontal.TProgressbar", background="green")
        style.configure("blue.Horizontal.TProgress", background="blue")
        self.progress_bar = ttk.Progressbar(root, length=300, mode="determinate", maximum=100, style="green.Horizontal.TProgressbar")#, orient="horizontal"
        self.progress_bar.grid(row=2, column=0, columnspan=3, pady=10)

        # Configure row and column weights to make them expand
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_rowconfigure(2, weight=1)
        
    def disable_close(self):
        Thread(target=messagebox.showinfo, args=("", "画像の読み込み中、及びアップロード中はウィンドウを閉じることは出来ません。")).start()
        
    def enable_close(self):
        if messagebox.askyesno("確認", "終了しますか?"):
            self.root.destroy()
        else:
            pass

    def select_folder(self):
        self.root.wm_protocol("WM_DELETE_WINDOW", self.disable_close)
        folder_path = filedialog.askdirectory()
        self.folder_path = folder_path
        if folder_path:
            self.file_list = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png'))]
            #print(self.file_list)
            self.upload_button.config(state=tk.DISABLED)
            self.select_folder_button.config(state=tk.DISABLED)
            self.update_button.config(state=tk.DISABLED)
            self.upload_progress = 0
            self.progress_bar["value"] = 0
            self.progress_bar["maximum"] = 100
            self.progress_bar.config(style="blue.Horizontal.TProgressbar")
            Thread(target=self.display_files).start()

    def display_files(self):
        self.progress_bar.config(style="blue.Horizontal.TProgressbar")
        self.tree.delete(*self.tree.get_children())
        for file_name in self.file_list:
            #result, message = self.get_result_and_message(file_name)
            #checksum = self.calculate_checksum(os.path.join(self.folder_path, file_name))

            # 非同期で画像を読み込む
            #t = Thread(target=self.load_and_insert_image, args=(file_name, self.get_result_and_message(file_name)[0], self.calculate_checksum(os.path.join(self.folder_path, file_name)), self.get_result_and_message(file_name)[1]))
            #t = Thread(target=self.root.after, args=(0, self.insert_image, file_name, self.get_result_and_message(file_name)[0], self.calculate_checksum(os.path.join(self.folder_path, file_name)), self.get_result_and_message(file_name)[1]))
            #t.start()
            #t.join()
            self.root.after(0, self.insert_image, file_name, self.get_result_and_message(file_name)[0], self.calculate_checksum(os.path.join(self.folder_path, file_name)), self.get_result_and_message(file_name)[1])
            self.upload_progress += 1
            self.progress = int(self.upload_progress / len(self.file_list) * 100)
            self.progress_bar["value"] = self.progress
        Thread(target=self.enable_button).start()
    
    def enable_button(self):
        sleep(1)
        self.upload_button.config(state=tk.NORMAL)
        self.select_folder_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.NORMAL)
        self.upload_progress = 0
        self.progress_bar["value"] = 0
        self.progress_bar.config(style="green.Horizontal.TProgressbar")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.enable_close)

    def load_and_insert_image(self, file_name, result, checksum, message):
        try:
            #file_path = os.path.join(self.folder_path, file_name)
            #image = Image.open(file_path)
            #image.thumbnail((50, 50))  # 画像サイズを調整

            # ImageTk.PhotoImage で画像を表示
            #img = ImageTk.PhotoImage(image)
            sleep(0.1)
            t = Thread(target=self.root.after, args=(0, self.insert_image, file_name, result, checksum, message))
            t.start()
            sleep(0.1)
        except Exception as e:
            print(f"Error loading image: {e}")

    def insert_image(self, file_name, result, checksum, message):
        self.tree.insert("", "end", values=[result, file_name, checksum, message])

    # def update_files(self):
    #     if not self.folder_path:
    #         return

    #     current_file_list = self.file_list.copy()
    #     self.file_list = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.jpg', '.png'))]
        
    #     # Update existing entries and add new ones
    #     for file_name in self.file_list:
    #         result, message = self.get_result_and_message(file_name)
    #         if file_name in current_file_list:
    #             # Update existing entry
    #             item_id = None
    #             for item in self.tree.get_children():
    #                 if self.tree.item(item, "values")[1] == file_name:
    #                     item_id = item
    #                     break
    #             if item_id:
    #                 self.tree.set(item_id, "結果", result)
    #                 self.tree.set(item_id, "メッセージ", message)
    #         else:
    #             # Add new entry
    #             Thread(target=self.display_files).start()
    def update_files(self):
        self.root.wm_protocol("WM_DELETE_WINDOW", self.disable_close)
        self.upload_button.config(state=tk.DISABLED)
        self.select_folder_button.config(state=tk.DISABLED)
        self.update_button.config(state=tk.DISABLED)
        if not self.folder_path:
            return

        current_file_list = self.file_list.copy()
        self.file_list = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.jpg', '.png'))]
        
        # Update existing entries and add new ones
        for file_name in self.file_list:
            result, message = self.get_result_and_message(file_name)
            if file_name in current_file_list:
                # Update existing entry
                item_id = None
                for item in self.tree.get_children():
                    if self.tree.item(item, "values")[1] == file_name:
                        item_id = item
                        break
                if item_id:
                    self.tree.set(item_id, "結果", result)
                    self.tree.set(item_id, "メッセージ", message)
            else:
                # Add new entry
                checksum = self.calculate_checksum(os.path.join(self.folder_path, file_name))
                self.tree.insert("", "end", values=[result, file_name, checksum, message])

        # Delete entries for files that no longer exist
        for file_name in current_file_list:
            if file_name not in self.file_list:
                for item in self.tree.get_children():
                    if self.tree.item(item, "values")[1] == file_name:
                        self.tree.delete(item)
                        break
        self.upload_button.config(state=tk.NORMAL)
        self.select_folder_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.NORMAL)

    def upload_files(self):
        self.root.wm_protocol("WM_DELETE_WINDOW", self.disable_close)
        self.progress_bar.config(style="green.Horizontal.TProgressbar")
        self.upload_button.config(state=tk.DISABLED)
        self.select_folder_button.config(state=tk.DISABLED)
        self.update_button.config(state=tk.DISABLED)
        if not self.file_list:
            return

        base_url = "***"
        auth_data = {"id": "*****", "password": "*****"}

        def upload_single_file(file_name, time=0):
            if not self.check_file_exists(file_name):
                file_path = os.path.join(self.folder_path, file_name)
                checksum = self.calculate_checksum(file_path)

                # Check if the file already exists
                #if self.check_file_exists(base_url, auth_data, checksum):
                #    self.update_table(file_name, "×", "That file already exists. Please specify a different file name.")
                #    return

                files = {'files': open(file_path, 'rb')}
                params = {**auth_data, 'checksum': checksum}

                response = requests.post(base_url, files=files, data=params)

                if response.status_code == 200:
                    result = response.json().get('status', -1)
                    if result == 0:
                        if time == 0:
                            self.update_table(file_name, "○", "Upload completed.")
                        else:
                            self.update_table(file_name, "○", "Upload completed. (Retry: "+str(time)+")")
                        #self.update_table(file_name, "○", "Upload completed.")
                        self.increment_progress()
                    elif result == 1:
                        self.update_table(file_name, "×", "The file type is not supported. You can upload JPG or PNG files.")
                        self.increment_progress()
                    elif result == 2:
                        self.update_table(file_name, "×", "That file already exists. Please specify a different file name.")
                        self.increment_progress()
                    elif result == 3:
                        self.update_table(file_name, "×", "Checksums did not match. The data may be corrupted or the hash type may be incorrect. Please use MD5 checksum.")
                        self.increment_progress()
                    else:
                        self.update_table(file_name, "×", f"Unknown error. Status: {result}")
                        self.increment_progress()
                else:
                    if response.status_code >= 500 and response.status_code < 600:
                        self.update_table(file_name, "×("+str(time)+")", f"HTTP POST request failed. Status code: {response.status_code}. Retrying... (retry: "+str(time)+")")
                        upload_single_file(file_name, time=time+1)
                    else:
                        self.update_table(file_name, "×", f"HTTP POST request failed. Status code: {response.status_code}")
                        self.increment_progress()
                if self.progress_bar["value"] == 100:
                    Thread(target=self.enable_button).start()
            else:
                self.update_table(file_name, "×", "That file already exists. Please specify a different file name.")
                self.increment_progress()
                if self.progress_bar["value"] == 100:
                    Thread(target=self.enable_button).start()
                return

        # プログレスバーの初期化
        self.upload_progress = 0
        self.progress_bar["value"] = 0

        # ファイル数に基づいて進捗バーの最大値を設定
        self.progress_bar["maximum"] = 100

        # 非同期にファイルをアップロードする
        for file_name in self.file_list:
            # すでにアップロード済みのファイルはスキップ
            if self.is_file_uploaded(file_name):
                self.increment_progress()
                if self.progress_bar["value"] == 100:
                    Thread(target=self.enable_button).start()
                continue

            t = Thread(target=upload_single_file, args=(file_name,))
            t.start()

        # プログレスバーの色を設定
        # print([self.tree.item(item, "values")[0] for item in self.tree.get_children()])
        # if "×" in [self.tree.item(item, "values")[0] for item in self.tree.get_children()]:
        #    self.progress_bar["style"] = "yellow.Horizontal.TProgressbar"
        # else:
        #    self.progress_bar["style"] = "green.Horizontal.TProgressbar"

    def calculate_checksum(self, file_path):
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()

    def check_file_exists(self, filename):
        params = {"filename": filename}
        response = requests.get("***", params=params)
        if response.status_code != 200:
            res = self.check_file_exists(filename)
        else:
            try:
                res = response.json().get('exists')
            except:
                res = self.check_file_exists(filename)
        
        return res

    def is_file_uploaded(self, file_name):
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[1] == file_name and self.tree.item(item, "values")[0] == "○":
                return True
        return False

    def get_result_and_message(self, file_name):
        # Find existing entry for the file name
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[1] == file_name:
                return self.tree.item(item, "values")[0], self.tree.item(item, "values")[3]
        return "", ""

    def update_table(self, file_name, result, message):
        item_id = None
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[1] == file_name:
                item_id = item
                break

        if item_id:
            self.tree.set(item_id, "結果", result)
            self.tree.set(item_id, "メッセージ", message)

    def increment_progress(self):
        self.upload_progress += 1
        self.progress_bar["value"] = int(self.upload_progress / len(self.file_list) * 100)
        self.root.update_idletasks()  # UIの更新
        if '×' in [self.tree.item(item, "values")[0] for item in self.tree.get_children()]:
            if '○' in [self.tree.item(item, "values")[0] for item in self.tree.get_children()]:
                self.progress_bar.config(style="yellow.Horizontal.TProgressbar")
            else:
                self.progress_bar.config(style="red.Horizontal.TProgressbar")
        else:
            self.progress_bar.config(style="green.Horizontal.TProgressbar")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileUploadApp(root)
    root.mainloop()
