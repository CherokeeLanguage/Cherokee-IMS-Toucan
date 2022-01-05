import os

from typing import List

from typing import List


def get_file_list_cstr_vctk_corpus() -> List[str]:
    root = os.path.abspath("data/other-audio-data/cstr-vctk-corpus")
    file_list: List[str] = list()
    with open(os.path.join(root, "cstr-vctk-corpus-48k.txt")) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            wav_file = os.path.splitext(line.split("|")[3])[0]+".wav"
            wav_path = os.path.join(root, "wavs", wav_file)
            if os.path.exists(wav_path):
                file_list.append(wav_path)
    return file_list
