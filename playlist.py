# Import Required Modules 
from tkinter import *
from pyyoutube import Api 
from pytube import YouTube 
from threading import Thread 
from tkinter import messagebox
import os

dirname = os.path.dirname(os.path.abspath(__file__))
destination = dirname + '/download/'
print(destination)

## Listing Code

from string import ascii_lowercase
import itertools

def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)

###     

  
def get_list_videos(): 
    global playlist_item_by_id 
    # Clear ListBox 
    list_box.delete(0, 'end') 
  
    # Create API Object 
    api = Api(api_key='AIzaSyDBmJnUkkVtzezNonTf38V2JgmkzweZRTM') 
  
    if "youtube" in playlistId.get(): 
        playlist_id = playlistId.get()[len( 
            "https://www.youtube.com/playlist?list="):] 
    else: 
        playlist_id = playlistId.get() 
  
    # Get list of video links 
    playlist_item_by_id = api.get_playlist_items( 
        playlist_id=playlist_id, count=None, return_json=True) 
  
    # Iterate through all video links and insert into listbox 
    for index, videoid in enumerate(playlist_item_by_id['items']): 
        list_box.insert( 
            END, f" {str(index+1)}. {videoid['contentDetails']['videoId']}") 
  
    download_start.config(state=NORMAL) 
  
  
def threading(): 
    # Call download_videos function 
    t1 = Thread(target=download_videos) 
    t1.start() 
  
  
def download_videos(): 
    download_start.config(state="disabled") 
    get_videos.config(state="disabled") 
  
    # Iterate through all selected videos 
    for i in list_box.curselection():

        letter_pref = next(itertools.islice(iter_all_strings(), i, None, None))

        videoid = playlist_item_by_id['items'][i]['contentDetails']['videoId'] 
  
        link = f"https://www.youtube.com/watch?v={videoid}"

        try:
  
            yt_obj = YouTube(link) 
            video = yt_obj.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=destination)

            base, ext = os.path.splitext(out_file) 
            # Select elements before and after the last '/'
            before_last_slash = base[:base.rfind('/')]
            after_last_slash = base[base.rfind('/') + 1:]
            new_name = before_last_slash + '/' + letter_pref + ' ' + after_last_slash + '.mp3'

            os.rename(out_file, new_name) 

        except Exception as e:

            print(e)
            
            continue

  
        # filters = yt_obj.streams.filter(progressive=True, file_extension='mp3') 
  
        # # download the highest quality video 
        # filters.get_highest_resolution().download() 
  
    messagebox.showinfo("Success", "Video Successfully downloaded") 
    download_start.config(state="normal") 
    get_videos.config(state="normal") 
  
  
# Create Object 
root = Tk() 
# Set geometry 
root.geometry('400x400') 
  
# Add Label 
Label(root, text="Youtube Playlist Downloader", 
      font="italic 15 bold").pack(pady=10) 
Label(root, text="Enter Playlist URL:-", font="italic 10").pack() 
  
# Add Entry box 
playlistId = Entry(root, width=60) 
playlistId.pack(pady=5) 
  
# Add Button 
get_videos = Button(root, text="Get Videos", command=get_list_videos) 
get_videos.pack(pady=10) 
  
# Add Scrollbar 
scrollbar = Scrollbar(root) 
scrollbar.pack(side=RIGHT, fill=BOTH) 
list_box = Listbox(root, selectmode="multiple") 
list_box.pack(expand=YES, fill="both") 
list_box.config(yscrollcommand=scrollbar.set) 
scrollbar.config(command=list_box.yview) 
  
download_start = Button(root, text="Download Start", 
                        command=threading, state=DISABLED) 
download_start.pack(pady=10) 
  
# Execute Tkinter 
root.mainloop() 