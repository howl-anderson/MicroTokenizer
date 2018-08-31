#!/usr/bin/env python
import os

from MicroTokenizer.train.train import train

current_dir = os.path.dirname(os.path.abspath(__file__))

input_file_list = [os.path.join(current_dir, 'data.txt')]
output_dir = [os.path.join(current_dir, '../MicroTokenizer/model_data')]

train(input_file_list, output_dir)
