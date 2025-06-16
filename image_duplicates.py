from PIL import Image
import imagehash
import os

class DuplicateDetection:

    def __init__(
            self, 
            target: list[str] | str, 
            hash_size: int=32, 
            delete_dups: bool=False
    ):
        self.target: list[str] | str = target
        self.hash_size: int = hash_size
        self.delete_dups = delete_dups

    def run(self):
        duplicates = {}
        if isinstance(self.target, list):
            for dir in self.target:
                duplicates[dir] = self.detect(dir)
        else:
            duplicates[self.target] = self.detect(self.target)

        for dir, dups in duplicates.items():
            print(f"\n{len(dups)} duplicates found in {dir}")

        if self.delete_dups:
            for dir, dups in duplicates.items():
                inpt = input(f"\nDo you wish to delete {len(dups)} duplicate files from {dir}? Y/N ")
                if (inpt.strip().lower()) == "y":
                    self.remove(dups)
        
    def detect(self, directory):

        # img file names inside the target directory
        images = os.listdir(directory)
        # all previous hashes
        previous_hashes = {}
        # all duplicate image paths
        duplicates = []

        for image in images:

            # File type must be a jpeg or png
            file_extension = os.path.splitext(image)[-1]
            acceptable_extensions = [".jpg", ".png", ".jpeg"]
            if file_extension not in acceptable_extensions:
                raise TypeError(f"{image} must be a jpeg or png!")
            
            if os.name == "nt":
                abs_path = os.path.abspath(directory)
                # long file path exception (windows only)
                os_dir = r"\\?\\" + abs_path
            else:
                os_dir = directory
                
            img_path = os.path.join(os_dir, image)

            with Image.open(img_path) as img:
        
                # creating a hash for the currrent image
                this_hash = imagehash.average_hash(img, self.hash_size)

                # if this new hash already exists -> its a duplicate
                if this_hash in previous_hashes:

                    this_image_path = os.path.join(directory, image)
                    that_image_path = os.path.join(
                        directory, previous_hashes[this_hash]
                    )
                    print(f"Duplicate found between: {this_image_path}" +
                          f" and {that_image_path}")
                    
                    duplicates.append(img_path)
                else:
                    previous_hashes[this_hash] = image

        return duplicates
    
    def remove(self, duplicates):
        for img_path in duplicates:
            os.remove(img_path)
            print(f"{img_path} has been deleted")
        print(f"{len(duplicates)} have been removed")
