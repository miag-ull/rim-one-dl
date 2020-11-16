from pathlib import Path

from skimage import img_as_ubyte
from skimage.io import imsave

from dcseg_to_binary_mask import dcseg_to_binary_mask


def generate_dir_binary_masks(dir_name, masks_dir_name, out_dir):
    """Read all the images from dir_name and convert the DCSeg TXT masks from masks_dir_name to binary masks in PNG
    format. The PNG masks are stored in out_dir.

    :param dir_name: directory that contains the RIM-ONE DL images to generate the PNG masks for (string)
    :param masks_dir_name: directory that contains the DCSeg TXT masks to be converted to PNG binary masks (string)
    :param out_dir: directory to store the PNG masks (string)
    """
    basepath = Path(dir_name)
    masks_basepath = Path(masks_dir_name)
    out_dir_basepath = Path(out_dir)
    for entry in basepath.iterdir():
        if not entry.is_dir():
            image_name = entry.resolve().name
            print(f"Generating mask for: {str(entry.resolve())}")
            disc_name = image_name.replace(".png", "-1-Disc-T.txt")
            cup_name = image_name.replace(".png", "-1-Cup-T.txt")
            disc_path = masks_basepath.joinpath(disc_name)
            cup_path = masks_basepath.joinpath(cup_name)
            if not disc_path.exists() or not cup_path.exists():
                print(f"Missing mask(s) for: {str(entry.resolve())}")
                continue
            # Get the disc and cup masks as NumPy arrays
            disc_mask = dcseg_to_binary_mask(str(entry.resolve()), str(disc_path.resolve()))
            cup_mask = dcseg_to_binary_mask(str(entry.resolve()), str(cup_path.resolve()))
            # Save the masks as PNG
            out_disc_name = disc_name.replace(".txt", ".png")
            out_cup_name = cup_name.replace(".txt", ".png")
            disc_mask = img_as_ubyte(disc_mask)
            cup_mask = img_as_ubyte(cup_mask)
            imsave(out_dir_basepath.joinpath(out_disc_name), disc_mask, check_contrast=False)
            imsave(out_dir_basepath.joinpath(out_cup_name), cup_mask, check_contrast=False)


if __name__ == "__main__":
    # Adjust the directories to your actual values:
    generate_dir_binary_masks(
        'path_to_RIM-ONE_DL_images/normal',
        'path_to_RIM-ONE_DL_reference_segmentations/normal',
        'path_to_output_dir/normal_png')    # The output directory has to be created first

    # Adjust the directories to your actual values:
    generate_dir_binary_masks(
        'path_to_RIM-ONE_DL_images/glaucoma',
        'path_to_RIM-ONE_DL_reference_segmentations/glaucoma',
        'path_to_output_dir/glaucoma_png')    # The output directory has to be created first

    print("Done.")
