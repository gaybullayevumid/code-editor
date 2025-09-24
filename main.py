import tkinter as tk
from tkinter import filedialog, messagebox

# Asosiy oynani yaratamiz
root = tk.Tk()
root.title("Python Code Editor - Dark Mode")
root.geometry("800x600")

# Dark mode ranglari
bg_color = "#1e1e1e"   # fon (Visual Studio Code kabi)
fg_color = "#ffffff"   # matn oq
menu_bg = "#2d2d2d"    # menyu fon
menu_fg = "#ffffff"    # menyu matn

# Matn maydoni (kod yozish uchun)
text_area = tk.Text(
    root,
    wrap="none",
    font=("Consolas", 12),
    bg=bg_color,
    fg=fg_color,
    insertbackground="white"  # kursor rangi oq
)
text_area.pack(fill="both", expand=True)

# Faylni saqlash funksiyasi
def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".py",
                                        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file:
        with open(file, "w") as f:
            f.write(text_area.get(1.0, tk.END))
        messagebox.showinfo("Saqlash", "Fayl muvaffaqiyatli saqlandi!")

# Fayl ochish funksiyasi
def open_file():
    file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file:
        with open(file, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())

# Menyu qo‘shamiz
menu_bar = tk.Menu(root, bg=menu_bg, fg=menu_fg, tearoff=0, activebackground="#007acc", activeforeground="white")
file_menu = tk.Menu(menu_bar, tearoff=0, bg=menu_bg, fg=menu_fg, activebackground="#007acc", activeforeground="white")

file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar, bg=bg_color)

root.mainloop()




