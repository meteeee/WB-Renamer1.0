import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Menu
import json
import os
import logging

logging.basicConfig(filename='rename_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

config_file = "app_config.json"
current_lang = "TR"

def load_config():
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"prefix": "WB0", "suffix": "200150", "start_number": 0, "file_types": "*.*"}

def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f)
    messagebox.showinfo(lang[current_lang]["settings_saved"], lang[current_lang]["settings_saved"])

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_path.set(directory)
        rename_button.config(state=tk.NORMAL)
    else:
        rename_button.config(state=tk.DISABLED)

def start_renaming():
    directory = directory_path.get()
    start_number = int(start_number_entry.get())
    prefix = prefix_entry.get()
    suffix = suffix_entry.get()
    file_types = file_types_entry.get()
    if not directory:
        messagebox.showwarning(lang[current_lang]["warning_select_folder"], lang[current_lang]["warning_select_folder"])
        return
    num_renamed = rename_files_in_directory(directory, start_number, prefix, suffix, file_types, output_text)
    if num_renamed > 0:
        config = {"prefix": prefix, "suffix": suffix, "start_number": start_number + num_renamed, "file_types": file_types}
        save_config(config)

def rename_files_in_directory(directory_path, start_number, prefix, suffix, file_types, output_text):
    current_number = start_number
    renamed_files = 0
    files = filter_files(directory_path, file_types)
    for file in sorted(files):
        try:
            new_filename = f"{prefix}{current_number}{suffix}{os.path.splitext(file)[-1]}"
            old_file_path = os.path.join(directory_path, file)
            new_file_path = os.path.join(directory_path, new_filename)
            os.rename(old_file_path, new_file_path)
            output_text.insert(tk.END, f"'{file}' {lang[current_lang]['success']} '{new_filename}'.\n")
            logging.info(f"'{file}' to '{new_filename}'")
            current_number += 1
            renamed_files += 1
        except Exception as e:
            logging.error(f"Error renaming {file}: {e}")
            continue
    messagebox.showinfo(lang[current_lang]["success"], f"{lang[current_lang]['success']} {renamed_files}")
    return current_number - start_number

def filter_files(directory, file_types):
    if file_types == "*.*":
        return os.listdir(directory)
    else:
        return [f for f in os.listdir(directory) if any(f.endswith(ext) for ext in file_types.split(";"))]

def switch_language():
    global current_lang
    current_lang = "EN" if current_lang == "TR" else "TR"
    update_ui_texts()

def update_ui_texts():
    file_menu.entryconfig(0, label=lang[current_lang]["select_folder"])
    file_menu.entryconfig(2, label=lang[current_lang]["exit"])
    help_menu.entryconfig(0, label=lang[current_lang]["how_to_use_menu"])
    help_menu.entryconfig(1, label=lang[current_lang]["about_menu"])
    rename_button.config(text=lang[current_lang]["rename_button"])
    prefix_label.config(text=lang[current_lang]["prefix_label"])
    start_number_label.config(text=lang[current_lang]["start_number_label"])
    suffix_label.config(text=lang[current_lang]["suffix_label"])
    file_types_label.config(text=lang[current_lang]["file_types_label"])
    language_button.config(text=lang[current_lang]["language_switch"])
    root.title("WB Renamer v1.0")

def about_app_command():
    messagebox.showinfo(lang[current_lang]["about_menu"], lang[current_lang]["about"])

def how_to_use_command():
    messagebox.showinfo(lang[current_lang]["how_to_use_menu"], lang[current_lang]["how_to_use"])


lang = {
    "EN": {
        "settings_saved": "Settings successfully saved",
        "about": """
WB Renamer v1.0
---------------
This tool is designed for efficiently renaming files in bulk, adhering to specified naming conventions.

Developed by Mete Avcı, it allows for customizable prefixes, suffixes, and sequential numbering.

For support or feedback:
Contact: Mete Avcı - metheus@yandex.com
GitHub: https://github.com/meteeee
""",
        "how_to_use": """
1. Open the application and navigate to the 'File' menu at the top.
2. Click 'Select Folder' to choose the directory containing the files you want to rename.
3. In the provided fields, enter the desired:
   - 'Prefix': A string that will be added to the start of each file name.
   - 'Start Number': The starting number for sequentially numbered files.
   - 'Suffix': A string that will be added to the end of each file name, before the file extension.
4. In the 'File Types' field, enter the extensions of the files you want to rename (e.g., .txt;.jpg). 
   Leave this field as is (*.*) if you do not need to specify certain file types.
5. Press the 'Rename' button to start the renaming process.
""",
        "success": "Successfully renamed",
        "error": "Error",
        "warning_select_folder": "Please select a folder.",
        "file_menu": "File",
        "select_folder": "Select Folder",
        "exit": "Exit",
        "help_menu": "Help",
        "how_to_use_menu": "How to Use",
        "about_menu": "About",
        "rename_button": "Rename",
        "prefix_label": "Prefix:",
        "start_number_label": "Start Number:",
        "suffix_label": "Suffix:",
        "file_types_label": "File Types (.txt;.jpg):",
        "language_switch": "🇺🇸"
    },
    "TR": {
        "settings_saved": "Ayarlar başarıyla kaydedildi",
        "about": """
WB Renamer v1.0
---------------
Bu araç, belirli adlandırma kurallarına uygun olarak dosyaları toplu bir şekilde yeniden adlandırmak için tasarlanmıştır.

Mete Avcı tarafından geliştirilmiş olup, özelleştirilebilir önekler, sonekler ve ardışık numaralandırma seçenekleri sağlar.

Destek veya geri bildirim için:
İletişim: Mete Avcı - metheus@yandex.com
GitHub: https://github.com/meteeee""",
        "how_to_use": """
1. Uygulamayı açın ve üst kısımdaki 'Dosya' menüsüne gidin.
2. 'Klasör Seç' seçeneğine tıklayarak yeniden adlandırmak istediğiniz dosyaların bulunduğu dizini seçin.
3. İlgili alanlara istenilen bilgileri girin:
   - 'Önek': Her dosya adının başına eklenecek metin.
   - 'Başlangıç Sayısı': Ardışık numaralı dosyalar için başlangıç numarası.
   - 'Sonek': Dosya adının sonuna, dosya uzantısından önce eklenecek metin.
4. 'Dosya Tipleri' alanına, yeniden adlandırmak istediğiniz dosyaların uzantılarını girin (örn., .txt;.jpg).
   Belirli dosya türlerini belirtmeniz gerekmiyorsa bu alanı olduğu gibi bırakın (*.*) .
5. Yeniden adlandırma işlemini başlatmak için 'Yeniden Adlandır' butonuna basın.
"""
,
        "success": "Başarıyla yeniden adlandırıldı",
        "error": "Hata",
        "warning_select_folder": "Lütfen bir klasör seçin.",
        "file_menu": "Dosya",
        "select_folder": "Klasör Seç",
        "exit": "Çıkış",
        "help_menu": "Yardım",
        "how_to_use_menu": "Nasıl Kullanılır",
        "about_menu": "Hakkında",
        "rename_button": "Yeniden Adlandır",
        "prefix_label": "Önek:",
        "start_number_label": "Başlangıç Sayısı:",
        "suffix_label": "Sonek:",
        "file_types_label": "Dosya Tipleri (.txt;.jpg):",
        "language_switch": "🇹🇷"
    }
}

def load_config():
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"prefix": "WB0", "suffix": "200150", "start_number": 0, "file_types": "*.*"}

def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f)
    messagebox.showinfo(lang[current_lang]["settings_saved"], lang[current_lang]["settings_saved"])

def switch_language():
    global current_lang
    current_lang = "EN" if current_lang == "TR" else "TR"
    update_ui_texts()

def update_ui_texts():
    file_menu.entryconfig(0, label=lang[current_lang]["select_folder"])
    file_menu.entryconfig(1, label=lang[current_lang]["exit"])
    help_menu.entryconfig(0, label=lang[current_lang]["how_to_use_menu"])
    help_menu.entryconfig(1, label=lang[current_lang]["about_menu"])
    rename_button.config(text=lang[current_lang]["rename_button"])
    prefix_label.config(text=lang[current_lang]["prefix_label"])
    start_number_label.config(text=lang[current_lang]["start_number_label"])
    suffix_label.config(text=lang[current_lang]["suffix_label"])
    file_types_label.config(text=lang[current_lang]["file_types_label"])
    language_button.config(text=lang[current_lang]["language_switch"])
    root.title("WB Renamer v1.0")

def about_app_command():
    messagebox.showinfo(lang[current_lang]["about_menu"], lang[current_lang]["about"])

def how_to_use_command():
    messagebox.showinfo(lang[current_lang]["how_to_use_menu"], lang[current_lang]["how_to_use"])

root = tk.Tk()
root.title("WB Renamer v1.0")
# root.iconbitmap('path_to_your_icon.ico') # Uncomment and set the path to your icon file.

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=lang[current_lang]["file_menu"], menu=file_menu)
file_menu.add_command(label=lang[current_lang]["select_folder"], command=select_directory)
file_menu.add_command(label=lang[current_lang]["exit"], command=root.quit)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=lang[current_lang]["help_menu"], menu=help_menu)
help_menu.add_command(label=lang[current_lang]["how_to_use_menu"], command=how_to_use_command)
help_menu.add_command(label=lang[current_lang]["about_menu"], command=about_app_command)


directory_path = tk.StringVar()
start_number = tk.IntVar(value=load_config()["start_number"])
prefix_var = tk.StringVar(value=load_config()["prefix"])
suffix_var = tk.StringVar(value=load_config()["suffix"])
file_types_var = tk.StringVar(value=load_config().get("file_types", "*.*"))

prefix_label = tk.Label(root, text=lang[current_lang]["prefix_label"])
prefix_label.pack(padx=10, pady=(10,0))
prefix_entry = tk.Entry(root, textvariable=prefix_var)
prefix_entry.pack(padx=10, pady=(0,5))

start_number_label = tk.Label(root, text=lang[current_lang]["start_number_label"])
start_number_label.pack(padx=10)
start_number_entry = tk.Entry(root, textvariable=start_number)
start_number_entry.pack(padx=10, pady=(0,5))

suffix_label = tk.Label(root, text=lang[current_lang]["suffix_label"])
suffix_label.pack(padx=10)
suffix_entry = tk.Entry(root, textvariable=suffix_var)
suffix_entry.pack(padx=10, pady=(0,10))

file_types_label = tk.Label(root, text=lang[current_lang]["file_types_label"])
file_types_label.pack(padx=10)
file_types_entry = tk.Entry(root, textvariable=file_types_var)
file_types_entry.pack(padx=10, pady=(0,10))

rename_button = tk.Button(root, text=lang[current_lang]["rename_button"], command=lambda: start_renaming())
rename_button.pack(padx=10, pady=(0,10))

output_text = scrolledtext.ScrolledText(root, height=10)
output_text.pack(padx=10, pady=(0,10))

language_button = tk.Button(root, text=lang[current_lang]["language_switch"], command=switch_language, font=("Arial", 14))
language_button.pack(side=tk.BOTTOM, fill=tk.X)

update_ui_texts()

root.mainloop()