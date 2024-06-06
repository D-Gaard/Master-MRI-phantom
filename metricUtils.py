#file for various stuff for distance metrics and their vissualization
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.fft import fftfreq, fft

COLORS = ["red","green","blue","red","green","blue"]
ORDER = ["X-translation","Y-translation","Z-translation","X-rotation","Y-rotation","Z-rotation"]
SHORTORDER = ["X-trans","Y-trans","Z-trans","X-rot","Y-rot","Z-rot"]
GENDER = ["female","female","female","female","female","male","male","male","male","male"]
AGE = [9,9,9,10,10,9,9,9,10,10]
WIDTH = 10
FORMATER =  {'float': lambda x: f" {x:>{WIDTH-1}.3f}" if x >= 0 else f"{x:>{WIDTH}.3f}"}
FORMATED_SHORTORDER = "[" +' '.join([f"{s:>{WIDTH}s}" for s in SHORTORDER]) + "]"

#plot 1 testperson
def plot_one_tp(tp,person_num,style="combined"):
  frame_idxs = [x for x in range(tp.shape[0])]
  if style == "combined":
    plt.figure(figsize=(12,6))
    plt.title(f"Capture sequence for person {person_num} ({AGE[person_num]} yo {GENDER[person_num]})")
    for i in range(6):
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
      else:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i])
    plt.legend()
    plt.grid()
    plt.ylabel("Translation [mm]/Rotation [$\degree$]")
    plt.xlabel("Frames")
    plt.show()

  elif style == "split":
    plt.figure(figsize=(20,10))
    plt.suptitle(f"Capture sequence for person {person_num} ({AGE[person_num]} yo {GENDER[person_num]})")
    for i in range(6):
      plt.subplot(2,3,i+1)
      plt.title(f"{ORDER[i]}")
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
        plt.ylabel("Rotation [$\degree$]")
      else:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i])
        plt.ylabel("Translation [mm]")
      #plt.legend()
      plt.grid()
      plt.xlabel("Frames")
    plt.show()

#plot two testperson datasets for comparison
def plot_two_tp(tp,tp2,person_num,titles,style="combined"):
  frame_idxs = [x for x in range(tp.shape[0])]
  min_max_offset = 0.2
  if style == "combined":
    plt.figure(figsize=(22,8))
    plt.suptitle(f"Capture sequence for person {person_num} ({AGE[person_num]} yo {GENDER[person_num]})", fontsize=24)
    plt.subplot(1,2,1)
    plt.title(f"{titles[0]}", fontsize=24)
    for i in range(6):
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
      else:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i])
    plt.legend(fontsize=20)
    plt.grid()
    plt.ylabel("Translation [mm]/Rotation [$\degree$]", fontsize=24)
    plt.xlabel("Frames", fontsize=24)
    plt.ylim((np.min((tp,tp2))-min_max_offset,np.max((tp,tp2))+min_max_offset))
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()

    plt.subplot(1,2,2)
    plt.title(f"{titles[1]}", fontsize=24)
    for i in range(6):
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, tp2[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
      else:
        plt.plot(frame_idxs, tp2[:,i], label=ORDER[i],c = COLORS[i])
    plt.legend(fontsize=20)
    plt.grid()
    plt.ylabel("Translation [mm]/Rotation [$\degree$]", fontsize=24)
    plt.xlabel("Frames", fontsize=24)
    plt.ylim((np.min((tp,tp2))-min_max_offset,np.max((tp,tp2))+min_max_offset))
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.show()

  elif style == "split":
    plt.figure(figsize=(20,10))
    plt.suptitle(f"Capture sequence for person {person_num} ({AGE[person_num]} yo {GENDER[person_num]})")
    for i in range(6):
      plt.subplot(2,3,i+1)
      plt.title(f"{ORDER[i]}")
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i])
        plt.plot(frame_idxs, tp2[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
        plt.ylabel("Rotation [$\degree$]")
      else:
        plt.plot(frame_idxs, tp[:,i], label=ORDER[i],c = COLORS[i])
        plt.plot(frame_idxs, tp2[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
        plt.ylabel("Translation [mm]")
      plt.legend()
      plt.grid()
      plt.xlabel("Frames")
    plt.show()

#print and compute min/max of tp group
def group_min_max(tps):
  min_ = np.amin(tps,axis=(0,1)) 
  max_ = np.amax(tps,axis=(0,1))
  with np.printoptions(formatter=FORMATER, suppress=True):
    print(f"### MIN: {min_} ###\n### MAX: {max_} ###\n")
  return min_, max_

#print and compute min/max of tp
def tp_min_max(tp):
  min_ = np.amin(tp,axis=0) 
  max_ = np.amax(tp,axis=0)
  with np.printoptions(formatter=FORMATER, suppress=True):
    print(f"### MOV: {FORMATED_SHORTORDER} ###\n### MIN: {min_} ###\n### MAX: {max_} ###\n")
  return min_, max_

#apply distance function to each of the 6 values 1 row at a time -> sum,mean,std
def calculate_distance(dist_func,tp,tp1,display=True):
  if tp.shape != tp1.shape:
    raise ValueError("Arrays tp and tp1 must have the same shape.")
  
  stats = np.zeros((3,6))

  # Iterate over each column (value) in the inner dimension
  for i in range(6):
      # Initialize arrays to store distances for each row separately
      distances_per_row = np.zeros(tp.shape[0])

      # Compute the distance metric for each row separately
      for j in range(tp.shape[0]):
          distances_per_row[j] = dist_func(tp[j, i], tp1[j, i])

      # Calculate sum, average, and standard deviation for the distances of each row
      stats[0, i] = np.sum(distances_per_row)
      stats[1, i] = np.mean(distances_per_row)
      stats[2, i] = np.std(distances_per_row)
  
  if display:
    with np.printoptions(formatter=FORMATER, suppress=True):
      print(f"### MOV: {FORMATED_SHORTORDER} ###\n### SUM: {stats[0]} ###\n### AVG: {stats[1]} ###\n### STD: {stats[2]} ###\n")
  return stats

#L2 - euclidian dist
def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y)**2))


#calculate distance function acrros a group of tps using calculate_distance
def calculate_distances_across_pairs(distance_func, tps, tp1s,display=True,display_inner=False):
  if tps.shape != tp1s.shape:
        raise ValueError("Arrays tps and tp1s must have the same shape.")
  # Initialize arrays to store sum, average, and standard deviation across all pairs
  sums = np.zeros((tps.shape[0], 6))
  averages = np.zeros((tps.shape[0], 6))
  stds = np.zeros((tps.shape[0], 6))

  # Iterate over each pair
  for i in range(tps.shape[0]):
      stats = calculate_distance(distance_func, tps[i], tp1s[i],display=display_inner)
      sums[i] = stats[0]
      averages[i] = stats[1]
      stds[i] = stats[2]

  # Aggregate the results across all pairs
  total_sum = np.mean(sums, axis=0)
  total_average = np.mean(averages, axis=0)
  total_std = np.mean(stds, axis=0)

  if display:
    with np.printoptions(formatter=FORMATER, suppress=True):
      print(f"### MEAN MOV: {FORMATED_SHORTORDER} ###\n### MEAN SUM: {total_sum} ###\n### MEAN AVG: {total_average} ###\n### MEAN STD: {total_std} ###\n")

  return np.vstack((total_sum, total_average, total_std))

#corelation between each movement for 2 datasets
def calculate_corelation_matrix(tp1,tp2,tp=-1,display=True):
  cors = []
  for i in range(6):
    correlation_matrix_= np.corrcoef(tp1[:,i], tp2[:,i])
    cors.append(correlation_matrix_)

    if display:
      if i == 0:
        print(f"### COR TP{tp} ###")
      print(f"### {ORDER[i]} ###\n {correlation_matrix_} \n")
  return cors

# Compute correlation matrix and p-values, also return significance
def calculate_6x6_corelation(data,pval = 0.05,display=True):
  reshaped_data = np.reshape(data, (data.shape[0]*data.shape[1], 6))
  corr_matrix_data = np.zeros((6, 6))
  p_values_data = np.zeros((6, 6))

  for i in range(6):
    for j in range(6):
        corr, p_value = pearsonr(reshaped_data[:, i], reshaped_data[:, j])
        corr_matrix_data[i, j] = corr
        p_values_data[i, j] = p_value

  significant_corr_matrix_data = np.where(p_values_data < pval, corr_matrix_data, np.nan)
  if display:
    with np.printoptions(formatter=FORMATER, suppress=True):
      print(f" {FORMATED_SHORTORDER} \n### CORELATION: ###\n {corr_matrix_data} \n### P-Values ###\n {p_values_data} \n")

  return corr_matrix_data, p_values_data, significant_corr_matrix_data


#Compute correlation matrix and p-values between two datasets, also return significance
def calculate_6x6_corelation_pairwise(data1,data2, pval = 0.05,display=True):
  reshaped_data1 = np.reshape(data1, (data1.shape[0]*data1.shape[1], 6))
  reshaped_data2 = np.reshape(data2, (data2.shape[0]*data2.shape[1], 6))
  corr_matrix_data = np.zeros((6, 6))
  p_values_data = np.zeros((6, 6))

  for i in range(6):
    for j in range(6):
        corr, p_value = pearsonr(reshaped_data1[:, i], reshaped_data2[:, j])
        corr_matrix_data[i, j] = corr
        p_values_data[i, j] = p_value

  significant_corr_matrix_data = np.where(p_values_data < pval, corr_matrix_data, np.nan)
  if display:
    with np.printoptions(formatter=FORMATER, suppress=True):
      print(f" {FORMATED_SHORTORDER} \n### CORELATION: ###\n {corr_matrix_data} \n### P-Values ###\n {p_values_data} \n")

  return corr_matrix_data, p_values_data, significant_corr_matrix_data


# Plot 6x6 corelation matrix:
def plot_corelations(significant1,significant2,title=["ABCD","Step20"],sup=""):
  fig, axs = plt.subplots(1, 2, figsize=(15, 10))
  # Plot for data1
  im1 = axs[0].imshow(significant1, cmap='seismic', vmin=-1, vmax=1)
  for i in range(6):
    for j in range(6):
        if not np.isnan(significant1[i, j]):
            axs[0].text(j, i, f'{significant1[i, j]:.2f}',
                        ha='center', va='center', color='black',fontweight='bold', fontsize=16)
            
  axs[0].set_title(f'Significant Correlation Matrix p=0.05 ({title[0]})', fontsize=20)
  axs[0].set_xticks(np.arange(6))
  axs[0].set_yticks(np.arange(6))
  axs[0].set_xticklabels(SHORTORDER, fontsize=16)
  axs[0].set_yticklabels(SHORTORDER, fontsize=16)
  plt.colorbar(im1, ax=axs[0],fraction=0.046, pad=0.04)

  # Plot for data2
  im2 = axs[1].imshow(significant2, cmap='seismic', vmin=-1, vmax=1)
  for i in range(6):
      for j in range(6):
          if not np.isnan(significant2[i, j]):
              axs[1].text(j, i, f'{significant2[i, j]:.2f}',
                          ha='center', va='center', color='black', fontweight='bold', fontsize=16)

  axs[1].set_title(f'Significant Correlation Matrix p=0.05 ({title[1]})', fontsize=20)
  axs[1].set_xticks(np.arange(6))
  axs[1].set_yticks(np.arange(6))
  axs[1].set_xticklabels(SHORTORDER, fontsize=16)
  axs[1].set_yticklabels(SHORTORDER, fontsize=16)
  plt.colorbar(im2, ax=axs[1],fraction=0.046, pad=0.04)

  plt.tight_layout()

  if sup != "":
    plt.suptitle(sup,fontsize=20)
  plt.show()


#calculate the corelation between two datasets for every match
#thus the first 10 cols will be for each tp, and the 11 wil be the combined (if you pass a 10 tp dataset)
def calculate_combined_correlation(data1, data2, pval=0.05, display=True):
  outer_dims = data1.shape[0]
  inner_dims = data1.shape[2]
  step = data1.shape[1]

  reshaped_data1 = np.reshape(data1, (outer_dims*step, inner_dims))
  reshaped_data2 = np.reshape(data2, (outer_dims*step, inner_dims))

  combined_corr_matrix_data = np.zeros((inner_dims, outer_dims + 1))
  combined_p_values_data = np.zeros((inner_dims, outer_dims + 1))
  significant_corr_matrix_data = np.zeros((inner_dims, outer_dims + 1))
  print(combined_corr_matrix_data.shape)

  # Compute correlations for each inner dimension without reshaping
  for i in range(outer_dims):
    for j in range(inner_dims):
      corr, p_value = pearsonr(data1[i,:, j], data2[i,:, j])
      combined_corr_matrix_data[j, i] = corr
      combined_p_values_data[j, i] = p_value

  for i in range(inner_dims):
    corr, p_value = pearsonr(reshaped_data1[:, i], reshaped_data2[:, i])
    combined_corr_matrix_data[i, outer_dims] = corr
    combined_p_values_data[i, outer_dims] = p_value

  significant_corr_matrix_data = np.where(combined_p_values_data < pval, combined_corr_matrix_data, np.nan)
  
  if display:
    with np.printoptions(formatter=FORMATER, suppress=True,linewidth=140):
      print("### COMBINED CORRELATION MATRIX ###\n", combined_corr_matrix_data)
      print("### COMBINED P-VALUES MATRIX ###\n", combined_p_values_data)
      print("### SIGNIFICANT CORRELATION MATRIX ###\n", significant_corr_matrix_data)

  return combined_corr_matrix_data, combined_p_values_data, significant_corr_matrix_data

#plot 6x11 corelation matrix diagonals:
def plot_6x11_corelation(significant):
  fig, ax = plt.subplots(figsize=(10, 8))
  im = ax.imshow(significant, cmap='seismic', vmin=-1, vmax=1)

  for i in range(6):
      for j in range(11):
          if not np.isnan(significant[i, j]):
              ax.text(j, i, f'{significant[i, j]:.2f}',
                      ha='center', va='center', color='black', fontweight='bold', fontsize=12)

  ax.set_title('Significant Correlation Matrix Diagonals p=0.05', fontsize=20)
  ax.set_xticks(np.arange(11))
  ax.set_xticklabels(['TP0', 'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7', 'TP8', 'TP9', 'COMBINED'], fontsize=12, rotation=45)
  ax.set_yticks(np.arange(6))
  ax.set_yticklabels(SHORTORDER, fontsize=12)

  plt.colorbar(im, ax=ax, fraction=0.046*6/11, pad=0.04)
  plt.tight_layout()
  plt.show()


#plot 6x3 corelation matrix diagonals:
def plot_6x3_corelation(significant):
  fig, ax = plt.subplots(figsize=(10, 8))
  im = ax.imshow(significant, cmap='seismic', vmin=-1, vmax=1)

  for i in range(6):
      for j in range(3):
          if not np.isnan(significant[i, j]):
              ax.text(j, i, f'{significant[i, j]:.2f}',
                      ha='center', va='center', color='black', fontweight='bold', fontsize=16)

  ax.set_title('Significant Correlation Matrix Diagonals p=0.05', fontsize=20)
  ax.set_xticks(np.arange(3))
  ax.set_xticklabels(['TP2', 'TP7','COMBINED'], fontsize=16, rotation=45)
  ax.set_yticks(np.arange(6))
  ax.set_yticklabels(SHORTORDER, fontsize=16)

  plt.colorbar(im, ax=ax, fraction=0.046*6/3, pad=0.04)
  plt.tight_layout()
  plt.show()


#calculate and plot frequency spectrum of two datasets:
def calculate_powerspectrum(data1,data2,labels=["ABCD","Step20"],ymin = 0.05, ymax = 250,display=True):
  #reshaped_data1 = np.reshape(data1, (10*380, 6))
  #reshaped_data2 = np.reshape(data2, (10*380, 6))
  fft_data1 = np.fft.fft(data1, axis=1)
  fft_data2 = np.fft.fft(data2, axis=1)

  # Frequency axis
  N = data1.shape[1]  # Length of the signal
  freq = np.fft.fftfreq(N,1.25) #0.8s pr value

  if display:  
    # Plotting
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    # Plot FFT for each dimension
    plt.suptitle("Average powerspectrum for each DOF (abs(fft))", fontsize=20)
    for i in range(6):
        ax = axs[i // 3, i % 3]
        ax.plot(freq[:N//2], np.abs(fft_data1[:, :N//2, i]).mean(axis=0), label=labels[0])
        ax.plot(freq[:N//2], np.abs(fft_data2[:, :N//2, i]).mean(axis=0), label=labels[1])
        ax.set_title(f'{ORDER[i]}', fontsize=16)
        ax.set_xlabel('Frequency [Hz]', fontsize=16)
        ax.set_ylabel('Amplitude (log)', fontsize=16)
        ax.set_yscale('log')
        ax.set_ylim(ymin,ymax)
        ax.legend(fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=16)
    plt.tight_layout()
    plt.show()
  return fft_data1,fft_data2,freq


#plot the isolated moves
def plot_isolated_moves(iso,title="20step",style="combined"):
  frame_idxs = [x for x in range(iso.shape[0])]
  if style == "combined":
    plt.figure(figsize=(12,6))
    plt.title(f"Isolated moves in the range [-10,10] with 0.5 increments ({title})",fontsize=20)
    for i in range(6):
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, iso[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
      else:
        plt.plot(frame_idxs, iso[:,i], label=ORDER[i],c = COLORS[i])
    plt.legend(fontsize=20,bbox_to_anchor=(1.01, 0.5), loc='center left')
    plt.grid()
    plt.ylabel("Translation [mm]/Rotation [$\degree$]",fontsize=20)
    plt.xlabel("Frames",fontsize=20)
    #plt.ylim((-10,10))
    plt.show()
  if style == "split":
    plt.figure(figsize=(20,10))
    plt.suptitle(f"Isolated moves in the range [-10,10] with 0.5 increments ({title})")
    for i in range(6):
      plt.subplot(2,3,i+1)
      plt.title(f"{ORDER[i]}")
      if "rot" in ORDER[i]:
        plt.plot(frame_idxs, iso[:,i], label=ORDER[i],c = COLORS[i], linestyle = "--")
        plt.ylabel("Rotation [$\degree$]")
      else:
        plt.plot(frame_idxs, iso[:,i], label=ORDER[i],c = COLORS[i])
        plt.ylabel("Translation [mm]")
      #plt.legend()
      plt.grid()
      plt.xlabel("Frames")
    plt.show()

#compute the maximal for each movement type change in a group of tps:
def compute_maximal_change(tps,display=True):
  diff = np.diff(tps, axis=1)
    
  max_change = np.max(np.abs(diff), axis=(0, 1))

  if display:
    with np.printoptions(formatter=FORMATER, suppress=True):
      print(f"### MOV:       {FORMATED_SHORTORDER} ###\n### MAXCHANGE: {max_change} ###\n")
  return max_change