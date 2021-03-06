import os
import shutil
import sys
import platform

import pandas as pd

from preprocessor import image_center_crop


if not os.path.exists("./data"):
    os.mkdir("./data")

if not os.path.exists("./data/coronahack-chest-xraydataset.zip"):
    os.chdir("./data")
    os.system("kaggle datasets download -d praveengovi/coronahack-chest-xraydataset")
    os.chdir("..")
else:
    print("Download found...")

print("Starting Extraction")
print(platform.system())
if platform.system() in ["Linux", "Darwin"]:
    os.system('unzip -q "./data/coronahack-chest-xraydataset.zip" -d "./data/"')
else:
    os.system(
        'tar -xf "./data/coronahack-chest-xraydataset.zip" --directory "./data/" '
    )
print("Extraction Complete")

print("Reading Metadata")
images_data = pd.read_csv("./data/Chest_xray_Corona_Metadata.csv")

os.mkdir("./data/Corona_Classification_data")
os.mkdir("./data/Corona_Classification_data/train")
os.mkdir("./data/Corona_Classification_data/train/INFECTED")
os.mkdir("./data/Corona_Classification_data/train/NORMAL")
os.mkdir("./data/Corona_Classification_data/test")
os.mkdir("./data/Corona_Classification_data/test/NORMAL")
os.mkdir("./data/Corona_Classification_data/test/INFECTED")


print("Starting Preprocessing and Moving According to Labels...")

for index, row in images_data.iterrows():
    if row["Dataset_type"] == "TRAIN":
        path_of_image = f"./data/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset/train/{row['X_ray_image_name']}"
        image_center_crop(path_of_image)
        if row["Label"] == "Normal":
            shutil.move(
                path_of_image,
                f"./data/Corona_Classification_data/train/NORMAL/{row['X_ray_image_name']}",
            )

        if row["Label"] == "Pnemonia":
            shutil.move(
                path_of_image,
                f"./data/Corona_Classification_data/train/INFECTED/{row['X_ray_image_name']}",
            )

    if row["Dataset_type"] == "TEST":
        path_of_image = f"./data/Coronahack-Chest-XRay-Dataset/Coronahack-Chest-XRay-Dataset/test/{row['X_ray_image_name']}"
        image_center_crop(path_of_image)
        if row["Label"] == "Normal":
            shutil.move(
                path_of_image,
                f"./data/Corona_Classification_data/test/NORMAL/{row['X_ray_image_name']}",
            )

        if row["Label"] == "Pnemonia":
            shutil.move(
                path_of_image,
                f"./data/Corona_Classification_data/test/INFECTED/{row['X_ray_image_name']}",
            )
    sys.stdout.write(f"\rCropping Successfull for {row['X_ray_image_name']}")
    sys.stdout.flush()


print("Moving Complete")
shutil.rmtree("./data/Coronahack-Chest-XRay-Dataset")

files_to_be_deleted = [
    "1-s2.0-S1684118220300682-main.pdf-002-a1.png",
    "1-s2.0-S1684118220300682-main.pdf-002-a2.png",
    "1-s2.0-S1684118220300682-main.pdf-003-b1.png",
    "1-s2.0-S1684118220300682-main.pdf-003-b2.png",
    "7EF28E12-F628-4BEC-A8C5-E6277C2E4F60.png",
    "23E99E2E-447C-46E5-8EB2-D35D12473C39.png",
    "41591_2020_819_Fig1_HTML.webp-day5.png",
    "41591_2020_819_Fig1_HTML.webp-day10.png",
]

for filename in files_to_be_deleted:
    os.remove(f"./data/Corona_Classification_data/train/INFECTED/{filename}")
print("Cleaning Complete")
