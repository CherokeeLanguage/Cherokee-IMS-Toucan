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
import random
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
    src_audio_globs: List[str] = [
            "data/other-audio-data/cstr-vctk-corpus/mp3-48k/*.mp3",
            "data/other-audio-data/comvoi_clean/mp3/*.mp3"
    ]

    noise_audio_glob: str = "data/other-audio-data/noise/*.mp3"

    shutil.rmtree(dest_audio_dir, ignore_errors=True)
    os.makedirs(dest_audio_dir)

    print("\n=== Creating HiFiGan wavs")

    all_audio_files: List[str] = []
    for audio_file_glob in src_audio_globs:
        all_audio_files.extend(glob.glob(f"{audio_file_glob}"))

    print("Creating clean audio files")
    bar: ProgressBar = ProgressBar(maxval=len(all_audio_files))
    bar.start()
    idx: int = 0
    for audio_file in all_audio_files:
        idx += 1
        audio_file_noisy: str = f"{idx:09d}_clean.wav"
        audio: AudioSegment = AudioSegment.from_file(audio_file)
        audio = audio.set_channels(1).set_frame_rate(output_sr)
        audio.export(os.path.join(dest_audio_dir, audio_file_noisy), format="wav")
        bar.update(bar.currval + 1)
    bar.finish()

    print("Creating noisy audio files")
    noise_audio_segments: List[AudioSegment] = list()
    for noise_file in glob.glob(noise_audio_glob):
        noise_audio_segments.append(AudioSegment.from_file(noise_file).set_frame_rate(output_sr).set_channels(1))
    ran: random.Random = random.Random(len(noise_audio_segments))
    bar: ProgressBar = ProgressBar(maxval=len(all_audio_files))
    bar.start()
    idx: int = 0
    for audio_file in all_audio_files:
        idx += 1
        ran.shuffle(noise_audio_segments)
        noise_overlay: AudioSegment = AudioSegment.silent(frame_rate=output_sr)
        for segment in noise_audio_segments:
            noise_overlay.append(segment)
        audio_file_noisy: str = f"{idx:09d}_noisy.wav"
        audio: AudioSegment = AudioSegment.from_file(audio_file).set_frame_rate(output_sr)
        audio = audio.overlay(noise_overlay, loop=True)
        if ran.choice([True, False, False]):
            audio = audio.set_frame_rate(8000).set_frame_rate(output_sr)
        elif ran.choice([True, False, False]):
            audio = audio.set_frame_rate(4000).set_frame_rate(output_sr)
        audio = audio.set_channels(1)
        audio.export(os.path.join(dest_audio_dir, audio_file_noisy), format="wav")
        bar.update(bar.currval + 1)
    bar.finish()


if __name__ == "__main__":
    main()
