from typing import List,Union
from PIL import Image
import os


def compress_images(directory:Union[str,None] = None,quality=30):
  if directory:
    os.chdir(directory)
  files: List[str] = [file for file in os.listdir()]
  for file in files:
    if os.path.isdir(file):
      compress_images(file)
    else:
      if file.endswith('jpg') or file.endswith('png'):
        filename,_ = file.split('.')
        try:
          image = Image.open(file)
          image.save(file,optimize=True,quality=quality)
        except Exception as e:
          print(e)
        print(f'{filename} Compressed')
     
  
if __name__ == "__main__":
  compress_images("media")