from io import BytesIO
from os.path import splitext

from mutagen.mp3 import EasyMP3
from mutagen.id3 import ID3, APIC


class MP3Metadata(EasyMP3):
    def __init__(self, file: str) -> None:
        super().__init__(file)
        self.ID3.RegisterKey('artwork', self._get_artwork, self._set_artwork, self._delete_artwork)
    
    def _get_artwork(self, id3: ID3, key: str) -> [BytesIO, str]:
        artwork = id3['APIC:']
        data = BytesIO(artwork.data)
        ext = artwork.mime.split('/')[-1]
        
        return [data, ext]
    
    def _set_artwork(self, id3: ID3, key: str, file: str) -> None:
        with open(file[0], 'rb') as data:
            id3['APIC:'] = APIC(
                encoding = 3,
                mime = 'image/' + splitext(file[0])[1],
                type = 3,
                desc = key.title(),
                data = data.read()
            )
    
    def _delete_artwork(self, id3: ID3, key: str) -> None:
        del id3['APIC:']
