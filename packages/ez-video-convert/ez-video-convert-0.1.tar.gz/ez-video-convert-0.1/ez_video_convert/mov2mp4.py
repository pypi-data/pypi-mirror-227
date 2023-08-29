import click
import os
import subprocess
import pyperclip

@click.command()
def convert_mov_to_mp4():
    # Get path from clipboard
    mov_path = pyperclip.paste().strip()

    if not os.path.exists(mov_path) or not mov_path.lower().endswith(".mov"):
        click.echo("Invalid .mov file path from clipboard. Please copy a valid .mov file path.")
        return

    mp4_path = mov_path.rsplit('.', 1)[0] + '.mp4'
    
    subprocess.run(['ffmpeg', '-i', mov_path, mp4_path])
    click.echo(f"Converted {mov_path} to {mp4_path}")

if __name__ == "__main__":
    convert_mov_to_mp4()