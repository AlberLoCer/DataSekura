class File_alterator:
    def __init__(self):
        return
    def split_file(self, path, volName):
        CHUNK_SIZE = 1024
        file_number = 1
        with open(path) as f:
            chunk = f.read(CHUNK_SIZE)
            while chunk:
                with open(volName + str(file_number)) as chunk_file:
                    chunk_file.write(chunk)
                file_number += 1
                chunk = f.read(CHUNK_SIZE)