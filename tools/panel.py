import argparse
import copy

import moviepy.editor as mpe
from typing import List, Optional
import os

import numpy as np

def parse_args():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input_videos", nargs='+', help='<Required> Input videos', required=True)
    argument_parser.add_argument("-l", "--labels", nargs='+', default=None)
    argument_parser.add_argument("-o", "--output_path", help="<Required> output path", required=True)
    argument_parser.add_argument("-r", "--rows", help="number of rows in panel", required=False, default=1, type=int)
    argument_parser.add_argument("-c", "--cols", help="number of cols in panel", required=False, default=None, type=int)

    args = argument_parser.parse_args()
    return args

def _create_idx_grid(rows: int, cols: int) -> List[List[int]]:
    """
    >>> create_idx_grid(5, 2)
    [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
    >>> create_idx_grid(2, 3)
    [[0, 1, 2], [3, 4, 5]]
    >>> create_idx_grid(1, 3)
    [[0, 1, 2]]
    >>> create_idx_grid(3, 1)
    [[0], [1], [2]]
    """
    video_grid_idxs = []
    for row in range(rows):
        row_idxs = []
        for col in range(cols):
            i = col + row*cols
            row_idxs.append(i)
        video_grid_idxs.append(row_idxs)
    return video_grid_idxs

def create_video_panel(video_paths: List[str], rows: int, cols: int, labels: List[str] = None):
    """ Creates video panel given paths and rows/cols target
    """
    idx_grid = _create_idx_grid(rows, cols)
    video_grid: List[List[Optional[mpe.VideoFileClip]]] = [[None]*len(row) for row in idx_grid]

    for row, row_idxs in enumerate(idx_grid):
        for col, video_idx in enumerate(row_idxs):
            if video_idx < len(video_paths):
                clip = mpe.VideoFileClip(video_paths[video_idx])
            else:
                # create blank clip matching size and duration of last clip processed.
                clip = mpe.ColorClip(clip.size, (0, 0, 0), duration=clip.duration)

            if labels is not None:
                label = labels[video_idx]

                txt_clip = mpe.TextClip(label, fontsize=40, color='white')
                txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration)
                clip = mpe.CompositeVideoClip([clip, txt_clip])

            video_grid[row][col] = clip.resize(width=int(clip.size[0]/cols))

    final_clip = mpe.clips_array(video_grid)
    final_clip.audio = video_grid[0][0].audio
    return final_clip


if __name__ == "__main__":
    parsed_args = parse_args()

    num_videos = len(parsed_args.input_videos)

    num_rows = parsed_args.rows
    num_cols = parsed_args.cols if parsed_args.cols is not None else num_videos // num_rows

    clip = create_video_panel(parsed_args.input_videos, num_rows, num_cols, parsed_args.labels)
    clip.write_videofile(parsed_args.output_path)