from PIL import Image
import imagehash
import os

class DuplicateDetection:

    def __init__(
            self, 
            target: list[str], 
            hash_size: int=32, 
            delete_dups: bool=False
    ):
        self.target: list[str] | str = target
        self.hash_size: int = hash_size
        self.delete_dups = delete_dups

    def run(self):
        duplicates = self.detect()
        print(f"\n{len(duplicates)} duplicate(s) found in {len(self.target)} target directories")
        if self.delete_dups:
            inpt = input(f"Do you wish to delete {len(duplicates)} duplicate images Y/N: ")
            if inpt.strip().lower() == "y":
                self.remove(duplicates)

    def detect(self):

        img_paths = self.get_image_paths()
        print(f"Searching {len(img_paths)} images for duplicates...")
        # all previous hashes
        previous_hashes = {}
        # all duplicate image paths
        duplicates = []

        for path in img_paths:

            if os.name == "nt":
                clean_path = path[path.find('C'):]

            with Image.open(path) as img:
        
                # creating a hash for the currrent image
                this_hash = imagehash.average_hash(img, self.hash_size)

                # if this new hash already exists -> its a duplicate
                if this_hash in previous_hashes:

                    this_image_path = clean_path
                    that_image_path = previous_hashes[this_hash]
                    print(f"Duplicate found between: {this_image_path}" +
                          f" and {that_image_path}")
                    
                    duplicates.append(path)
                else:
                    previous_hashes[this_hash] = clean_path

        return duplicates
    
    def get_image_paths(self):

        # img file names inside the target directory
        img_paths = []
        acceptable_extensions = [".jpg", ".png", ".jpeg"]

        for directory in self.target:
            images = os.listdir(directory)

            for img in images:

                file_extension = os.path.splitext(img)[-1]
                if file_extension not in acceptable_extensions:
                    raise TypeError(f"{img} must be a jpeg or png!")
                
                if os.name == "nt":
                    abs_path = os.path.abspath(directory)
                    # long file path exception (windows only)
                    os_dir = r"\\?\\" + abs_path
                else:
                    os_dir = directory

                img_paths.append(os.path.join(os_dir, img))

        return img_paths
    
    def remove(self, duplicates):

        for img_path in duplicates:
            os.remove(img_path)

            if os.name == "nt":
                clean_path = img_path[img_path.find('C'):]
            print(f"{clean_path} has been deleted")

        print(f"{len(duplicates)} duplicate images have been deleted")
