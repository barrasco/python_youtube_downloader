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
    args = sys.argv
    global output_folder
    if "--help" in args or "-?" in args:
        print("")
        print("#=================================================================================")
        print(f"{bcolors.HEADER} Youtube downloader (@Marduken 2021) {bcolors.ENDC}")
        print("#=================================================================================")
        print("* Parameters: ")
        print(f"{bcolors.WARNING}--video / -v url{bcolors.ENDC} : download video with url param")
        print(f"{bcolors.WARNING}--videos-file / -vf{bcolors.ENDC} : download all individual videos listed on 'videos.txt' file")
        print(f"{bcolors.WARNING}--playlists-file / -pf{bcolors.ENDC} : download all individual videos listed on all playlists listed on 'playlist.txt' file")
        print("#=================================================================================")
    elif "--playlist-file" in args or "-pf" in args:
        output_folder = output_folder + "\Playlists"
        lines = readFile("playlists.txt")        
        for line in lines:
            downYoutubePlaylist(line)
    elif "--videos-file" in args or "-vf" in args:
        lines = readFile("videos.txt")
        for line in lines:
            downYoutubeVideoByUrl(line)
    elif len(args) >= 3 and (args[1] == "--video" or args[1] == "-v"):
        line = args[2]
        downYoutubeVideoByUrl(line)
    else:
        print("Incorrect parameters! check help using --help or -? parameter")

if __name__ == "__main__":
    main()