#YouTube to MP3 Convertor
import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import yt_dlp

# Function to update the progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        # Calculate the percentage of download completed
        percent = float(d['_percent_str'].strip('%'))
        progress_bar['value'] = percent
        root.update_idletasks()

    elif d['status'] == 'finished':
        # Reset the progress bar when finished
        progress_bar['value'] = 100
        root.update_idletasks()

# Function to download and extract audio using yt-dlp with selected bitrate
def download_audio():
    url = url_entry.get()

    try:
        # Get the directory to save the audio file
        download_path = filedialog.askdirectory()
        if not download_path:
            raise Exception("No folder selected.")

        # Get the selected bitrate from the dropdown
        selected_bitrate = bitrate_var.get()

        # Define yt-dlp options to download the best audio format and convert to MP3 with the selected bitrate
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': selected_bitrate,  # Use selected bitrate
            }],
            'progress_hooks': [progress_hook],  # Add progress hook
        }

        # Download the audio using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Show success message
        messagebox.showinfo("Success", f"Audio has been saved in MP3 format at: {download_path}")

    except Exception as e:
        # Show an error message
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to create the GUI
def create_gui():
    global url_entry, bitrate_var, progress_bar, root

    # Create the main window
    root = Tk()
    root.title("YouTube to MP3 Converter")
    root.geometry("450x350")
    root.config(bg="#2E8BC0")  # Background color

    # Create and place the URL label
    Label(root, text="YouTube Video URL:", bg="#2E8BC0", fg="white", font=("Helvetica", 12)).pack(pady=10)

    # Create and place the URL entry widget
    url_entry = Entry(root, width=50, font=("Helvetica", 12), bd=2, relief="sunken")
    url_entry.pack(pady=5)

    # Create and place the bitrate selection label
    Label(root, text="Select Audio Bitrate (kbps):", bg="#2E8BC0", fg="white", font=("Helvetica", 12)).pack(pady=10)

    # Bitrate selection dropdown
    bitrate_var = StringVar(root)
    bitrate_var.set("192")  # Set default bitrate to 192 kbps
    bitrate_options = ["32", "96", "128", "192", "256", "320"]
    bitrate_menu = OptionMenu(root, bitrate_var, *bitrate_options)
    bitrate_menu.config(font=("Helvetica", 12), bg="#F18F01", fg="white", bd=2, relief="raised")
    bitrate_menu.pack(pady=10)

    # Create and place the download button
    download_button = Button(root, text="Download and Convert", command=download_audio, bg="#F18F01", fg="white",
                             font=("Helvetica", 12, "bold"), relief="raised", bd=3)
    download_button.pack(pady=20)

    # Create a progress bar widget
    progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
    progress_bar.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()

# Run the GUI application
create_gui()
