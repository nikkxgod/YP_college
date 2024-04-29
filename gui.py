import tkinter as tk
window = tk.Tk()
window.geometry('1240x900')
window.resizable(False,False)

btn_input_url = tk.Button(window, text='Добавить событие')
btn_input_url.pack(expand=True,anchor='s',pady=40)




window.mainloop()
