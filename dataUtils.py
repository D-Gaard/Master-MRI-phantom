import numpy as np
import pandas as pd
import itertools

NUM_META_ROWS = 6

#load a gridsearch dataset
def load_dataset(a,samples,stepsize,path_base,full_path):
  if full_path =="":
    path = path_base+f"phantom_{stepsize}_{samples}_{a}Accel.csv"
  else:
     path = full_path
  df = pd.read_csv(path, skiprows=NUM_META_ROWS)
  new_header = ["Frame", "Time", "X_rot","Y_rot","Z_rot","X_trans","Y_trans","Z_trans"]
  df.columns = new_header

  return df

def load_testperson(person_num,path_base):
  path = path_base+f"20_p{person_num}.csv"
  df = pd.read_csv(path, skiprows=NUM_META_ROWS)
  new_header = ["Frame", "Time", "X_rot","Y_rot","Z_rot","X_trans","Y_trans","Z_trans"]
  df.columns = new_header

  return df

def load_testperson2(person_num,path_base):
  path = path_base + f"20_p{person_num}_renorm.csv"
  df = pd.read_csv(path, skiprows=NUM_META_ROWS)
  new_header = ["Frame", "Time", "X_rot","Y_rot","Z_rot","X_trans","Y_trans","Z_trans"]
  df.columns = new_header
  return df

def load_testperson3(person_num,path_base):
  path = path_base + f"5_p{person_num}.csv"
  df = pd.read_csv(path, skiprows=NUM_META_ROWS)
  new_header = ["Frame", "Time", "X_rot","Y_rot","Z_rot","X_trans","Y_trans","Z_trans"]
  df.columns = new_header
  return df


#center the translation around 0 and make coordinate systmes match the ABCD data
def fixCoordinates(df):
  translations = ["X_trans", "Y_trans","Z_trans"]
  for t in translations:
      df[t] = df[t].subtract(df.iloc[0][t])
  columns_to_invert = ["X_rot","Z_rot","X_trans","Z_trans"]
  df.loc[:, columns_to_invert] *= -1

  return df

#extract the wanted frames from the gridsearch
def get_frames(df,samples,frame_offset,start_offset): #uses frame number instead of time
    extract = [start_offset  + frame_offset*i for i in range(1,samples+1)] 
    return df[df["Frame"].isin(extract)]

#check if rot/trans differnece between frames is low
def is_stable(frames, t_eps, r_eps):
  rot = abs(frames.iloc[:,-6:-3].max() - frames.iloc[:,-6:-3].min())
  trans = abs(frames.iloc[:,-3:].max() - frames.iloc[:,-3:].min())

  if all(t < t_eps for t in trans) and all(r < r_eps for r in rot):
    return True
  return False

#check if extracted frames are not wobling
def check_extracted_frames(df,df_extracted,spacing,t_eps,r_eps):
    bad_frames = []
    good_frames = []
    good_frames_idx = []
    ctr = 0
    for i in df_extracted["Frame"]:
        frames_2check = list(range(i-spacing,i)) #check previous frames
        df_2check = df[df["Frame"].isin(frames_2check)]
        if not is_stable(df_2check,t_eps,r_eps):
            bad_frames.append(i)
        else:
            good_frames_idx.append(ctr)
            good_frames.append(i)
        ctr += 1
    return good_frames,bad_frames,good_frames_idx


#check which frames from the gridsearch are usable (eg. not wobeling at the end)
#df = all frames
#wanted_frames = amount of frames to extract from the gidsearch data
#frame_offset = delay between gridsearch movments
#start_offset = start of gridsearch
#spacing = amount of previous frames to consider to delcare frame usable
#t_eps = translational difference allowed
#r_eps = rotational difference allowed
def getValidFrames(df,wanted_frames,frame_offset,start_offset,spacing,t_eps,r_eps):
  df_extracted = get_frames(df,wanted_frames,frame_offset,start_offset)
  valid_idx ,invalid_idx, valid_arg_idx = check_extracted_frames(df,df_extracted,spacing,t_eps,r_eps)

  print(f"TOTAL FRAMES: {len(df_extracted)} ({len(valid_idx) + len(invalid_idx)})")
  print(f"INVALID FRAMES: {len(invalid_idx)}, VALID FRAMES: {len(valid_idx)}")

  df_valid = df_extracted[df_extracted["Frame"].isin(valid_idx)]

  return df_valid, valid_arg_idx



#assumes a sample rate of 3
def getGridsearchCableLengths(stepsize):
  # Define the ranges for each number
  ranges = [
      range(-stepsize, stepsize+1,stepsize),  # Range for S1
      range(-stepsize, stepsize+1,stepsize),  # Range for S2
      range(-stepsize, stepsize+1,stepsize),  # Range for S3
      range(-stepsize, stepsize+1,stepsize),  # Range for S4
      range(-stepsize, stepsize+1,stepsize),  # Range for S5
      range(-stepsize, stepsize+1,stepsize),  # Range for S6
  ]
  combinations = list(itertools.product(*ranges))
  comb_list = list(map(list,combinations))
  return comb_list

#get all the targets coresponding to no wobble
def getValidTargets(targets,valid_idx):
   return list(map(list,np.array(targets)[valid_idx]))
   
