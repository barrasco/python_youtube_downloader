import sys, string
from pytube.cli import on_progress
from pytube import YouTube
from pytube import Playlist
from pytube.helpers import target_directory

#also check : 
# https://stackoverflow.com/questions/14140495/how-to-capture-a-video-and-audio-in-python-from-a-camera-or-webcam
# https://github.com/JRodrigoF/AVrecordeR

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

output_folder = "Output"

def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

def complete_callback (self, str):
    print("====================================")
    print(f"{bcolors.OKGREEN}Download complete{bcolors.ENDC}:" + str)
    print("====================================")

def downYoutubeVideoByUrl(url:str):
    yt = YouTube(url,on_progress,complete_callback,None,True,True)
    downYoutubeVideo(yt)

def downYoutubeVideo(video:YouTube):
    video.streams.\
    filter(type='video', progressive=True, file_extension='mp4').\
    order_by('resolution').\
    desc().\
    first().\
    download(output_folder) 

def sanitize_text(t:str) -> str:
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in t if c in valid_chars)

def downYoutubePlaylist(url):
    global output_folder
    playlist = Playlist(url)
    output_folder = output_folder + "\\"+ sanitize_text(playlist.title)
    print(f"{bcolors.OKBLUE}Download Playlist: {bcolors.ENDC}" + playlist.title+"\n")
    for video in playlist.video_urls:
        downYoutubeVideoByUrl(video)

def main():
    args = sys.argv[1:]
    global output_folder
    if "--help" in args or "-?" in args:
        print("")
        print("--videos / -v : download all individual videos listed on videos.txt file")
        print("--playlists / -p : download all individual videos listed on all playlists listed on playlist.txt file")
    elif "--playlist" in args or "-p" in args:
        output_folder = output_folder + "\Playlists"
        lines = readFile("playlists.txt")        
        for line in lines:
            downYoutubePlaylist(line)
    else:
        lines = readFile("videos.txt")
        for line in lines:
            downYoutubeVideoByUrl(line)

if __name__ == "__main__":
    main()