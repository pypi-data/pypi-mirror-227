# MP3Metadata
MP3Metadata is a tool for the manipulation and creation of metadata in MP3 files.

## Requirements
- [Mutagen](https://mutagen.readthedocs.io/en/latest/)

MP3Metadata makes heavy use of Mutagen, which is designed for reading and writing metadata in a variety of media formats. MP3Metadata is essentially just a wrapper for the EasyMP3 class, which offers a simpler, more select interface to the EasyID3 class. MP3Metadata makes use of features in the EasyID3 class in order to add album artwork to its shortened list of attributes, as well as completing some processing so that image data is easier to display on platforms such as [Kivy](https://kivy.org/).

## Usage
```python
from mp3metadata import MP3Metadata

mp3 = MP3Metadata('One Week.mp3')

# ['One Week']
print(mp3['title'])
# ['Barenaked Ladies']
print(mp3['artist'])
# [<_io.BytesIO object at 0xffffffff>, 'jpg']
print(mp3['artwork'])

# New title
mp3['title'] = 'Five Days in May'
# New artwork (provide path to file)
mp3['artwork'] = 'gordon800x800.jpg'

# Save changes
mp3.save()
```
Here's how you can insert the artwork into Kivy.
```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

from mp3metadata import MP3Metadata


class AlbumArtwork(Image):
    def __new__(self, path: str) -> Image:
        mp3 = MP3Metadata(path)
        data, ext = mp3['artwork']
        img = CoreImage(data, ext=ext)
        
        return Image(texture=img.texture)


class MusicWidget(Widget):
    def __init__(self) -> None:
        super().__init__()
        
        self.path = '/music/03/Dear August.mp3'
        self.image = AlbumArtwork(self.path)
        
        self.add_widget(self.image)


class MusicApp(App):
    def build(self):
        return MusicWidget()


MusicApp().run()
```
