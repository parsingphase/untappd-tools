#!/usr/bin/env python

import argparse
import json
import numpy
import re

from matplotlib import cm, colors, pyplot
from typing import Optional
from utils import file_contents
from wordcloud import WordCloud


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Create a word cloud from your checkin descriptions',
    )
    parser.add_argument('source', help='Path to source file (export.json)')
    parser.add_argument('--output', required=False, help='Path to output file, STDOUT if not specified')
    args = parser.parse_args()
    return args


def run_cli():
    args = parse_cli_args()
    source = args.source
    dest = args.output
    generate_cloud_image(source, dest)


def generate_cloud_image(source: str, dest: Optional[str] = None):
    source_data = json.loads(file_contents(source))
    comments = [
        re.sub('\[.*\]', '', checkin['comment']).lower() for checkin in source_data
        if checkin['comment'] is not None and checkin['comment'] != ''
    ]
    # post-filter anything we've removed all text from
    comments = [comment for comment in comments if comment != '']

    beer_colours = truncate_colormap(cm.get_cmap('YlOrBr'), 0.4, 1.0)  # YlOrBr, copper, autumn
    cloud = WordCloud(width=800, height=800,
                      background_color='white',
                      min_font_size=10,
                      colormap=beer_colours,
                      ).generate(' '.join(comments))
    # plot the WordCloud image
    pyplot.figure(figsize=(8, 8), facecolor=None)
    pyplot.imshow(cloud)
    pyplot.axis("off")
    pyplot.tight_layout(pad=0)
    if dest:
        pyplot.savefig(dest, format=dest.split('.')[-1])
    else:
        pyplot.show()


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(numpy.linspace(minval, maxval, n)))
    return new_cmap


if __name__ == '__main__':
    run_cli()