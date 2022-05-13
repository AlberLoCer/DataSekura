class VolumeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Encrypted volume already exists!"

class DriveXexception(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Drive X:// is already being used..."

class VCencryptionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Impossible to encrypt... Try in another directory"

class SplitFileException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Could not split the encrypted file"

class MilestoneException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Milestone file could not be found!"

class MilestoneDecryptionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "An error ocurred while decrypting milestone files!"

class PermissionDeniedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Permission denied for encrypting this directory!"

class ExistingBackupException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Could not create backup, another backup already exists."

class IncorrectPasswordException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Incorrect password!"

class DropboxTokenException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Invalid access token introduced."

class DriveLoginException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Invalid user authentication flow."

class ExistingScatterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "There is already a scattered file named like that!"

class NonExistingScatterFileException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "No matching scattered files found!"

class DriveDownloadException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Could not fetch requested Google Drive resource."

class DriveUploadException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Could not upload file to Google Drive."

class DropboxDownloadException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Could not fetch requested Dropbox resource."

class DropboxUploadException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "Could not upload file to Dropbox."

class DropboxBinNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "No matching encrypted files found!"

class DropboxNoBinException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "No binary files were found!"

class DropboxFileNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "No matching encrypted files found!"
