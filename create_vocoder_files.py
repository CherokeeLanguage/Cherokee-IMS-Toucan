#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(conda shell.bash hook)"
conda deactivate
conda activate toucan_conda_venv
exec python "$0" "$@"
exit $?
''"""

import glob
import shutil
import os
import sys
from progressbar import ProgressBar
from pydub import AudioSegment
from typing import List


def main():
    argv0: str = sys.argv[0]
    if argv0:
        workdir: str = os.path.dirname(argv0)
        if workdir:
            os.chdir(workdir)

    dest_audio_dir: str = os.path.join(os.getcwd(), "IMS_Toucan", "audios", "vocoder")
    output_sr: int = 48000
    src_mp3_globs: List[str] = [
            "data/other-audio-data/cstr-vctk-corpus/mp3-48k/*.mp3",
            "data/other-audio-data/comvoi_clean/mp3/*.mp3"
    ]

    shutil.rmtree(dest_audio_dir, ignore_errors=True)
    os.makedirs(dest_audio_dir)

    print("\n=== Creating HiFiGan wavs")

    all_mp3s: List[str] = []
    for mp3_glob in src_mp3_globs:
        all_mp3s.extend(glob.glob(f"{mp3_glob}"))
    bar: ProgressBar = ProgressBar(maxval=len(all_mp3s))
    bar.start()
    idx: int = 0
    for mp3 in all_mp3s:
        idx += 1
        audio: AudioSegment = AudioSegment.from_file(mp3)
        audio = audio.set_channels(1).set_frame_rate(output_sr)
        audio.export(os.path.join(dest_audio_dir, f"{idx:09d}.wav"), format="wav")
        bar.update(bar.currval + 1)
    bar.finish()


if __name__ == "__main__":
    main()
