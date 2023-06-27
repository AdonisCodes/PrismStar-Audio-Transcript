import subprocess

import pysrt
import whisper

# Set up the Whisper Transcribe instance
model = whisper.load_model("small")

# Function to write a Srt File, and return the path
def write_srt(result, index):
    # Write the Srt File
    print("Starting to Write the Srt File")
    subtitle_path = f"temp/{index}.srt"
    subs = pysrt.SubRipFile()
    segments = result["segments"]
    start_time = ""
    end_time = ""
    text = ""

    # Loop through the segments, and write the segments
    print("Looping over Transcript Segments...")
    for segment in segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        sub = pysrt.SubRipItem(
            index=len(subs) + 1,
            start=pysrt.SubRipTime(seconds=start_time),
            end=pysrt.SubRipTime(seconds=end_time),
            text=text,
        )
        subs.append(sub)

    # Save the Generated Srt File
    subs.append(pysrt.SubRipItem(index=len(subs) + 1, start=pysrt.SubRipTime(seconds=start_time),
                                 end=pysrt.SubRipTime(seconds=end_time), text=text, ))
    subs.save(subtitle_path, encoding="utf-8")

    # Return the path
    return subtitle_path

# Function to analyze the given Audio File and Extract the Transcript
def analyze_audio(path):
    # Analysing the audio
    print("Analyzing Audio")
    options = dict(beam_size=1, best_of=1)  # Set best_of to 1
    translate_options = dict(task="translate", **options)
    result = model.transcribe(path, **translate_options)
    return result


def video2mp3(video_file, output_ext="mp3"):
    # Getting the Video file name
    import os
    filename, ext = os.path.splitext(video_file)

    # Extract the Audio from the Video File
    print("Extracting audio from Video File...")
    subprocess.call(
        ["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    return f"{filename}.{output_ext}"


pat = video2mp3("temp/a.mp4")
# Analyzing the Audio
result = analyze_audio(pat)

# Creating the Srt File
subtitle_path = write_srt(result, 0)