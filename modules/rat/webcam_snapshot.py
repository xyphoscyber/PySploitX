import cv2
from core.base_module import BaseModule
from rich.console import Console

class WebcamSnapshot(BaseModule):
    """Captures a snapshot from the default webcam."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'OUTPUT_FILE': ['snapshot.png', 'The filename to save the snapshot as.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the webcam snapshot capture.
        """
        output_file = options.get('OUTPUT_FILE')
        console = Console()

        console.print("[*] Attempting to access webcam...")

        try:
            # 0 is the default camera
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                console.print("[!] Cannot open webcam. It may be in use or not connected.", style="bold red")
                return

            # Capture a single frame
            ret, frame = cap.read()

            if not ret:
                console.print("[!] Failed to capture frame from webcam.", style="bold red")
                cap.release()
                return

            # Save the captured frame to a file
            cv2.imwrite(output_file, frame)
            console.print(f"[bold green][+] Snapshot saved successfully to {output_file}[/bold green]")

            # Release the camera
            cap.release()

        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
            # Try to release the camera on error if it was opened
            if 'cap' in locals() and cap.isOpened():
                cap.release()
