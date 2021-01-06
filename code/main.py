import pygame
from tkinter import *
from tkinter import filedialog
import time
from mutagen.mp3 import MP3

root = Tk()
root.title('Chi MP3 Player')
# root.iconbitmap('logo.png')
root.geometry("500x450")  # 設定視窗大小

# Initialize Pygame Mixer
pygame.mixer.init()

# Grab Song Length Time info 歌曲時間軸
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000 #原本顯示毫秒,所以/1000
    time_format = time.strftime('%M:%S', time.gmtime(current_time)) #time format
    
    #先取得當前播放歌曲的資訊
    # current_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f'C:/Users/user/Desktop/project/mp3_player/mp3/audio/{song}.mp3'
    #取得整首歌曲長度using Mutagen
    song_mut = MP3(song) #load song
    song_length = song_mut.info.length
    song_length_format = time.strftime('%M:%S', time.gmtime(song_length)) #format
    
    status_bar.after(1000, play_time) #update time #顯示當前時間
    status_bar.config(text=f"{time_format}/{song_length_format}") 

# add song function
def add_song():
    song = filedialog.askopenfilename(
        initialdir='../audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
    # print(song)
    song = song.replace(
        "C:/Users/user/Desktop/project/mp3_player/mp3/audio/", "")
    song = song.replace(".mp3", "")
    # add song to listbox
    song_box.insert(END, song)


def add_many_songs():
    songs = filedialog.askopenfilenames(
        initialdir='../audio/', title="Choose many songs", filetypes=(("mp3 Files", "*.mp3"),))

    # Loop thru song list and replace directory info and mp3
    for song in songs:
        song = song.replace(
            "C:/Users/user/Desktop/project/mp3_player/mp3/audio/", "")
        song = song.replace(".mp3", "")
        # Insert into playlist
        song_box.insert(END, song)

# Play selected Song
def play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/user/Desktop/project/mp3_player/mp3/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # call the play_time function to get song length
    play_time()

def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)  # 停止後反白會消失

    #Clear The status_bar
    status_bar.config(text='')

# Create Global Pause Variable
global paused
paused = False
# Pause and Unpause The Current Song


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()  # Unpause
        paused = False
    else:
        pygame.mixer.music.pause()  # pause
        paused = True


def previous_song():
    previous_one = song_box.curselection()
    previous_one = previous_one[0] - 1
    song = song_box.get(previous_one)
    if song == "": #這樣才不會在最後一首又按上一首時報錯
        previous_one = 0
        song = song_box.get(previous_one)


    song = f'C:/Users/user/Desktop/project/mp3_player/mp3/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.selection_set(previous_one, last=None)
    song_box.activate(previous_one)

# play the next song in the playlist


def next_song():
    # 歌曲轉換的部分
    next_one = song_box.curselection()  # all songs are tuple numbers
    # print(next_one) #(0,) (1,) (2,) ...
    # print(next_one[0]) #擷取了tuple => 0,1,2...
    next_one = next_one[0] + 1  # add one
    song = song_box.get(next_one)  # get the name of song
    if song == "": #這樣才不會在最後一首又按下一首時報錯
        next_one = next_one - 1
        song = song_box.get(next_one)
    song = f'C:/Users/user/Desktop/project/mp3_player/mp3/audio/{song}.mp3' # 取得檔案位置
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)  # play new song

    # 選項的部分
    song_box.selection_clear(0, END)  # clear active bar in playlist listbox
    song_box.activate(next_one)  # active new song underline
    song_box.selection_set(next_one, last=None)  # active new song bar

def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()



# Create playlist box
# 黑色框框60px 字:白, 選取背景:灰 , selectforeground="purple"
song_box = Listbox(root, bg="black", fg="white",
                   width=60, selectbackground="gray")
song_box.pack(pady=20)  # margin 框框跟上面的距離20px


# define player control buttons Images =>插入圖片
back_btn_img = PhotoImage(file='../gui/back.png')
forward_btn_img = PhotoImage(file='../gui/forward.png')
play_btn_img = PhotoImage(file='../gui/play2.png')
pause_btn_img = PhotoImage(file='../gui/pause.png')
stop_btn_img = PhotoImage(file='../gui/stop2.png')

# Create player control frame =>開啟control功能
controls_frame = Frame(root)
controls_frame.pack()

# Create Player control buttons =>把img功能化
back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)  # borderwidth陰影
forward_btn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)  # command play => 實現播放功能
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_btn.grid(row=0, column=0)  # 圖片位置設定
forward_btn.grid(row=0, column=1)
play_btn.grid(row=0, column=2)
pause_btn.grid(row=0, column=3)
stop_btn.grid(row=0, column=4)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Song Menu => directory
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
add_song_menu.add_command(label="Add Many Song To Playlist", command=add_many_songs)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)


#Create Status Bar
status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E) #text留白,之後要用別的套件輸入時間軸, anchor字的位置:東
status_bar.pack(fill=X, side=BOTTOM, ipady=2) #ipady:框寬度


root.mainloop()
