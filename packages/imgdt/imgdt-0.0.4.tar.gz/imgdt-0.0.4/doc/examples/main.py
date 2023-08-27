from imgdt import run

run(
    dataset_folder = "path\\to\\folder",
    target_folder = None,
    history_file = None,
    dataset_name = 'Weapons',
    convert_img = True,
    scaling_size = 1080,
    crop_img = True,
    remove_originals = False,
    verbose = True
)
