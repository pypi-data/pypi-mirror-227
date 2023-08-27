# tools.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of ImageDatasetTools and is released under
# the MIT License: https://opensource.org/license/mit/

import os
import shutil
from PIL import Image
from .utils import _Logger

class History:
    def __init__(self, path: str) -> None:
        """
        Images label history file manager

        Parameters
        ----------
        path : str
            path to history text file, by default dataset parent folder
        """
        self.path = path

    def __str__(self) -> None:
        self.__call__()
        return ''

    def __call__(self) -> None:
        with open(self.path, 'r') as history_file:
            i = 1
            for line in history_file:
                print(f"{str(i).rjust(6)} | {line}", end='')
                i += 1
        return

    def load(self,
             existing_old_labels: list = None,
             existing_new_labels: list = None) -> tuple[list, list]:
        """
        Load original and new labels from history file

        Parameters
        ----------
        existing_old_labels : list[str], optional
            confront saved old labels with existing images label to avoid reconversions
        existing_new_labels : list[str], optional
            confront saved new labels with existing images label to avoid reconversions

        Returns
        -------
        tuple[list[str], list[str]]
            return saved old and new images label
        """
        _Logger.text(f"Reading history from \"{self.path}\"...")
        history_new_labels = []
        history_old_labels = []
        with open(self.path, 'r') as history_file:
            for line in history_file:
                old_label, new_label = line.strip().split(',')
                if old_label in existing_old_labels and new_label not in existing_new_labels:
                    line.strip(' ')
                else:
                    history_old_labels.append(old_label)
                    history_new_labels.append(new_label)
        _Logger.success(f"History loaded!")
        return history_old_labels, history_new_labels

    def save(self, old_labels, new_labels) -> None:
        """
        Save original and new labels to history file

        Parameters
        ----------
        old_labels : list[str]
            list of old labels to save
        new_labels : list[str]
            list of new labels to save
        """
        _Logger.text(f"Updating history to \"{self.path}\"...")
        for old_label, new_label in zip(old_labels, new_labels):
            with open(self.path, 'a') as history_file:
                history_file.write(f"{old_label},{new_label}\n")
            lines_seen = set()
            # Avoid repetitions
            with open(self.path, 'r') as file:
                lines = file.readlines()
            with open(self.path, 'w') as file:
                for line in lines:
                    if line.strip() not in lines_seen:
                        file.write(line)
                        lines_seen.add(line.strip())
        _Logger.success(f"History saved!")

    def clear(self) -> None:
        """
        Clear the history file
        """
        _Logger.text(f"Clearing \"{self.path}\"...")
        history = open(self.path, 'r+')
        history.truncate(0)
        _Logger.success(f"History cleared!")

class Transformer:
    def __init__(self, dataset_folder: str, target_folder: str) -> None:
        """
        Transformer tool to perform various action on an image dataset

        Paramters
        ---------
        dataset_folder : str
            path to the dataset folder
        target_folder : str
            path to the target folder
        """
        self.dataset_folder = dataset_folder
        self.target_folder = target_folder

    def __str__(self) -> None:
        self.__call__()
        return ''

    def __call__(self) -> None:
        _Logger.classic(f"\n{type(self)}\n\nArgs:\n-----")
        _Logger.classic(f"dataset_folder: {type(self.dataset_folder)}\n{' '*4}\"{self.dataset_folder}\"")
        _Logger.classic(f"target_folder: {type(self.target_folder)}\n{' '*4}\"{self.target_folder}\"")
        return

    def _get_labels(self, verbose: bool = False) -> tuple[list, list]:
        if verbose:
            _Logger.text(f"Scanning \"{self.dataset_folder}\" for images...")
        old_labels = [f for f in os.listdir(self.dataset_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if verbose:
            _Logger.success(f"{len(old_labels)} images found!")
        old_labels = self._sort(self.dataset_folder, old_labels, verbose=False)
        if verbose:
            _Logger.text(f"Scanning \"{self.target_folder}\" for images...")
        new_labels = [f for f in os.listdir(self.target_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if verbose:
            _Logger.success(f"{len(new_labels)} images found!")
        return old_labels, new_labels

    def _sort(self, folder, labels, verbose: bool = False) -> list:
        if verbose:
            _Logger.text(f"Sorting images from \"{folder}\"...")
        labels.sort()
        if verbose:
            _Logger.success(f"Images sorted!")
        return labels

    def convert(self,
                dataset_folder: str = None,
                target_folder: str = None,
                labels: list = None,
                dataset_name: str = '',
                remove_originals: bool = False,
                history_new_labels: list = None,
                verbose: bool = False) -> tuple[list, list]:
        """
        Convert to jpg format and ordinally raname the images of a dataset

        Parameters
        ----------
        dataset_folder : str, optional
            path to the dataset folder, by default Transformer.dataset_folder
        target_folder : str, optional
            path to the target folder, by default Transformer.target_folder
        labels : list[str], optional
            list of original images labels to convert, by default obtained through the Transformer.dataset_folder
        dataset_name : str, optional
            prefix to add when renaming, by default None
        remove_originals : bool, optional
            remove original images after conversion, by default False
        history_new_labels : list[str], optional
            list of images to skip from conversion, by default None
        verbose: bool, optional
            get more output, by default False.

        Returns
        -------
        tuple[list[str], list[str]]
            lists of original labels and converted labels.
        """
        if not dataset_folder:
            dataset_folder = self.dataset_folder
        if not target_folder:
            target_folder = self.target_folder
        if not labels:
            labels, _ = self._get_labels(verbose)
        _Logger.text(f"Converting and renaming images from \"{dataset_folder}\"...")
        old_labels = []
        new_labels = []
        counter = 0
        index = 1
        for old_label in labels:
            _Logger.loading(f"[{index}/{len(labels)}]")
            old_path = os.path.join(dataset_folder, old_label)
            if not(old_label.lower().startswith(dataset_name) and old_label[len(dataset_name):].split('.')[0].isdigit()):
                new_label = f'{dataset_name}{index:08d}.jpg'
                if not(new_label in history_new_labels or new_label in new_labels):
                    while new_label.lower() in labels:
                        index += 1
                        new_label = f'{dataset_name}{index:08d}.jpg'
                    if not old_label.lower().endswith('.jpg'):
                        image = Image.open(old_path)
                        new_path = os.path.join(target_folder, new_label)
                        image.convert('RGB').save(new_path, format='JPEG')
                        image.close()
                    else:
                        new_path = os.path.join(target_folder, new_label)
                        shutil.copy(old_path, new_path)
                    if remove_originals:
                        os.remove(old_path)
                    old_labels.append(old_label)
                    new_labels.append(new_label)
                    counter += 1
            index += 1
        print(20*' ', end='\r')
        _Logger.success(f"[{counter}/{len(labels)}] images converted and renamed!")
        return old_labels, new_labels

    def scale(self,
              scaling_size: int = 640,
              folder: str = None,
              labels: list = None,
              verbose: bool = False) -> None:
        """
        Scale images of a dataset

        Parameters
        ----------
        scaling_size : int, optional
            target size (px) for scaling images from the target folder, by default 1080
        folder : str, optional
            path to the folder containing the images, by default Transformer.target_folder
        labels : list, optional
            list of images label to convert, by default obtained through the Transformer.dataset_folder
        verbose : bool, optional
            get more output, by default False
        """
        if not folder:
            folder = self.target_folder
        if not labels:
            _, labels = self._get_labels(verbose)
        _Logger.text(f"Scaling images from \"{folder}\"...")
        counter = 0
        index = 0
        for label in labels:
            _Logger.loading(f"[{index}/{len(labels)}]")
            image_path = os.path.join(folder, label)
            image = Image.open(image_path)
            width, height = image.size
            if scaling_size < height and scaling_size < width:
                if width <= height:
                    new_width = scaling_size
                    new_height = int(height * (scaling_size / width))
                elif width > height:
                    new_width = int(width * (scaling_size / height))
                    new_height = scaling_size
                scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
                scaled_image.save(image_path, format='JPEG')
                counter += 1
            elif scaling_size <= height and scaling_size <= width:
                scaled_image = image
            else:
                scaled_image = image
                _Logger.error(f"Image \"{os.path.basename(image.filename)}\" has low resolution: can't be rescaled!")
            scaled_image.close()
            index += 1
        print(20*' ', end='\r')
        _Logger.success(f"[{counter}/{len(labels)}] images rescaled!")

    def crop(self,
             folder: str = None,
             labels: list = None,
             verbose: bool = False) -> None:
        """
        Crop images of a dataset

        Parameters
        ----------
        folder : str, optional
            path to the folder containing the images, by default Transformer.target_folder, by default None
        labels : list, optional
            list of images label to convert, by default obtained through the Transformer.dataset_folder
        verbose : bool, optional
            get more output, by default False
        """
        if not folder:
            folder = self.target_folder
        if not labels:
            _, labels = self._get_labels(verbose)
        _Logger.text(f"Resizing images from \"{folder}\"...")
        counter = 0
        index = 0
        for label in labels:
            _Logger.loading(f"[{index}/{len(labels)}]")
            image_path = os.path.join(folder, label)
            image = Image.open(image_path)
            width, height = image.size
            crop_length = min(width, height)
            if height != width and (height == crop_length or width == crop_length):
                if height < width:
                    offset = int((width - crop_length)/2)
                    if width % 2 == 0:
                        cropped_image = image.crop((offset, 0, width-offset, height))
                    else:
                        cropped_image = image.crop((offset, 0, width-offset-1, height))
                    cropped_image.save(image_path, format='JPEG')
                    counter += 1
                elif height > width:
                    offset = int((height - crop_length)/2)
                    if height % 2 == 0:
                        cropped_image = image.crop((0, offset, width, height-offset))
                    else:
                        cropped_image = image.crop((0, offset, width, height-offset-1))
                    cropped_image.save(image_path, format='JPEG')
                    counter += 1
                else:
                    cropped_image = image
            else:
                cropped_image = image
            cropped_image.close()
            index += 1
        print(20*' ', end='\r')
        _Logger.success(f"[{counter}/{len(labels)}] images cropped!")