from tkinter import *
import tkinter.messagebox as tmsg
from tkinter.filedialog import askdirectory
import pyttsx3
import speech_recognition as sr
import time
import webbrowser
import json
import os
import random

name = "Ally"
name = name.title()

data_filename = "Ally_Data.json"
history_filename = "Ally_History.txt"
tut_address = r"https://www.youtube.com/watch?v=v6YqIklzYZU"


def show(data):
    time_to_show = time.strftime("(%I:%M %p)")
    chat_history.configure(state=NORMAL)
    chat_history.insert(END, f"{time_to_show} {data}\n")
    chat_history.yview_pickplace(END)
    chat_history.update()
    chat_history.configure(state=DISABLED)
    with open(history_filename, "a") as f_obj:
        f_obj.write(f"{time.ctime()}  {data}\n")


def time_am_pm():

    pr_time = time.strftime('%I:%M %p')
    return pr_time


def get_date():
    mon_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    date_day = str(int(time.strftime("%d")))
    date_mon_num = int(time.strftime("%m"))
    date_mon = mon_dict[date_mon_num]
    date_year = str(int(time.strftime("%Y")))
    date_week_day = (time.strftime("%A"))
    today_date = f"{date_week_day} the {date_day}th of {date_mon} {date_year}"
    return today_date


def show_status(string):
    status_var.set(string)
    status_label.update()


def change_voice_code(event):
    global temp_voice_code

    voice_type = (voice_var.get())
    filename = data_filename
    try:
        with open(filename, "r") as f_obj:
            data_dict = json.load(f_obj)
            data_dict["voice"] = voice_type

        with open(filename, 'w') as file_object:
            json.dump(data_dict, file_object)

    except:
        with open(filename, "w") as file_obj:
            data_dict_new = {"voice": voice_type}
            json.dump(data_dict_new, file_obj)
    temp_voice_code = get_voice_code()
    tmsg.showinfo("Voice Changed", f"Voice is changed to {voice_type}.")


def get_voice_code():
    try:
        with open(data_filename) as file_obj:
            voice_type = json.load(file_obj)["voice"]
            voice_type = voice_type.lower()
            if voice_type == "male":
                voice_code = 0
            elif voice_type == "female":
                voice_code = 1
            else:
                voice_code = 1
    except:
        voice_code = 1

    return voice_code


def speak(string):
    """ This functions accepts a string and then speaks it. """
    # 1- female
    # 0 - male
    show_status("Busy")
    show(f"{name.title()} : {string}\n")
    engine = pyttsx3.init('sapi5')
    type_voices = engine.getProperty('voices')
    engine.setProperty('voice', type_voices[temp_voice_code].id)
    engine.say(string)
    engine.runAndWait()
    show_status("Ready now")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        show_status("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            show_status("Recognizing")
            query = r.recognize_google(audio, language='en-in')
            return_val = query

        except Exception as e:

            return_val = None

            if "recognition connection failed" in str(e):
                show_status("Connection Failed")
                speak("It seems that you are not connected to Internet. Please connect to internet and try again.")

            else:
                show_status("Not Recognized")
                speak("Sorry, I was not able to recognize what you just said. Please try again.")

    show_status("Ready now")
    return return_val


def wish_me():
    hour = int(time.strftime("%H"))
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 17:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak(f"I am {name}. I am your digital assistant. I am created by Swastik. Please tell me how may I help you.")


def search_google(query_raw):
    if query_raw == "":
        pass
    else:
        query_processed = query_raw.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={query_processed}")


def search_youtube(query_raw):
    if query_raw == "":
        pass
    else:
        query_processed = query_raw.replace(" ", "+")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query_processed}")


def search_wikipedia(query_raw):
    if query_raw == "":
        pass
    else:
        query_processed = query_raw.replace(" ", "_")
        webbrowser.open(f"https://en.wikipedia.org/wiki/{query_processed}")


def play_music():
    try:
        with open(data_filename) as file_obj:
            data_dict = json.load(file_obj)
            music_folder_path = rf"{data_dict['music_folder_path']}"
            songs = os.listdir(music_folder_path)
            random_song = random.choice(songs)
            speak("Playing...")
            os.startfile(os.path.join(music_folder_path, random_song))

    except PermissionError:
        speak("I am not able to access the folder you have selected. If you have selected the folder from your C drive please change it to some other drive.")

    except:
        speak("You have not selected any path for your music folder. Please make a separate folder for musics and select it first.")


def start_assistant(query):
    if query:
        query = query.lower()
        query = query.strip()

        # Logic for executing tasks

        if ("repeat" in query) and ("me" in query):
            to_speak = query[query.find("me") + 3:]
            to_speak = to_speak.strip()
            if to_speak == "":
                speak("You haven't said anything to repeat")
            else:
                speak(f"You Said - {to_speak}")

        elif "open wikipedia" in query:
            speak("Opening Wikipedia...")
            webbrowser.open("https://www.wikipedia.org/")

        elif ("search" in query) and ("google" in query):
            speak("Searching on Google...")
            search_query = query[query.find("google") + 7:]
            search_google(search_query)

        elif ("search" in query) and ("youtube" in query):
            speak("Searching on Youtube...")
            search_query = query[query.find("youtube") + 8:]
            search_youtube(search_query)

        elif "wikipedia" in query:
            if query == "wikipedia":
                speak("Opening Wikipedia...")
                webbrowser.open("https://www.wikipedia.org/")
            else:
                speak("Searching on Wikipedia...")
                search_query = query[query.find("wikipedia") + 10:]
                search_query = search_query.strip()
                if search_query == "":
                    search_query = query.replace("wikipedia", "")
                    search_query = search_query.strip()

                search_wikipedia(search_query)

        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com/")

        elif "open youtube" in query:
            speak("Opening youtube...")
            webbrowser.open("https://www.youtube.com/")



        elif ((("what" in query) or ("tell" in query) or ("what's" in query)) and ("time" in query)) or (
                query == "time"):
            speak(f"It is {time_am_pm()}")

        elif ((("what" in query) or ("tell" in query) or ("what's" in query) or ("today's" in query)) and (
                "date" in query)) or (query == "date"):
            speak(f"It is {get_date()}")

        elif (("what is your name" in query) or (("tell" in query) and "your name" in query) or (
                "who are you" in query) or (("what's" in query) and ("name" in query))) or query == name.lower():
            speak(f"I am {name}. I am your digital assistant. Please tell me how may I help you...")

        elif ((query == "hi") or (query == "hello")) and (name.lower() in query):
            speak(f"I am {name}. I am your assistant. Tell me how can I help you...")

        elif ("play" in query) and (("music" in query) or ("song" in query)):
            play_music()

        elif (('close' in query) or('quit' in query) or ('exit' in query)) and (('yourself' in query) or (name.lower() in query)):
            exit_it()

        else:
            speak("Searching on Google...")
            search_google(query)


def voice_command_query(event):
    query = take_command()
    if not (query is None) or (query == ""):
        show(f"You : {query}")
        start_assistant(query)


def written_command_query(event):
    query = command_var.get()
    query = query.strip()
    command_pad.delete(0, END)
    if not (query == ""):
        show(f"You : {query}")
        start_assistant(query)
    else:
        pass


def give_space(event):
    text_entered = command_var.get()
    try:
        if text_entered[0] != ' ':
            command_pad.insert(0, ' ')
    except:
        pass


def exit_it():
    root.destroy()


def add_music_path():
    music_path = rf"{askdirectory()}"

    try:
        with open(data_filename) as file_obj:
            data_dict = json.load(file_obj)
            data_dict["music_folder_path"] = music_path

        with open(data_filename, 'w') as f_obj:
            json.dump(data_dict, f_obj)

    except:
        data_dict = {"voice": "Female", "music_folder_path": music_path}
        with open(data_filename, 'w') as f_obj:
            json.dump(data_dict, f_obj)

    tmsg.showinfo('Path Added/Changed', f'Music path added/changed.\n\nCurrent Music Path\n{music_path}')


def help_user():
    tmsg.showinfo("Help", f"This is a desktop assisant named {name}.\nYou can use it to make your work easy.\nTo know more about it, watch the tutorial.")


def open_tut():
    webbrowser.open(tut_address)


def open_about():
    message = f"{name} desktop assistant version 1.0\n\nBuilt on May 17 2020\n\nBuilt by Swastik.\n\nOpen Source Software."
    tmsg.showinfo('About', message)


def show_history():
    try:
        history_file = history_filename
        with open(history_file) as f_obj:
            history = f_obj.read()

        if history.strip() == "":
            tmsg.showinfo('History Empty', f'No history found.')

        else:
            chat_history.delete(0.0, END)
            chat_history.configure(state=NORMAL)
            chat_history.insert(END, history)
            chat_history.yview_pickplace(END)
            chat_history.update()
            chat_history.configure(state=DISABLED)

    except:
        tmsg.showinfo('History Empty', f'No history found.')


def clear_history():
    with open(history_filename, 'w') as file_object:
        file_object.close()

    chat_history.configure(state=NORMAL)
    chat_history.delete(0.0, END)
    chat_history.configure(state=DISABLED)

    tmsg.showinfo('History Cleared', 'History is cleared.')


win_color = '#80ff00'
temp_voice_code = get_voice_code()

root = Tk()
root.geometry('650x659+10+0')
root.resizable(0, 0)

root.title(f'{name.title()} Desktop Assistant')

title_label = Label(root, text=f"{name.title()} Desktop Assistant", font="calibri 40 bold",
                    bg=win_color, fg="blue", padx=2, pady=20)
title_label.pack(side=TOP, fill=X)

voice_frame = Frame(root, borderwidth=6, bg=win_color)
voice_frame.pack(fill=X)

Label(voice_frame, text=f"{name}'s Voice", bg=win_color, padx=20,
      font="calibri 12").grid(row=0, column=0)

voices = ["Male", "Female"]
voice_var = StringVar()
voice_var.set(voices[get_voice_code()])

column_num = 0
for voice in voices:
    column_num += 1
    Radiobutton(voice_frame, text=voice, padx=14, variable=voice_var, bg=win_color,
                value=voice).grid(row=0, column=column_num)

ch_voice_btn = Button(voice_frame, text="Change Voice", bd=2, fg='black', bg='white', font='aerial 10',
                      relief=RAISED)
ch_voice_btn.grid(row=0, column=3)
ch_voice_btn.bind('<ButtonRelease-1>', change_voice_code)

write_frame = Frame(root, borderwidth=6, bg=win_color)
write_frame.pack(side=TOP, fill=X)

Label(write_frame, text="Write Command : ", font='aeriel 20 bold',
      bg=win_color).grid(row=0, column=0, padx=20)

command_var = StringVar()
command_pad = Entry(write_frame, text=command_var, font='aerial 20 bold', relief=SUNKEN, bd=2, bg='white')
command_pad.grid(row=0, column=1)
command_pad.bind('<Return>', written_command_query)
command_pad.bind('<Key>', give_space)

search_button = Button(write_frame, text="Send", bd=2, fg='black', bg='white', font='aerial 15 bold',
                       relief=RAISED)
search_button.grid(row=1, column=1, pady=7)
search_button.bind('<ButtonRelease-1>', written_command_query)

mic_frame = Frame(root, borderwidth=6, bg=win_color)
mic_frame.pack(side=TOP, fill=X)

command_button = Button(mic_frame, text="Speak Command", bd=2, fg='black', bg='white', font='aerial 15 bold',
                        relief=RAISED)
command_button.pack(pady=5)
command_button.bind('<ButtonRelease-1>', voice_command_query)

status_var = StringVar()
status_var.set("  ")
status_label = Label(mic_frame, textvariable=status_var, font='calibri 15', bg=win_color, fg="black")
status_label.pack(pady=5)

history_frame = Frame(root, borderwidth=6, bg=win_color)
history_frame.pack(side=TOP, fill=X)

chat_scroll = Scrollbar(history_frame)
chat_scroll.pack(side=RIGHT, fill=Y)

chat_history = Text(history_frame, font='calibri 20 bold', padx=8,
                    yscrollcommand=chat_scroll.set, height=7, width=43)
chat_history.configure(state=DISABLED)
chat_history.pack()
chat_scroll.config(command=chat_history.yview)

exit_frame = Frame(root, borderwidth=6, bg=win_color)
exit_frame.pack(side=TOP, fill=X)
exit_btn = Button(exit_frame, text="Exit", bd=2, fg='black', bg='white', font='aerial 15 bold',
                  relief=RAISED, command=exit_it)
exit_btn.pack()

main_menu = Menu(root)

option_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Options', menu=option_menu)
option_menu.add_command(label='Add/Change Music Path', command=add_music_path)
option_menu.add_command(label='Show History', command=show_history)
option_menu.add_command(label='Clear History', command=clear_history)

help_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='Help', command=help_user)
help_menu.add_command(label='Getting Started', command=open_tut)
help_menu.add_command(label='Watch Tutorial', command=open_tut)
help_menu.add_command(label='About', command=open_about)

root.config(menu=main_menu)

wish_me()
command_pad.focus()

root.mainloop()
