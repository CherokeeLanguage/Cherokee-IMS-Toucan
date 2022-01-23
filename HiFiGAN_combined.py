#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(conda shell.bash hook)"
conda deactivate
conda activate toucan_conda_venv
exec python "$0" "$@"
exit $?
''"""
import os
import random
import shutil

import torch

from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.HiFiGAN import HiFiGANGenerator
from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.HiFiGAN import HiFiGANMultiScaleMultiPeriodDiscriminator
from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.HiFiGANDataset_disk import HiFiGANDataset
from IMS_Toucan.TrainingInterfaces.Spectrogram_to_Wave.HiFIGAN.hifigan_train_loop import train_loop
from Utility.file_lists import *


def main():
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(0)
    device = torch.device("cuda")

    torch.manual_seed(131714)
    random.seed(131714)
    torch.random.manual_seed(131714)

    print("Preparing")
    model_save_dir = os.path.join("IMS_Toucan", "Models", "HiFiGAN_combined")
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)

    shutil.rmtree("_cache", ignore_errors=True)
    os.makedirs("_cache", exist_ok=True)

    file_list: List[str] = get_hifigan_wav_list()
    train_set = HiFiGANDataset(list_of_paths=file_list, cache_dir="_cache", loading_processes=1)

    generator = HiFiGANGenerator()
    generator.reset_parameters()
    multi_scale_discriminator = HiFiGANMultiScaleMultiPeriodDiscriminator()

    print("Training model")
    train_loop(batch_size=16,
               steps=2_000_000,
               generator=generator,
               discriminator=multi_scale_discriminator,
               train_dataset=train_set,
               device=device,
               epochs_per_save=1,
               model_save_dir=model_save_dir,
               path_to_checkpoint=None)  # os.path.join(model_save_dir, "checkpoint_328158.pt"))


if __name__ == "__main__":
    main()
