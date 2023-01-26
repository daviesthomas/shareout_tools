import argparse
import moviepy.editor as mpe
from typing import List
import os

def parse_args():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input_videos", nargs='+', help='<Required> Input videos', required=True)
    argument_parser.add_argument("-o", "--output_path", help="<Required> output path", required=True)
    argument_parser.add_argument("-r", "--rows", help="number of rows in panel", required=False, default=1)
    argument_parser.add_argument("-c", "--cols", help="number of cols in panel", required=False, default=None)

    args = argument_parser.parse_args()
    return args

def create_video_panel(video_paths: List[str], rows: int, cols: int):
    clips = [mpe.VideoFileClip(video_path) for video_path in video_paths]
    final_clip = mpe.clips_array([clips])
    final_clip.audio = clips[0].audio
    return final_clip

if __name__ == "__main__":
    parsed_args = parse_args()


    num_videos = len(parsed_args.input_videos)

    num_rows = 1 #args.rows
    num_cols = num_videos #args.cols

    clip = create_video_panel(parsed_args.input_videos, num_rows, num_cols)
    clip.write_videofile(parsed_args.output_path)