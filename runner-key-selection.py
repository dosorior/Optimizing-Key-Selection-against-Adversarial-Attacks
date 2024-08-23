import argparse
import os
from utils import helper_functions
from genericpath import isdir
from SeedGenerator.seed_generator import Seed_Generator
import numpy as np

parser = argparse.ArgumentParser(description='Generic runner key selection via signal and feature domain')

parser.add_argument('--input_main', '-im',
                    dest="main",
                    type=str,
                    help='dir of the directory where are all databases')


parser.add_argument('--db_po', '-pos',
                    dest="pos",
                    type=str,
                    help='name of the folder containing the positives')

parser.add_argument('--db_ne', '-neg',
                    dest="neg",
                    type=str,
                    help='name of the folder containing the negatives')


parser.add_argument('--input_positiveBD', '-ip',
                    dest="positives",
                    type=str,
                    help='name of the db for mated comparisons (i.e. positive db where are face images or face embeddings before morphing)',
                    default='VGGFace2')


parser.add_argument('--input_negativeBD','-in',
                    dest="negatives",
                    type=str,
                    help='name of the negative database (i.e. face images or face embeddings) for morphing',
                    default='LFW')

parser.add_argument('--level_morphing','-lm',
                    dest="typeM",
                    type=str,
                    help='morphing at the signal-(signal) or feature-level(feature)',
                    default='signal')


parser.add_argument('--type_selection_seed','-ts',
                    dest="typeS",
                    type=str,
                    help='definition of the type of seed selection (i.e. enum={sf_distance,sf_random,random,distance})',
                    default='random')


parser.add_argument('--key_scenario','-ks',
                    dest="keyScenario",
                    type=str,
                    help='Normal (samples of a same identity should contribute to the same key (i.e. the sample to do the morph)) and Stolen (all different identities should contribute under the same key)',
                    default='n')

parser.add_argument('--output','-o',
                    dest="output",
                    type=str,
                    help='dir of the directory where will be saved the inputs morphed')

args= parser.parse_args()

path_db_positive = os.path.join(args.main,args.pos)

path_db_negative = os.path.join(args.main,args.neg)

path_save = os.path.join(args.output,'info_morphing_{}_neg_{}_{}_{}.csv'.format(args.positives,args.negatives,args.typeM,args.typeS))

if isdir(path_db_positive) and isdir(path_db_negative):

    print("Exist databases")

    references, probes, negatives = HelperFunctions.preprocessing_db_ref_probes_neg(path_db_positive,args.positives,path_db_negative,args.negatives)

    seed_generator = Seed_Generator(args.typeS,args.typeM,path_save)

    seed_generator.prepare_system(references,probes)

    path_out_probes = os.path.join(args.output,'info_probes_{}_{}.csv'.format(args.typeM,args.typeS))

    seed_generator.saving_info_search(path_out_probes)

    seed_generator.selecting_seed_morph(negatives)
    

