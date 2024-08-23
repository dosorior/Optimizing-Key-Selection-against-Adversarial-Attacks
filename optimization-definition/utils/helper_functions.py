import os
from collections import defaultdict
from pathlib import Path
import pandas as pd

def prepare_vgg_face_2_positive(path_db,faces_imgs):
    """prepare vggface2 db as positive"""

    dataset_ref = {}

    dataset_ref = defaultdict(list)
    
    dataset_prob = {}

    dataset_prob = defaultdict(list)

    key = " "

    for id in faces_imgs:

        list_samples = os.listdir(os.path.join(path_db,id))

        for sample in list_samples:

            if '1' in sample.split('_')[1]: #considering the image as ref if this contains 1

                key = id

                if key in dataset_ref:

                    dataset_ref[key].append(Path(path_db,id,sample))
                
                else:

                    dataset_ref[key] = [Path(path_db,id,sample)]
            
            else:

                if '2' in sample.split('_')[1]: #considering the image as ref if this contains 2

                    key = id

                if key in dataset_prob:

                    dataset_prob[key].append(Path(path_db,id,sample))
                
                else:

                    dataset_prob[key] = [Path(path_db,id,sample)]

        
    return dataset_ref,dataset_prob


def prepare_lfw_negative(path_db,faces_imgs):
    """prepare LFW db as negative"""

    list_negatives= []

    for id in faces_imgs:

        list_negatives.append(id)
        
    return list_negatives

    
def preprocessing_db_ref_probes_neg_old(path_db_positive,namedb_positive,path_db_negative,namedb_negative):
    """Preparing input data"""

    faces_positives = os.listdir(path_db_positive)

    references = {}

    probes = {}

    negatives = {}

    if namedb_positive == 'VGGFace2': #processing VGGFace2Set

        dataset_ref,dataset_prob = prepare_vgg_face_2_positive(path_db_positive,faces_positives)

        references = dataset_ref

        probes = dataset_prob

    ####ending positive databases####
 
    faces_negatives = os.listdir(path_db_negative)

    if namedb_negative == 'LFW': #processing LFW

        dataset_negative = {}

        negatives_collection = prepare_lfw_negative(path_db_negative,faces_negatives)

        negatives = negatives_collection

    ####ending negative databases####
    
    return references,probes,negatives

def preprocessing_db_ref_probes_neg(path_db_positive,namedb_positive,path_db_negative,namedb_negative):
    """Preparing input data"""

    references = {}

    references = defaultdict(list)

    probes = {}

    probes =  defaultdict(list)

    negatives = {}

    negatives = defaultdict(list)

    dataset = {}

    dataset = defaultdict(list)

    files = list(Path(path_db_positive).rglob('*.{}'.format('npy')))

    if namedb_positive == 'VGGFace2': #processing VGGFace2Set

        key =''

        for f_path in files:

            key = f_path.parent.name

            if key in dataset:

                dataset[key].append(f_path)
                
            else:

                dataset[key] = [f_path]

        for d in dataset:

            list_samples= dataset[d]

            ref_list = list_samples[0:25]

            for r in ref_list:

                key = r.parent.name

                if key in references:

                    references[key].append(r)
                
                else:

                    references[key] = [r]
                    

            prob_list = list_samples[25:]

            for p in prob_list:

                key = p.parent.name

                if key in probes:

                    probes[key].append(p)
                
                else:

                    probes[key] = [p]
    
    faces_negatives = list(Path(path_db_negative).rglob('*.{}'.format('npy')))

    if namedb_negative == 'LFW': #processing LFW

        negatives_collection = prepare_lfw_negative(path_db_negative,faces_negatives)

        negatives = negatives_collection

    return  references, probes, negatives
    
    
def organizing_db_positives_by_demograhic_info(data):

    file_ids = 'D:\DemographicInfo\VGGFace2\VGGFace2_id.txt' #getting path

    file_demographic_info = 'D:\DemographicInfo\VGGFace2\VGGFace2_sex.txt'  #getting path

    with open(file_ids) as file_id,  open(file_demographic_info) as file_info:
        
        ids = file_id.readlines()

        ids = [id.strip() for id in ids]

        ids = list(ids)

        info_softbio = file_info.readlines()

        info_softbio = [info.strip() for info in info_softbio]

        info_softbio = list(info_softbio)

        id_info = list(zip(ids,info_softbio))

        id_female = list(map(lambda x: x[0], filter(lambda x: x[1]=='f', id_info))) #getting female

        id_male =  list(map(lambda x: x[0], filter(lambda x: x[1]=='m', id_info))) #getting male

        return id_female,id_male

    
def organizing_db_negatives_by_demograhic_info(data):

    file = 'D:\DemographicInfo\LFW\LFW_LUB.csv' #info soft-bio by sex for LFW

    data = pd.read_csv(file)

    data_info = pd.DataFrame(data, columns=['identity','gender'])

    data_id = data_info['identity']

    data_id = list(data_id)

    data_info = data_info['gender']

    data_info = list(data_info)

    info_general = list(zip(data_id,data_info))

    id_female = list(map(lambda x: x[0], filter(lambda x: x[1]=='f', info_general))) #getting female

    id_male =  list(map(lambda x: x[0], filter(lambda x: x[1]=='m', info_general))) #getting male

    return id_female,id_male


def gettingdirs(id_female,id_male,enrol):

    ref_female_dirs = []

    ref_male_dirs = []

    for e in enrol:

        list_ref = enrol[e]

        if e in id_female:

            [ref_female_dirs.append(ref_f)for ref_f in list_ref] #female
        
        else:

            [ref_male_dirs.append(ref_m)for ref_m in list_ref] #male
    
    dict_dirs_ref_f = {}

    dict_dirs_ref_f = defaultdict(list)

    dict_dirs_ref_m = {}

    dict_dirs_ref_m = defaultdict(list)

    for ref_m in ref_male_dirs:

        parent = ref_m.parent.name

        key = " "

        key = parent

        if key in dict_dirs_ref_m:

            dict_dirs_ref_m[key].append(ref_m)
        
        else:

            dict_dirs_ref_m[key] = [ref_m]
        
    for ref_f in ref_female_dirs:

        parent = ref_f.parent.name

        key = " "

        key = parent

        if key in dict_dirs_ref_f:

            dict_dirs_ref_f[key].append(ref_f)
        
        else:

            dict_dirs_ref_f[key] = [ref_f]
    
    return dict_dirs_ref_f,dict_dirs_ref_m


def gettingdirs_negative(id_female,id_male,negative):

    ref_female_dirs = []

    ref_male_dirs = []

    counter = 0

    for n in negative:

        name = n.stem

        if name in id_female:

            ref_female_dirs.append(n)
        
        else:

            ref_male_dirs.append(n)

    return ref_female_dirs,ref_male_dirs