import requests
import io
from PyPDF2 import PdfReader
from PIL import Image
from PIL.ExifTags import TAGS
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class MetadataExtractor(BaseModule):
    """Downloads a file from a URL and extracts its metadata."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'URL': ['http://example.com/document.pdf', 'The URL of the file to analyze (PDF or image).']
        }

    def run(self, options):
        """
        Executes the metadata extraction.
        """
        url = options.get('URL')
        console = Console()

        if not url:
            console.print("[!] URL option not set.", style="bold red")
            return

        try:
            console.print(f"[*] Downloading file from {url}...")
            response = requests.get(url, timeout=20)
            response.raise_for_status() # Raise an exception for bad status codes
            file_content = io.BytesIO(response.content)
            content_type = response.headers.get('Content-Type', '').lower()

            if 'pdf' in content_type:
                self._extract_pdf_metadata(file_content, console)
            elif 'image' in content_type or url.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                self._extract_image_metadata(file_content, console)
            else:
                console.print(f"[yellow]Unsupported file type: {content_type}. Can only process PDF and image files.[/yellow]")

        except requests.exceptions.RequestException as e:
            console.print(f"[!] Failed to download file: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")

    def _extract_pdf_metadata(self, file_content, console):
        """Extracts and prints metadata from a PDF file."""
        try:
            pdf = PdfReader(file_content)
            info = pdf.metadata
            if not info:
                console.print("[yellow]No metadata found in the PDF.[/yellow]")
                return

            table = Table(title="PDF Metadata")
            table.add_column("Field", style="cyan")
            table.add_column("Value")
            
            table.add_row("Author", str(info.author))
            table.add_row("Creator", str(info.creator))
            table.add_row("Producer", str(info.producer))
            table.add_row("Subject", str(info.subject))
            table.add_row("Title", str(info.title))
            table.add_row("Creation Date", str(info.creation_date))
            table.add_row("Modification Date", str(info.modification_date))
            
            console.print(table)

        except Exception as e:
            console.print(f"[!] Could not read PDF metadata: {e}", style="bold red")

    def _extract_image_metadata(self, file_content, console):
        """Extracts and prints EXIF metadata from an image file."""
        try:
            image = Image.open(file_content)
            exif_data = image._getexif()

            if not exif_data:
                console.print("[yellow]No EXIF metadata found in the image.[/yellow]")
                return

            table = Table(title="Image EXIF Metadata")
            table.add_column("Tag", style="cyan")
            table.add_column("Value")

            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                # Decode bytes value if necessary
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except AttributeError:
                        pass # Keep as bytes if it fails
                table.add_row(str(tag_name), str(value))
            
            console.print(table)

        except Exception as e:
            console.print(f"[!] Could not read image metadata: {e}", style="bold red")
