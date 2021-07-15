import os

from MicroTokenizer.tools.train import train

current_dir = os.path.dirname(os.path.abspath(__file__))

input_file_list = [os.path.join(current_dir, 'data.txt')]
output_dir = os.path.join(current_dir, './model_data')

train(input_file_list, output_dir)
