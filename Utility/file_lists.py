import glob
import os

from typing import List


def get_hifigan_wav_list() -> List[str]:
    file_list: List[str] = list()
    root = os.path.abspath(os.path.join("IMS_Toucan", "audios", "vocoder"))
    for wav in glob.glob(os.path.join(root, "*_clean.wav")):
        file_list.append(wav)
    return file_list
