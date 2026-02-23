import os

def get_unique_path(standard_path):
        if not os.path.exists(standard_path):
            return standard_path

        base, ext = os.path.splitext(standard_path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path