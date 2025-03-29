from os import walk
import pygame

def import_folder(path):
    surface_list = []
    
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = f"{path}/{image}"
            # print(f"Trying to load: {full_path}")
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
            except pygame.error as e:
                print(f"Error loading {full_path}: {e}")  # Print the specific error
                continue
    
    return surface_list