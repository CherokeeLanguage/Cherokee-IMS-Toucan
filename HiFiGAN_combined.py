import random

import torch

from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.HiFiGAN import HiFiGANGenerator
from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.HiFiGAN import HiFiGANMultiScaleMultiPeriodDiscriminator
from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.HiFiGANDataset import HiFiGANDataset
from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.hifigan_train_loop import train_loop
from Utility.file_lists import *


def run(gpu_id, resume_checkpoint, finetune, model_dir):
    if gpu_id == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        device = torch.device("cpu")

    else:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(gpu_id)
        device = torch.device("cuda")

    torch.manual_seed(131714)
    random.seed(131714)
    torch.random.manual_seed(131714)

    print("Preparing")
    if model_dir is not None:
        model_save_dir = model_dir
    else:
        model_save_dir = "Models/HiFiGAN_combined"
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)

    file_lists = list()
    file_lists.append(get_file_list_cstr_vctk_corpus())

    datasets = list()

    for file_list in file_lists:
        datasets.append(HiFiGANDataset(list_of_paths=file_list))
    train_set = torch.utils.data.ConcatDataset(datasets)

    generator = HiFiGANGenerator()
    generator.reset_parameters()
    multi_scale_discriminator = HiFiGANMultiScaleMultiPeriodDiscriminator()

    print("Training model")
    train_loop(batch_size=16,
               steps=2000000,
               generator=generator,
               discriminator=multi_scale_discriminator,
               train_dataset=train_set,
               device=device,
               epochs_per_save=1,
               model_save_dir=model_save_dir,
               path_to_checkpoint=resume_checkpoint)
