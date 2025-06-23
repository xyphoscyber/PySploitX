import sounddevice as sd
from scipy.io.wavfile import write
from core.base_module import BaseModule
from rich.console import Console

class MicRecorder(BaseModule):
    """Records audio from the microphone."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DURATION': [10, 'The recording duration in seconds.'],
            'OUTPUT_FILE': ['recording.wav', 'The output WAV file name.'],
            'SAMPLE_RATE': [44100, 'The sample rate for the recording.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the microphone recording.
        """
        duration = int(options.get('DURATION'))
        output_file = options.get('OUTPUT_FILE')
        fs = int(options.get('SAMPLE_RATE'))
        console = Console()

        console.print(f"[*] Starting microphone recording for {duration} seconds...")

        try:
            # Record audio
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
            sd.wait()  # Wait until recording is finished

            # Save as WAV file
            write(output_file, fs, recording)
            
            console.print(f"[bold green][+] Recording saved successfully to {output_file}[/bold green]")

        except sd.PortAudioError as e:
            console.print(f"[!] Audio device error: {e}", style="bold red")
            console.print("[!] No input device found or it's in use.", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")