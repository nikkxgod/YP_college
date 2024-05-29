#TODO:
#норм вид придать
import numpy as np
import pymongo
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import Toplevel, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

window = tk.Tk()
window.geometry('420x885+0+0')
window.resizable(False, False)

def open_event(event_id):
    event = raybet_db.find_one({'_id': event_id})
    count_odds = len(event['odds'])
    x = range(count_odds)
    team_name1 = event['teams'][0]
    team_name2 = event['teams'][1]
    y_winner1 = []
    y_winner2 = []
    if event['round']=='bo3':
        y_map1_team1 = []
        y_map1_team2 = []
        y_map2_team1 = []
        y_map2_team2 = []
    
    for i in event['odds']:
        y_winner1.append(float(i['Winner'][team_name1]))
        y_winner2.append(float(i['Winner'][team_name2]))
        if event['round']=='bo3':
            y_map1_team1.append(float(i['Map 1'][team_name1]))
            y_map1_team2.append(float(i['Map 1'][team_name2]))
            y_map2_team1.append(float(i['Map 2'][team_name1]))
            y_map2_team2.append(float(i['Map 2'][team_name2]))

    new_window = Toplevel(window)
    new_window.geometry('1100x885+423+0')
    new_window.title(buttons[event_id]['name']['text'])
    new_window.resizable(0, 0)

    frame_chart = tk.Frame(new_window)
    frame_chart.pack(fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots()

    line_winner_team1, = ax.plot(x, y_winner1, label=team_name1)
    line_winner_team2, = ax.plot(x, y_winner2, label=team_name2)
    if event['round']=='bo3':
        line_map1_team1, = ax.plot(x, y_map1_team1, label=team_name1)
        line_map1_team2, = ax.plot(x, y_map1_team2, label=team_name2)
        line_map2_team1, = ax.plot(x, y_map2_team1, label=team_name1)
        line_map2_team2, = ax.plot(x, y_map2_team2, label=team_name2)

    ax.legend()
    if event['round']=='bo3':
        max_y = max(max(y_winner1), max(y_winner2), max(y_map1_team1), max(y_map1_team2), max(y_map2_team1), max(y_map2_team2))
    else: 
        max_y = max(max(y_winner1), max(y_winner2))
    ax.set_ylim(0, max_y)  # Устанавливаем ограничение для оси Y
    ax.autoscale()  # Автоматическое масштабирование графика
    ax.set_yticks(np.linspace(1, max_y, 50))
    plt.xticks([])
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def winner_line():
        if line_winner_team1.get_visible():
            line_winner_team1.set_visible(False)
            line_winner_team2.set_visible(False)
        else:
            line_winner_team1.set_visible(True)
            line_winner_team2.set_visible(True)
        fig.canvas.draw()
        
    def map1_line():
        if line_map1_team1.get_visible():
            line_map1_team1.set_visible(False)
            line_map1_team2.set_visible(False)
        else:
            line_map1_team1.set_visible(True)
            line_map1_team2.set_visible(True)
        fig.canvas.draw()
        
    def map2_line():
        if line_map2_team1.get_visible():
            line_map2_team1.set_visible(False)
            line_map2_team2.set_visible(False)
        else:
            line_map2_team1.set_visible(True)
            line_map2_team2.set_visible(True)
        fig.canvas.draw()
        
    winner_button = tk.Button(new_window, text="Winner", command=winner_line)
    winner_button.pack(side='left', padx=5)
    if event['round']=='bo3':
        map1_button = tk.Button(new_window, text="Map 1", command=map1_line)
        map1_button.pack(side='left', padx=5)
        map2_button = tk.Button(new_window, text="Map 2", command=map2_line)
        map2_button.pack(side='left', padx=5)
    last_update_label = tk.Label(new_window, text=f'Last update: {event['odds'][-1]['Date time'].split()[1]}')
    last_update_label.pack(side='left',padx=20)
    toolbar = NavigationToolbar2Tk(canvas, new_window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)




def add_event():
    global buttons
    for event_id, button_data in buttons.items():
        button_data['name'].destroy()
        button_data['delete'].destroy()
    buttons.clear()
    i = 0
    events = raybet_db.find()
    sorted_events = sorted(events, key=lambda x: x['start_time'])
    for event in sorted_events:
        event_id = event['_id']
        buttons[event_id] = {}
        buttons[event_id]['name'] = tk.Button(frame_main, text=f"{event['match_name']} {str(event['start_time']).split()[1][:5]}", width=45, command=lambda event_id=event_id: open_event(event_id),bg='#FFDAB9')
        buttons[event_id]['delete'] = tk.Button(frame_main, image=delete_image, command=lambda event_id=event_id: delete_event(event_id),bg='#FFDAB9')
        buttons[event_id]['name'].place(x=58, y=i * 27)
        buttons[event_id]['delete'].place(x=386, y=i * 27)
        i += 1

def delete_event(event_id):
    urls_db.delete_one({'_id': event_id})
    raybet_db.delete_one({'_id': event_id})
    buttons[event_id]['name'].destroy()
    buttons[event_id]['delete'].destroy()
    del buttons[event_id]


def add_to_bd():
    global input_url
    url = input_url.get()
    if (url[:24]=='https://rbvn3.com/match/') and (url[24:].isdigit()==True) and (len(url[24:])==8):
        id = int(url.split('/')[-1])
        if raybet_db.find_one({'_id':int(id)})==None:
            urls_db.insert_one({'_id': id, 'url': url})
            input_url.delete(0, 'end')
            messagebox.showinfo("Уведомление", f"Событие добавится через {raybet_db.count_documents({})+2*2}c. Нажмите кнопку обновить")
        else:
            messagebox.showinfo("Уведомление", f"Событие уже добавлено")
    else:
        messagebox.showinfo("Уведомление", f"Некорректная ссылка")
        

def add_url_btn_click():
    input_label.place(x=155, y=5)
    input_url.place(x=130, y=30)
    add_to_bd_button.place(x=200, y=54)
    add_url_btn.place_forget()

db_client = pymongo.MongoClient("mongodb://localhost:27017")
project_db = db_client.project
urls_db = project_db.urls
raybet_db = project_db.raybet

frame_main = tk.Frame(window, width=1240, height=800, pady=20,bg='#000080')
frame_buttons = tk.Frame(window, width=1240, height=100, bg='#000080', pady=5)

input_url = tk.Entry(frame_buttons, width=35)
add_url_btn = tk.Button(frame_buttons, text='Добавить событие', bg='#FFDAB9',command=add_url_btn_click)
input_label = tk.Label(frame_buttons, text='Вставьте ссылку на событие',bg='#FFDAB9')
add_to_bd_button = tk.Button(frame_buttons, text='Добавить', command=add_to_bd,bg='#FFDAB9')
refresh_image = tk.PhotoImage(file='refresh.png')
refresh_button = tk.Button(image=refresh_image, command=add_event,bg='#FFDAB9').place(x=10, y=20)
delete_image = tk.PhotoImage(file='delete.png', height=20)

buttons = {}

frame_main.place(x=0,y=0)
frame_buttons.place(x=0, y=800)
add_url_btn.place(x=155, y=30)

add_event()
window.mainloop()
