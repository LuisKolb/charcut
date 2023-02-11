import os


#output = os.system(f'python charcut.py -e drew_LULW sample-data/human.txt,sample-data/mt.txt -n')
#
#print(output)


from charcut import run_on, load_input_files
import sys
import argparse

args = argparse.Namespace(file_pair=['sample-data/human.txt,sample-data/mt.txt'], src_file=None, match_size=3, alt_norm=True, echo_string ='1')



r = run_on(load_input_files(args), args)
print(r)