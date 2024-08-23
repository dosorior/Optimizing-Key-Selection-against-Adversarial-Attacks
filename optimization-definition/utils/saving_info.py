import argparse
import os

parser = argparse.ArgumentParser(description='Saving info')

parser.add_argument('--dest', '-d',
                    dest="dest",
                    type=str,
                    help='data to classify')

parser.add_argument('--out', '-o',
                    dest="out",
                    type=str,
                    help='output to save statistics')

args= parser.parse_args()

ids = os.listdir(args.dest)

file = os.path.join(args.out,'VGGFace2_id.txt')

with open(file,'w') as f1:

    for id in ids:

        f1.write('{} \n'.format(id))

