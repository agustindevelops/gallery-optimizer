import os
import subprocess
from PIL import Image

def open_heic(file_path):
    heif_file = pyheif.read(file_path)
    return Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

def optimize_image(image_path, output_dir):
    max_size = (350, 300)  # Maximum size
    with Image.open(image_path) as img:
        img.convert('RGB')
        
        # Use Image.Resampling.LANCZOS for high-quality downsampling
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Prepare the output path and replace file extension if necessary
        output_filename = os.path.basename(image_path).rsplit('.', 1)[0] + '.jpg'
        output_path = os.path.join(output_dir, output_filename)
        
        # Save the optimized image
        img.save(output_path, "JPEG", quality=85)

def convert_video(video_path, output_dir):
    base_name = os.path.basename(video_path)
    # Add a suffix to the base name to avoid overwriting the source file
    name, ext = os.path.splitext(base_name)
    output_filename = f"{name}-optimized{ext}"
    output_path = os.path.join(output_dir, output_filename.replace('.mov', '.mp4'))

    cmd = [
        'ffmpeg', '-i', video_path,
        '-vcodec', 'h264', '-acodec', 'aac',
        '-vf', "scale='min(350\\, iw):-2'",  # Adjust for aspect ratio
        '-b:v', '800k',
        output_path
    ]

    subprocess.run(cmd, check=True)

def main():
    input_dir = 'portfolio'
    output_dir = os.path.join(input_dir, 'optimized')
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.heic') or file.lower().endswith('.jpg'):
                optimize_image(os.path.join(root, file), output_dir)
            elif file.lower().endswith('.mov'):
                convert_video(os.path.join(root, file), output_dir)

if __name__ == "__main__":
    main()
