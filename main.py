import sys

import numpy as np
import torch
import torchvision
import argparse

from model import CoronaDetection

DESCRIPTION = """
Train the Corona Detection Model
"""

USAGE = """py runner.py --base_model base_model 

Run Corona Detection Model on your machine.

For example, you can pass the following parameters:

python main.py --base_model Inception --optimizer Adam --learning_rate 0.00001 --batch_size 32 --epoch 25 --colab

This will run main.py with base model as Inception and given parameters

"""

parser = argparse.ArgumentParser(description=DESCRIPTION, usage=USAGE)
parser.add_argument(
    "--base_model",
    metavar="base_model",
    type=str,
    action="store",
    help="Base Model to use. Available Options: ResNet18, ResNet34, ResNet50, ResNet101, ResNet152, Alexnet, VGG11, VGG13, VGG16, VGG19, GoogleNet, Inception",
    required=True,
)
parser.add_argument(
    "--optimizer",
    metavar="optimizer",
    type=str,
    action="store",
    help="Optimizer to use in the training",
    required=True,
)
parser.add_argument(
    "--learning_rate",
    metavar="learning_rate",
    type=float,
    action="store",
    help="Learning Rate for training",
    default=0.00001,
)
parser.add_argument(
    "--batch_size",
    metavar="batch_size",
    type=int,
    action="store",
    help="Batch_size",
    default=16,
)
parser.add_argument(
    "--epoch", metavar="epoch", type=int, action="store", help="Epoch", default=15
)
parser.add_argument(
    "--colab",
    action="store_true",
    help="Option to use when using colab for training...Mount the drive and it will be saved in the drive",
)

optimizers = {
    "Adam": torch.optim.Adam,
    "SGD": torch.optim.SGD,
    "RMSprop": torch.optim.RMSprop,
    "Adagrad": torch.optim.Adagrad,
    "Adadelta": torch.optim.Adadelta,
}

if __name__ == "__main__":
    kwargs = vars(parser.parse_args())

    print("Corona Detection Project")

    if torch.cuda.is_available():
        print("Using GPU")
        device = torch.device("cuda")
    else:
        print("Using CPU")
        device = torch.device("cpu")

    print("Creating Model Object: ")
    model = CoronaDetection(kwargs["base_model"], colab=kwargs["colab"])

    print("Setting up Data Directories")
    train_data_path = "./data/Corona_Classification_data/train/"
    train_data = torchvision.datasets.ImageFolder(
        root=train_data_path, transform=model.train_transformation
    )

    test_data_path = "./data/Corona_Classification_data/test/"
    test_data = torchvision.datasets.ImageFolder(
        root=test_data_path, transform=model.test_transformation
    )

    batch_size = kwargs["batch_size"]

    train_data_loader = torch.utils.data.DataLoader(
        train_data, batch_size=batch_size, shuffle=True
    )
    test_data_loader = torch.utils.data.DataLoader(
        test_data, batch_size=batch_size, shuffle=True
    )

    learning_rate = kwargs["learning_rate"]

    optimizer = optimizers[kwargs["optimizer"]](
        model.model.parameters(), lr=learning_rate
    )

    print("Starting Training")
    model.train(
        optimizer,
        torch.nn.CrossEntropyLoss(),
        train_data_loader,
        test_data_loader,
        epochs=kwargs["epoch"],
        device=device,
    )
    print("Completed Training")
