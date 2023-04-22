import ffmpeg

print("hello")
# video_stream = ffmpeg.input('ELDEN RING – Overview Trailer.mp4')
# audio_stream = ffmpeg.input('Yours Is an Empty Hope (Instrumental).mp4')
# ffmpeg.output(audio_stream, video_stream, 'out.mp4').run()

video_path1 = './Input/Ivan Drago - The Siberian Express.mp4'
video_path2 = './Input/Transformers The Movie Unicron Medley (Remix).mp4'

input_video = ffmpeg.input(video_path1)
video_file = ffmpeg.probe(video_path1)
duration1 = float(ffmpeg.probe(video_path1)["format"]["duration"])
input_audio = ffmpeg.input(video_path2)
duration2 = float(ffmpeg.probe(video_path2)["format"]["duration"])

framerate_factor = duration2 / duration1
print("framerate_factor:" + str(framerate_factor))
# l1/l2 = x/1
# Set the framerate of the input stream so that length matches video2
input_video = input_video.filter('setpts', f'PTS*{framerate_factor}')
ffmpeg.concat(input_video, input_audio, v=1, a=1).output('./Output/evandrago_unicron.mp4').run()