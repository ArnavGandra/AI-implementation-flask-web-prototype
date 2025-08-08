#remove background sound from main video file
#enhance primary voice and remove rest
#import hugging face model
#use model on the file and remove 
#return result to user -- save it on a folder and send the path.

import subprocess
import os
from uuid import uuid4
from pathlib import Path
import torchaudio
import noisereduce as nr
import soundfile as sf

class AudioExtractorService:

    @staticmethod
    def extract_audio(video_path: str, output_dir: str = "outputs") -> str:

        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate unique filename for output audio
        base_filename = Path(video_path).stem
        audio_filename = f"{base_filename}_{uuid4().hex[:8]}.mp3"
        audio_path = os.path.join(output_dir, audio_filename)

        # FFmpeg command to extract audio
        command = [
            "ffmpeg",
            "-i", video_path,      # input file
            "-vn",                 # remove video stream
            "-q:a", "0",           # best audio quality
            "-map", "a",           # select audio stream only
            audio_path
        ]

        # Run the command
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return audio_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")




class AudioEnhancerService:
    def __init__(self):
        pass  # no model to load upfront

    @staticmethod
    def convert_mp3_to_wav(mp3_path: str) -> str:
        wav_path = mp3_path.replace(".mp3", ".wav")
        command = ["ffmpeg", "-y", "-i", mp3_path, wav_path]
        import subprocess
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return wav_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Conversion to WAV failed: {e.stderr.decode()}")

    def enhance_audio(self, wav_path: str, output_dir: str = "enhanced_outputs") -> str:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        audio, rate = sf.read(wav_path)
        reduced_noise = nr.reduce_noise(y=audio, sr=rate)

        output_path = os.path.join(output_dir, f"{Path(wav_path).stem}_enhanced.wav")
        sf.write(output_path, reduced_noise, rate)
        return output_path



if __name__ == "__main__":
    video_path = "/Users/family/Downloads/videoplayback.mp4"  # <--- Change this to your actual input path
    output_dir = "/Users/family/Documents"

    print("[1] Extracting audio...")
    audio_path = AudioExtractorService.extract_audio(video_path, output_dir)

    print("[2] Converting to WAV...")
    wav_path = AudioEnhancerService.convert_mp3_to_wav(audio_path)

    print("[3] Enhancing audio...")
    enhancer = AudioEnhancerService()
    enhanced_audio_path = enhancer.enhance_audio(wav_path, output_dir)

    print(f"\n✅ Enhanced audio saved at:\n{enhanced_audio_path}")