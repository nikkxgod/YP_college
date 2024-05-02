import pymongo
import tkinter as tk
window = tk.Tk()
window.geometry('1240x900')
window.resizable(False,False)
# https://rbvn3.com/match/37950057

#функции
def add_to_bd():
    global input_url
    global input_label
    global add_to_bd_button
    global add_url_btn
    url = input_url.get()
    id = int(url.split('/')[-1])
    urls_db.insert_one({
        '_id':id,
        'url':url
        })
    input_url.place_forget()
    input_label.place_forget()
    add_to_bd_button.place_forget()
    # add_url_btn = tk.Button(frame_buttons, text='Добавить событие',command=add_url_btn_click)
    add_url_btn.place(x=500,y=30)



def add_url_btn_click():
    global input_url
    global input_label
    global add_to_bd_button
    global add_url_btn
    add_url_btn.place_forget()
    input_label.place(x=500,y=5)
    input_url.place(x=475,y=30)
    add_to_bd_button.place(x=545,y=54)
    
# создал бд
db_client = pymongo.MongoClient("mongodb://localhost:27017")
project_db = db_client.project
urls_db = project_db.urls

#Слои
frame_main = tk.Frame(window, width=1100, height=800, bg='green',pady=50)
frame_buttons = tk.Frame(window, width=1100, height=100, bg='blue',pady=5)

#все переменные 
input_url = tk.Entry(frame_buttons,width=35)
add_url_btn = tk.Button(frame_buttons, text='Добавить событие',command=add_url_btn_click)
input_label = tk.Label(frame_buttons,text='Вставьте ссылку на событие')
add_to_bd_button = tk.Button(frame_buttons,text='Добавить',command=add_to_bd)

#начало
frame_main.place(x=70,y=0)
frame_buttons.place(x=70,y=800)
add_url_btn.place(x=500,y=30)



# input_url = tk.Entry()
# label_input_url = tk.Label(text='Вставьте ссылку')
# btn_input_url = tk.Button(window, text='Добавить событие', command=lambda:(btn_input_url.destroy(),input_url.pack(expand=True,anchor='s',pady=40),label_input_url.pack(expand=True,anchor='s',pady=40)))
# btn_input_url.pack(expand=True,anchor='s',pady=20)


window.mainloop()
