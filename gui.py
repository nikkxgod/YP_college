import sqlite3
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
    # event = raybet_db.find_one({'_id': event_id})
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    Event  = cursor.execute("SELECT * FROM Match WHERE id = ?", (event_id,)).fetchone()
    unique_teams = cursor.execute("SELECT DISTINCT team FROM Odds WHERE match_id = ?", (event_id,)).fetchall()
    # count_odds = len(event['odds'])
    # x = range(count_odds)
    team_name1 = unique_teams[0][0]
    team_name2 = unique_teams[1][0]
    y_winner1 = []
    y_winner2 = []
    if Event[-1]=='bo3':
        y_map1_team1 = []
        y_map1_team2 = []
        y_map2_team1 = []
        y_map2_team2 = []
    
    w1 = cursor.execute("SELECT * FROM Odds WHERE match_id = ? AND team = ? AND bet_type = ?", (event_id,team_name1,'Winner',)).fetchall()
    for i in w1:
        y_winner1.append(i[3])
    w2 = cursor.execute("SELECT * FROM Odds WHERE match_id = ? AND team = ? AND bet_type = ?", (event_id,team_name2,'Winner',)).fetchall()
    for i in w2:
        y_winner2.append(i[3])
    if Event[-1]=='bo3':
    #     y_map1_team1.append(float(i['Map 1'][team_name1]))
        t1m1 = cursor.execute("SELECT * FROM Odds WHERE match_id = ? AND team = ? AND bet_type = ?", (event_id,team_name1,'Map 1',)).fetchall()
        for i in t1m1:
            y_map1_team1.append(i[3])
    #     y_map1_team2.append(float(i['Map 1'][team_name2]))
        t2m1 = cursor.execute("SELECT * FROM Odds WHERE match_id = ? AND team = ? AND bet_type = ?", (event_id,team_name2,'Map 1',)).fetchall()
        for i in t2m1:
            y_map1_team2.append(i[3])
    #     y_map2_team1.append(float(i['Map 2'][team_name1]))
        t1m2 = cursor.execute("SELECT * FROM Odds WHERE match_id = ? AND team = ? AND bet_type = ?", (event_id,team_name1,'Map 2',)).fetchall()
        for i in t1m2:
            y_map2_team1.append(i[3])

        t2m2 = cursor.execute("SELECT * FROM Odds WHERE match_id = ? AND team = ? AND bet_type = ?", (event_id,team_name2,'Map 2',)).fetchall()
        for i in t2m2:
            y_map2_team2.append(i[3])
    cursor.close
    new_window = Toplevel(window)
    new_window.geometry('1100x885+423+0')
    new_window.title(buttons[event_id]['name']['text'])
    new_window.resizable(0, 0)

    frame_chart = tk.Frame(new_window)
    frame_chart.pack(fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots()
    len_w1 = range(len(y_winner1))
    line_winner_team1, = ax.plot(len_w1, y_winner1, label=team_name1)
    len_w2 = range(len(y_winner2))
    line_winner_team2, = ax.plot(len_w2, y_winner2, label=team_name2)
    if Event[-1]=='bo3':
        len_t1m1 = range(len(y_map1_team1))
        line_map1_team1, = ax.plot(len_t1m1, y_map1_team1, label=team_name1)
        len_t2m1 = range(len(y_map1_team2))
        line_map1_team2, = ax.plot(len_t2m1, y_map1_team2, label=team_name2)
        len_t1m2 = range(len(y_map2_team1))
        line_map2_team1, = ax.plot(len_t1m2, y_map2_team1, label=team_name1)
        len_t2m2 = range(len(y_map2_team2))
        line_map2_team2, = ax.plot(len_t2m2, y_map2_team2, label=team_name2)

    ax.legend()
    if Event[-1]=='bo3':
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
        
    winner_button = tk.Button(new_window, text="Общая", command=winner_line)
    winner_button.pack(side='left', padx=5)
    if Event[-1]=='bo3':
        map1_button = tk.Button(new_window, text="Карта 1", command=map1_line)
        map1_button.pack(side='left', padx=5)
        map2_button = tk.Button(new_window, text="Карта 2", command=map2_line)
        map2_button.pack(side='left', padx=5)
    cursor = connection.cursor()
    last_datetime = cursor.execute("SELECT datetime FROM Odds WHERE match_id = ? ORDER BY datetime DESC LIMIT 1", 
    (event_id,)).fetchone()
    cursor.close()
    last_update_label = tk.Label(new_window, text=f'Последнее обновление: {last_datetime[0].split()[1]}')
    last_update_label.pack(side='left',padx=20)
    toolbar = NavigationToolbar2Tk(canvas, new_window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)




def add_event():
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    global buttons
    for event_id, button_data in buttons.items():
        button_data['name'].destroy()
        button_data['delete'].destroy()
    buttons.clear()
    i = 0
    events = cursor.execute("SELECT * FROM Match ORDER BY start_time ASC").fetchall()
    cursor.close()
    for event in events:
        a = event[0]
        event_id = a
        buttons[event_id] = {}
        buttons[event_id]['name'] = tk.Button(frame_main, text=f"{event[2]} {str(event[4]).split()[1][:5]}", width=45, command=lambda event_id=event_id: open_event(event_id))
        buttons[event_id]['delete'] = tk.Button(frame_main, image=delete_image, command=lambda event_id=event_id: delete_event(event_id))
        buttons[event_id]['name'].place(x=58, y=i * 27)
        buttons[event_id]['delete'].place(x=386, y=i * 27)
        i += 1

def delete_event(event_id):
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Match WHERE id = ?", (event_id,))
    cursor.execute("DELETE FROM Odds WHERE match_id = ?", (event_id,))
    cursor.execute("DELETE FROM Urls WHERE id = ?", (event_id,))
    connection.commit()
    cursor.close()
    buttons[event_id]['name'].destroy()
    buttons[event_id]['delete'].destroy()
    del buttons[event_id]



def add_to_bd():
    connection = sqlite3.connect("project.db")
    cursor = connection.cursor()
    global input_url
    url = input_url.get()
    if (url[:24]=='https://rbvn3.com/match/') and (url[24:].isdigit()==True) and (len(url[24:])==8):
        id = int(url.split('/')[-1])
        cursor.execute("SELECT id FROM Urls WHERE id = ?", (id,))
        match_exists = cursor.fetchone()
        if not match_exists:
            cursor.execute(""" INSERT INTO Urls (id, url) VALUES (?,?)""", (id, url))
            connection.commit()
            input_url.delete(0, 'end')
            cursor.close()
            messagebox.showinfo("Уведомление", f"Событие добавится через 5 c. Нажмите кнопку обновить")
        else:
            cursor.close()
            messagebox.showinfo("Уведомление", f"Событие уже добавлено")
    else:
        cursor.close()
        messagebox.showinfo("Уведомление", f"Некорректная ссылка")
        

def add_url_btn_click():
    input_label.place(x=155, y=5)
    input_url.place(x=130, y=30)
    add_to_bd_button.place(x=200, y=54)
    add_url_btn.place_forget()

# db_client = pymongo.MongoClient("mongodb://localhost:27017")
# project_db = db_client.project
# urls_db = project_db.urls
# raybet_db = project_db.raybet

frame_main = tk.Frame(window, width=1240, height=800, pady=20,bg='#ddeee8')
frame_buttons = tk.Frame(window, width=1240, height=100, pady=5,bg='#ddeee8')

input_url = tk.Entry(frame_buttons, width=35)
add_url_btn = tk.Button(frame_buttons, text='Добавить событие',command=add_url_btn_click)
input_label = tk.Label(frame_buttons, text='Вставьте ссылку на событие')
add_to_bd_button = tk.Button(frame_buttons, text='Добавить', command=add_to_bd)
refresh_image = tk.PhotoImage(file='refresh.png')
refresh_button = tk.Button(image=refresh_image, command=add_event).place(x=10, y=20)
delete_image = tk.PhotoImage(file='delete.png', height=20)

buttons = {}

frame_main.place(x=0,y=0)
frame_buttons.place(x=0, y=800)
add_url_btn.place(x=155, y=30)

add_event()
window.mainloop()
