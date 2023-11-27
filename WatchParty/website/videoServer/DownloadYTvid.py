'''
This file downloads a youtube video's audio and video data in mp3 and mp4 format via a youtube link
This is simply proof that this function works and it will be implemented
in the client and server files

This can be run by itself with a any youtube URL to be tested
'''



from moviepy.editor import VideoFileClip
from pytube import YouTube

def download_youtube_video(url, output_path):
    print("Video Downloader initiated...")
    #Create a YouTube object using the provided URL
    yt = YouTube(url)           
    #Get the stream with the highest resolution
    ys = yt.streams.get_highest_resolution()       

    #Download the video to the specified output path with the filename 'video.mp4'
    return ys.download(output_path, 'video.mp4')       
    



def extract_audio(video_path, audio_output_path):
    print("Extracing Audio from Video...")

    #Load the video file using VideofileClip
    video = VideoFileClip(video_path)
    #Get the audio component of the video
    audio = video.audio
    #Create a new audio file path with the filename 'videoAudio.wav'
    new_audio_path= audio_output_path+'videoAudio.wav'

    #Write the audio to the file path
    audio.write_audiofile(new_audio_path)

    #Return the path of the newly created audio file
    return new_audio_path

'''
This can be called to download the video natively with the youtube video in the youtube_url variable
This is not called in the web application this is simply for testing
'''
def main():

    youtube_url = 'https://www.youtube.com/watch?v=ssZWhJHGCRY'  # change video id here to test with other aoxF29RI2Bs
    video_output_path = 'WatchParty/website/Videos/'
    audio_output_path = 'WatchParty/website/Videos/'

    # Download YouTube video
    downloaded_video_path = download_youtube_video(youtube_url, video_output_path)
    print(downloaded_video_path)
    
    #extract_and_convert_audio(video_output_path, audio_output_path, )
    # Extract audio from video
    new_audio_path=extract_audio(downloaded_video_path, audio_output_path)
    print(new_audio_path)
    # Play the video (You can replace this with your video transmission logic)

     
    
#extract_audio('WatchParty/website/Videos/SampleVideo1.mp4', 'WatchParty/website/Videos/' )  #clever method of getting the audio from the sample video 
#extract_audio('WatchParty/website/Videos/video.mp4', 'WatchParty/website/Videos/' ) 
