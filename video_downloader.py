import os
import time
# For proper pyktok operation install those: pip install browser-cookie3, pip install pandas, pip install TikTokApi
import pyktok
import read_more
import instaloader
import tkinter as tk
#
from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip


def download_video():
    try:
        # Update text label
        info_label.config(text='Downloading video...')
        # Refresh frame to update text
        frame.update()
        # Get url from entry an assign it to var
        url = url_entry.get()

        # If elif statement to select the appropriate library to download the video
        if 'youtu' in url:
            try:
                # Get value from Checkbutton 0 for off 1 for on
                if high_resolution.get() == 0:
                    youtube_video = YouTube(url)
                    # Pick (just in theory, pytube at this moment is broken, gets 360p) the highest resolution video
                    save_youtube_video = youtube_video.streams.get_highest_resolution()
                    # Save video with original title
                    save_youtube_video.download()

                elif high_resolution.get() == 1:
                    youtube_video = YouTube(url)
                    # Pick the highest available resolution (Unfortunately, it will be downloaded without sound)
                    save_youtube_video = youtube_video.streams.filter(adaptive=True).filter(
                        mime_type='video/webm').first()
                    # Save video as video.mp4
                    save_youtube_video.download(filename='video.mp4')

                    youtube_audio = YouTube(url)
                    # Pick audio
                    save_youtube_video = youtube_audio.streams.get_audio_only()
                    # Save audio as audio.mp3
                    save_youtube_video.download(filename='audio.mp3')

                    # Update text label
                    info_label.config(text='Download complete!')
                    # Refresh frame to update text
                    frame.update()

                    # Sleep for 2 second to give the user a chance to see information about the success of downloading
                    # both files
                    time.sleep(2)
                    # Update text label about merging files
                    info_label.config(text='Merging files. Please wait...')
                    # Refresh frame to update text
                    frame.update()

                    # Replace with your MP3 file path
                    audio_file = 'audio.mp3'
                    # Replace with your MP4 file path
                    video_file = 'video.mp4'
                    # Desired output file name sourced from YouTube title
                    output_file = f'{youtube_video.title}.mp4'

                    # This is slow...
                    # Load the video file
                    video_clip = VideoFileClip(video_file)

                    # Load the audio file
                    audio_clip = AudioFileClip(audio_file)
                    # Set the audio of the video clip to the audio clip
                    final_video = video_clip.set_audio(audio_clip)
                    # Write the result to a file
                    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

                    # Close the clips to free up resources
                    video_clip.close()
                    audio_clip.close()

                    # Remove files used to make hi-res video
                    os.remove(audio_file)
                    os.remove(video_file)

                info_label.config(text='Download complete!')
            # Handle exceptions and prevent program crashes, also give feedback
            except Exception as e:
                info_label.config(text=f'An error occurred: {e}')
                print(e)
        elif 'instagram' in url:
            ig = instaloader.Instaloader()
            shortcode = url.split('/')[-2]
            try:
                # Load the post from instagram
                post = instaloader.Post.from_shortcode(ig.context, shortcode)

                # Check if the post has a video
                if post.is_video:

                    # Construct the filename for the video
                    video_filename = f'{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_{shortcode}'

                    # Download the video only
                    ig.download_pic(video_filename, post.video_url, post.date_utc)
                    info_label.config(text='Video downloaded successfully')
                else:
                    info_label.config(text='The post does not contain a video')

            # Handle exceptions and prevent program crashes, also give feedback
            except instaloader.exceptions.InstaloaderException as e:
                info_label.config(text=f'An error occurred: {e}')

        elif 'tiktok' in url:
            try:
                # If pyktok does not operate as expected, you may find it helpful to run the 'specify_browser' function.
                # 'specify_browser' takes as its sole argument a string representing a browser installed on your system,
                # e.g. "chrome," "firefox," "edge," etc.
                pyktok.save_tiktok(url, True)
                info_label.config(text='Video downloaded successfully')
            # Handle exceptions and prevent program crashes, also give feedback
            except Exception as e:
                info_label.config(text=f'An error occurred: {e}')
                print(e)
        # Give user info about invalid url
        else:
            info_label.config(text=f'An error occurred: Invalid url')

    # Handle exceptions and prevent program crashes, also give feedback
    except Exception as e:
        info_label.config(text=f'An error occurred: {e}')


def read():
    # Window with some information about program opened when clicked on 'Read more' button
    read_me_window = tk.Tk()
    read_me_window.geometry('550x300')
    read_me_window.resizable(False, False)
    read_me_window.config(background='#b37256')
    read_me_window.title('Read more')
    read_me_window_text = tk.Label(read_me_window, background='#b37256', foreground='#ffffff')
    read_me_window_text['text'] = read_more.read_more_text
    read_me_window_text.pack()
    read_me_window_close_button = tk.Button(read_me_window, text='Close', command=read_me_window.destroy,
                                            background='#ec9688', foreground='#ffffff', activebackground='#950714',
                                            activeforeground='#ffffff')
    read_me_window_close_button.pack()


root = tk.Tk()
root.title('Download video from Youtube, Instagram, TikTok')
root.geometry('700x380')
root.minsize(650, 380)
root.resizable(True, False)
root.config(background='#b37256')

# Create frame where all widgets will be placed
frame = tk.Frame(root, background='#b37256')
frame.pack()

# Create label
enter_url = tk.Label(frame, font=('Arial', 24), text='Enter URL:', background='#b37256', foreground='#ffffff')
enter_url.grid(row=0, column=0, pady=10)

# Create entry field to paste link to video
url_entry = tk.Entry(frame, width=40, font=('Arial', 20), background='#b0ae81', foreground='#ffffff')
url_entry.grid(row=1, column=0, pady=10)

# Create Download button to start the process
download_button = tk.Button(frame, text='Download', font=('Arial', 20), background='#ec9688', foreground='#ffffff',
                            activebackground='#950714', activeforeground='#ffffff', command=download_video)
download_button.grid(row=2, column=0, pady=10)

# Create label with no text, this will be updated depending on the stage, e.g. error or downloading
info_label = tk.Label(frame, font=('Arial', 24), text=' ', background='#b37256', foreground='#ffffff')
info_label.grid(row=3, column=0, pady=10)

# Create variable to pass value (0 or 1) into download_video() function
high_resolution = tk.IntVar()
# Create check button, selecting this will trigger downloading video+audio and merging them together
# in download_video() function
hi_res = tk.Checkbutton(frame, text='High Resolution Youtube\nWARNING! It may take a while!\nPlease read more',
                        background='#b37256', activebackground='#b37256',
                        activeforeground='#ffffff', variable=high_resolution)
hi_res.grid(row=4, column=0, pady=(20, 0))

# Create button to open new window with information triggered by read() function
read_button = tk.Button(frame, width=20, text='Read more', background='#ec9688', foreground='#ffffff',
                        activebackground='#950714', activeforeground='#ffffff', command=read)
read_button.grid(row=5, column=0, pady=5)

# Starts the program (create root window and everything inside it)
root.mainloop()
