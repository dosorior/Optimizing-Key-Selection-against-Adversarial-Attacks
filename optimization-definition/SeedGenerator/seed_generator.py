import os
from collections import defaultdict
import numpy as np
from scipy.spatial import distance
from utils import HelperFunctions
import random
from joblib import parallel_backend, Parallel, delayed
import multiprocessing
import csv

def compareToDistance(positive, negative, pos_info, negative_info):

    value = distance.sqeuclidean(positive, negative)

    return (np.round(value,4), pos_info, negative_info)

class Seed_Generator:

    def __init__(self, t_seed_selection, t_level_morph,output):

        self.t_seed_selection = t_seed_selection

        self.t_level_morph = t_level_morph
        
        self.enrol = {}

        self.search = {}

        self.demographic_info = False

        self.enrol_female_p = {}

        self.enrol_male_m = {}

        self.output = output


   

    def __saving_info(self,list_total_info):

        print("Saving csv!")

        with open(self.output,'w',newline='') as file:

            fieldnames = ['score','namePos','nameNeg','sessionNum', 'idSubject','SexNeg','SexPos']

            writer_info = csv.DictWriter(file,fieldnames=fieldnames)

            writer_info.writeheader()

            for element_i in list_total_info:

                results_comp= element_i[0]

                writer_info.writerow({'score':results_comp[0],'namePos':results_comp[1],'nameNeg':results_comp[2],'sessionNum':element_i[2],'idSubject':element_i[1],'SexNeg':element_i[3],'SexPos':element_i[4]})


    def __saving_info_random(self,list_total_info):

        print("Saving csv!")

        with open(self.output,'w',newline='') as file:

            fieldnames = ['score','namePos','nameNeg','sessionNum', 'idSubject','SexNeg','SexPos']

            writer_info = csv.DictWriter(file,fieldnames=fieldnames)

            writer_info.writeheader()

            for element_i in list_total_info:

                writer_info.writerow({'score':element_i[0],'namePos':element_i[1],'nameNeg':element_i[2],'sessionNum':element_i[3],'idSubject':element_i[4],'SexNeg':element_i[5],'SexPos':element_i[6]})


    def saving_info_search(self,out):

        with open(out,'w',newline='') as file:

            fieldnames = ['id','nameProbe','SessionNum']

            writer_info = csv.DictWriter(file,fieldnames=fieldnames)

            writer_info.writeheader()

            for element_i in self.search:

                list_prob = self.search[element_i]

                counter = 0

                for p in list_prob:

                    counter+=1

                    writer_info.writerow({'id':element_i,'nameProbe':p.stem,'SessionNum':counter})


    def selecting_seed_morph(self,negatives):
        
        if self.t_level_morph == 'signal': #applying criteria for morphing at the signal-level

            if self.t_seed_selection == 'distance': #compare against all negatives and select distance most disimilar, statistics on a top-20 was selected

                #loading negatives samples
                negative_list = list([(f.stem, f, np.load(f)[0]) for f in negatives])

                list_total_instances = []

                list_total_session = []

                list_total_positive = []

                list_total_negative = []

                list_total_scores = []

                list_total_info = []

                counter_identity = 0

                for ref_id in self.enrol: #for each identity 

                    counter_identity+=1
                    
                    print("Identity {}".format(counter_identity))
   
                    list_samples_session = self.enrol[ref_id]

                    list_samples_session.sort()

                    counter_sample = 0

                    for session_s in list_samples_session: #iterate for each session per identity

                        counter_sample+=1

                        # print("Sample{}".format(counter_sample))

                        number_s = counter_sample

                        list_session = [number_s]*100

                        list_sex_f = ['-']*100

                        list_sex_m = ['-']*100

                        list_instances = [session_s.parent.name]*100

                        feat_session_e = np.load(session_s)[0]
                            
                        results = Parallel(n_jobs=multiprocessing.cpu_count() - 1)(delayed(compareToDistance)(feat_session_e, f, session_s.stem, n) for n, p, f in negative_list)

                        results.sort(key=lambda a: a[0], reverse = True)  #most disimilar

                        pairs_type_neg_comp = results[0:100] #top 100 was selected

                        total_info = list(zip(pairs_type_neg_comp,list_instances,list_session,list_sex_f,list_sex_m)) #structure: sorted score,name_positive,name_neative,#_session,id_subject

                        list_total_info = [*list_total_info,*total_info]
                
                ####Saving in csv all the info####
                self.__saving_info(list_total_info)
                        
            if self.t_seed_selection == 'random': #compare against all negatives and select distance most disimilar, statistics on a top-20 was selected

               #loading negatives samples
                negative_list = list([(f.stem, f, np.load(f)[0]) for f in negatives])

                list_total_instances = []

                list_total_session = []

                list_total_positive = []

                list_total_negative = []

                list_total_scores = []

                list_total_info = []

                counter_identity = 0

                random_data = {}

                random_data = defaultdict(list)

                for ref_id in self.enrol: #for each identity 

                    counter_identity+=1
                    
                    print("Identity {}".format(counter_identity))
   
                    list_samples_session = self.enrol[ref_id]

                    list_samples_session.sort()

                    counter_sample = 0

                    for session_s in list_samples_session: #iterate for each session per identity

                        counter_sample+=1

                        # print("Sample{}".format(counter_sample))

                        number_s = counter_sample

                        feat_session_e = np.load(session_s)[0]
                            
                        results = Parallel(n_jobs=multiprocessing.cpu_count() - 1)(delayed(compareToDistance)(feat_session_e, f, session_s.stem, n) for n, p, f in negative_list)

                        random.shuffle(results)

                        best_res = []

                        for res in results:

                            if res[2] in random_data:

                                pass

                            else:

                                random_data[res[2]].append(res)

                                tuple_data = (res[0], res[1], res[2])

                                best_res = tuple_data

                                break

                        value = best_res[0].T

                        pos_name =  best_res[1]

                        neg_name = best_res[2]

                        tupla_info = [value,pos_name,neg_name,ref_id,counter_sample,'-','-'] #structure: sorted score,name_positive,name_neative,#_session,id_subject,sex_n_male,sex_p_female
                        
                        list_total_info.append(tupla_info)
                
                self.__saving_info_random(list_total_info)

                    
            
                ####Saving in csv all the info####

            if self.t_seed_selection == 'sf_distance':

                list_total_info = []

                self.demographic_info = True

                id_female_p, id_male_p = HelperFunctions.organizing_db_positives_by_demograhic_info(self.enrol)

                dirs_female_p,dirs_male_p = HelperFunctions.gettingdirs(id_female_p,id_male_p,self.enrol)

                self.enrol_female_p = dirs_female_p

                self.enrol_male_p = dirs_male_p

                id_female_n, id_male_n = HelperFunctions.organizing_db_negatives_by_demograhic_info(negatives)

                dirs_female_n, dirs_male_n = HelperFunctions.gettingdirs_negative(id_female_n,id_male_n,negatives)

                negative_list_m = list([(f.stem, f, np.load(f)[0]) for f in dirs_male_n])

                negative_list_f =  list([(f.stem, f, np.load(f)[0]) for f in dirs_female_n])

                list_total_instances_f = []

                list_total_session_f = []

                list_total_positive_f = []

                list_total_negative_f = []

                list_total_scores_f = []

                counter_id = 0

                for ref_id in dirs_female_p: #starting with females to be morphed against most dissimilar in the males

                    counter_id+=1

                    print("Identity {}".format(counter_id))

                    list_samples_session = self.enrol_female_p[ref_id]

                    list_samples_session.sort()

                    counter_sample = 0

                    for session_s in list_samples_session: #iterate for each session per identity

                        counter_sample+=1

                        number_s = counter_sample

                        list_sex_n = ['m']*100

                        list_sex_p = ['f']*100

                        list_session = [number_s]*100

                        list_instances = [ref_id]*100

                        feat_session_e = np.load(session_s)[0]

                        results = Parallel(n_jobs=multiprocessing.cpu_count() - 1)(delayed(compareToDistance)(feat_session_e, f, session_s.stem, n) for n, p, f in negative_list_m)

                        results.sort(key=lambda a: a[0], reverse = True)  #most disimilar

                        pairs_type_neg_comp = results[0:100] #top 100 was selected

                        total_info = list(zip(pairs_type_neg_comp,list_instances,list_session,list_sex_n,list_sex_p)) #structure: sorted score,name_positive,name_neative,#_session,id_subject,sex_n_male,sex_p_female

                        list_total_info = [*list_total_info,*total_info]
                        
                 ####Saving in csv all the info####
                # self.__saving_info(list_total_info)

                list_total_instances_m = []

                list_total_session_m = []

                list_total_positive_m = []

                list_total_negative_m = []

                list_total_scores_m = []

                counter_id = 0

                for ref_id in dirs_male_p: #starting with males to be morphed against most dissimilar in the females

                    counter_id+=1

                    print("Identity second group{}".format(counter_id))

                    list_samples_session = self.enrol_male_p[ref_id]

                    list_samples_session.sort()

                    counter_sample = 0

                    for session_s in list_samples_session: #iterate for each session per identity

                        counter_sample+=1

                        number_s = counter_sample

                        list_session = [number_s]*100

                        list_sex_n = ['f']*100

                        list_sex_p = ['m']*100

                        list_instances = [ref_id]*100

                        feat_session_e = np.load(session_s)[0]

                        results = Parallel(n_jobs=multiprocessing.cpu_count() - 1)(delayed(compareToDistance)(feat_session_e, f, session_s.stem, n) for n, p, f in negative_list_f)

                        results.sort(key=lambda a: a[0], reverse = True)  #most disimilar

                        pairs_type_neg_comp = results[0:100] #top 100 was selected

                        total_info = list(zip(pairs_type_neg_comp,list_instances,list_session,list_sex_n,list_sex_p)) #structure: sorted score,name_positive,name_neative,#_session,id_subject,sex male

                        list_total_info = [*list_total_info,*total_info]
                        
                ####Saving in csv all the info####
                self.__saving_info(list_total_info)

            
            if self.t_seed_selection == 'sf_random':

                list_total_info = []

                self.demographic_info = True

                id_female_p, id_male_p = HelperFunctions.organizing_db_positives_by_demograhic_info(self.enrol)

                dirs_female_p,dirs_male_p = HelperFunctions.gettingdirs(id_female_p,id_male_p,self.enrol)

                self.enrol_female_p = dirs_female_p

                self.enrol_male_p = dirs_male_p

                id_female_n, id_male_n = HelperFunctions.organizing_db_negatives_by_demograhic_info(negatives)

                dirs_female_n, dirs_male_n = HelperFunctions.gettingdirs_negative(id_female_n,id_male_n,negatives)

                negative_list_m = list([(f.stem, f, np.load(f)[0]) for f in dirs_male_n])

                negative_list_f =  list([(f.stem, f, np.load(f)[0]) for f in dirs_female_n])

                list_total_instances_f = []

                list_total_session_f = []

                list_total_positive_f = []

                list_total_negative_f = []

                list_total_scores_f = []

                random_data = {}

                random_data = defaultdict(list)

                counter_id = 0

                for ref_id in dirs_female_p: #starting with females to be morphed against most dissimilar in the males

                    counter_id+=1

                    print("Identity {}".format(counter_id))

                    list_samples_session = self.enrol_female_p[ref_id]

                    list_samples_session.sort()

                    counter_sample = 0

                    for session_s in list_samples_session: #iterate for each session per identity

                        counter_sample+=1

                        number_s = counter_sample

                        feat_session_e = np.load(session_s)[0]

                        results = Parallel(n_jobs=multiprocessing.cpu_count() - 1)(delayed(compareToDistance)(feat_session_e, f, session_s.stem, n) for n, p, f in negative_list_m)

                        random.shuffle(results)

                        best_res = []

                        for res in results:

                            if res[2] in random_data:

                                pass

                            else:

                                random_data[res[2]].append(res)

                                tuple_data = (res[0], res[1], res[2])

                                best_res = tuple_data

                                break

                        value = best_res[0].T

                        pos_name =  best_res[1]

                        neg_name = best_res[2]

                        tupla_info = [value,pos_name,neg_name,ref_id,counter_sample,'m','f'] #structure: sorted score,name_positive,name_neative,#_session,id_subject,sex_n_male,sex_p_female
                        
                        list_total_info.append(tupla_info)
                        
    

                list_total_instances_m = []

                list_total_session_m = []

                list_total_positive_m = []

                list_total_negative_m = []

                list_total_scores_m = []

                random_data_m = {}

                random_data_m = defaultdict(list)

                counter_id = 0

                for ref_id in dirs_male_p: #starting with males to be morphed against most dissimilar in the females

                    counter_id+=1

                    print("Identity second group{}".format(counter_id))

                    list_samples_session = self.enrol_male_p[ref_id]

                    list_samples_session.sort()

                    counter_sample = 0

                    for session_s in list_samples_session: #iterate for each session per identity

                        counter_sample+=1

                        number_s = counter_sample

                        feat_session_e = np.load(session_s)[0]

                        results = Parallel(n_jobs=multiprocessing.cpu_count() - 1)(delayed(compareToDistance)(feat_session_e, f, session_s.stem, n) for n, p, f in negative_list_f)

                        random.shuffle(results)

                        best_res = []

                        for res in results:

                            if res[2] in random_data_m:

                                pass

                            else:

                               random_data[res[2]].append(res)

                               tuple_data = (res[0], res[1], res[2])

                               best_res = tuple_data

                               break

                        value = best_res[0].T

                        pos_name =  best_res[1]

                        neg_name = best_res[2]

                        tupla_info = [value,pos_name,neg_name,ref_id,counter_sample,'f','m'] #structure: sorted score,name_positive,name_neative,#_session,id_subject,sex_n_male,sex_p_female
                        
                        list_total_info.append(tupla_info)
                        
                ####Saving in csv all the info####
                self.__saving_info_random(list_total_info)



    
    def prepare_system(self,references,probes):

        self.enrol = defaultdict(list)

        self.enrol = references

        self.search = probes



