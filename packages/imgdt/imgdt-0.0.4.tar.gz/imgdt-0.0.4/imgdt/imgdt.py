# imgdt.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of ImageDatasetTools and is released under
# the MIT License: https://opensource.org/license/mit/

import os
from pathlib import Path
from .tools import History, Transformer
from .utils import _Logger

def run(dataset_folder,
        target_folder: str = None,
        history_file: str = None,
        dataset_name: str = None,
        convert_img: bool = True,
        scaling_size: int = 1080,
        crop_img: bool = True,
        remove_originals: bool = False,
        verbose: bool = False):
    """
    Images conversion pipeline

    Parameters
    ----------
    dataset_folder : str
        path to the dataset folder
    target_folder : str, optional
        path to the target folde, by default dataset parent folder
    history_file : str, optional
        path to the history file, by default dataset parent folder
    dataset_name : str, optional
        prefix for renamed images and new folders, by default None
    convert_img : bool, optional
        convert and rename the images from the dataset folder to the target folder, by default True
    scaling_size : int, None, optional
        target size (px) for scaling images from the target folder, by default 1080
    crop_img : bool, optional
        crop the images from the target folder, by default True
    remove_originals : bool, optional
        remove original images after conversion, by default False
    verbose: bool, optional
        print more output, by default 'False'
    """
    if not isinstance(dataset_folder, str):
        raise TypeError("'dataset_folder' parameter in function 'imgdt.run()' must be a string.")
    if not os.path.exists(dataset_folder):
        raise ValueError("'dataset_folder' parameter in function 'imgdt.run()' does not exists!")
    if not os.path.isdir(dataset_folder):
        raise ValueError("'dataset_folder' parameter in function 'imgdt.run()' is not a folder!")
    if target_folder and not isinstance(target_folder, str):
        raise TypeError("'target_folder' parameter in function 'imgdt.run()' must be a string.")
    if history_file and not isinstance(history_file, str):
        raise TypeError("'history_file' parameter in function 'imgdt.run()' must be a string.")
    if dataset_name and not isinstance(dataset_name, str):
        raise TypeError("'dataset name' parameter in function 'imgdt.run()' must be a string.")
    if convert_img and not isinstance(convert_img, bool):
        raise TypeError("'convert_img' parameter in function 'imgdt.run()' must be boolean.")
    if scaling_size and not (isinstance(scaling_size, int) or isinstance(scaling_size, None)):
        raise TypeError("'scaling_size' parameter in function 'imgdt.run()' must be an integer or None.")
    elif scaling_size and isinstance(scaling_size, int):
        if scaling_size < 1 or scaling_size > 4320:
            raise ValueError("'scaling_size' parameter in function 'imgdt.run()' must be positive and less than 4320.")
    if crop_img and not isinstance(crop_img, bool):
        raise TypeError("'crop_img' parameter in function 'imgdt.run()' must be boolean.")
    if remove_originals and not isinstance(remove_originals, bool):
        raise TypeError("'remove_originals' parameter in function 'imgdt.run()' must be boolean.")
    if verbose and not isinstance(verbose, bool):
        raise TypeError("'verbose' parameter in function 'imgdt.run()' must be boolean.")

    if verbose:
        print("\n[Settings]")

    if dataset_name:
        if verbose:
            _Logger.info(f"{'Dataset name'.ljust(24)}: \'{dataset_name}\'")
        dataset_name = dataset_name + '_'

    if verbose:
        _Logger.info(f"{'Dataset folder path'.ljust(24)}: \"{dataset_folder}\"")

    if not target_folder or not os.path.exists(target_folder):
        target_folder = os.path.join(Path(dataset_folder).parent.absolute(), f"{dataset_name}New")
        if os.path.isdir(target_folder):
            suffix = f"\"{target_folder}\""
        else:
            suffix = "None"
    if verbose: _Logger.info(f"{'Target folder path'.ljust(24)}: {suffix}")

    if not history_file or not os.path.exists(history_file):
        history_file = os.path.join(Path(dataset_folder).parent.absolute(), f"{dataset_name}History.txt")
        if os.path.isfile(history_file):
            suffix = f"\"{history_file}\""
        else:
            suffix = "None"
    if verbose: _Logger.info(f"{'History file path'.ljust(24)}: {suffix}")

    if verbose: _Logger.info(f"{'Convert images'.ljust(24)}: {convert_img}")
    if verbose: _Logger.info(f"{'Scaling size (px)'.ljust(24)}: {scaling_size}")
    if verbose: _Logger.info(f"{'Crop images'.ljust(24)}: {crop_img}")
    if verbose: _Logger.info(f"{'Remove original images'.ljust(24)}: {remove_originals}")

    if not os.path.isfile(history_file):
        _Logger.text(f"Generating new history...")
        history_new_labels = set()
        with open(history_file, 'w') as f:
            pass
        _Logger.success(f"History generated at \"{history_file}\".")

    if not os.path.isdir(target_folder):
        _Logger.text(f"Generating target folder...")
        os.mkdir(target_folder)
        _Logger.success(f"Target folder generated at \"{target_folder}\".")

    transformer = Transformer(dataset_folder, target_folder)

    history = History(history_file)

    if convert_img:
        old_labels, new_labels = transformer._get_labels(verbose=True)
        _, history_new_labels = history.load(old_labels, new_labels)
        old_labels, new_labels = transformer.convert(
            dataset_name=dataset_name,
            remove_originals=remove_originals,
            history_new_labels=history_new_labels
        )
        history.save(old_labels, new_labels)
    else:
        _Logger.warning("Conversion skipped!")

    if scaling_size:
        transformer.scale(scaling_size)
    else:
        _Logger.warning("Rescaling skipped!")

    if crop_img:
        transformer.crop()
    else:
        _Logger.warning("Crop skipped!")