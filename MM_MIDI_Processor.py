# -*- coding: utf-8 -*-
"""Meddleying MAESTRO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GrdWC0M9hvezXydE0gpp0C2ycUMIiD16

# Meddleying MAESTRO (ver 2.6)

***

## A full-featured Algorithmic Intelligence music generator with full multi-instrument MIDI support.

***

### Project Los Angeles

### Tegridy Code 2020

***

# Setup Environment, clone needed code, and install all required dependencies
"""

#@title Install all dependencies (run only once per session)



#@title Import all modules
import glob
import os
import numpy as np
import music21
from music21 import *
import pickle
import time
import math
import sys
import tqdm.auto
import secrets
import pretty_midi
#from google.colab import output, drive
import statistics
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mido import MidiFile
#from IPython.display import display, Image
import MIDI
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI
ticks_per_note = 50
ctime = 0
cev_matrix = []
cnotes_matrix = []
debug = False

#os.mkdir('./Dataset/')
#os.mkdir('./C_Dataset/')

"""# Select and download a sample MIDI dataset"""

# Commented out IPython magic to ensure Python compatibility.
#@title (Best Choice/Multi-Instrumental) Processed ready-to-use Special Tegridy Multi-Instrumental Dataset

"""# Process MIDI Dataset to MIDI Notes and MIDI Events Lists"""

#@title Please note that transpose function reduces MIDIs to Piano only. Sliding some sliders to minimum value disables slider's option. Standard MIDI timings are 400/120
full_path_to_output_dataset_to = "Meddleying-MAESTRO-Music-Dataset.data" #@param {type:"string"}
dataset_slices_length_in_notes = 2 #@param {type:"slider", min:2, max:60, step:1}
transpose_MIDIs_to_one_key = False #@param {type:"boolean"}
melody_reduction_to_slices_max_pitches = False #@param {type:"boolean"}
desired_MIDI_channel = 16 #@param {type:"slider", min:1, max:16, step:1}
flip_input_dataset = False #@param {type:"boolean"}
remove_drums = False #@param {type:"boolean"}
flip_notes = False #@param {type:"boolean"}
transpose_notes_pitch = 0 #@param {type:"slider", min:-30, max:30, step:1}
remove_random_notes = False #@param {type:"boolean"}
remove_every_randomth_note = False #@param {type:"boolean"}
remove_every_n_notes = False #@param {type:"boolean"}
remove_n_notes_per_slice = 0 #@param {type:"slider", min:0, max:7, step:1}
remove_every_nth_note = 0 #@param {type:"slider", min:0, max:7, step:1}
keep_only_notes_above_this_pitch_number = 0 #@param {type:"slider", min:0, max:127, step:1}
constant_notes_duration_time_ms = 0 #@param {type:"slider", min:0, max:800, step:100}
five_notes_per_octave_pitch_quantization = False #@param {type:"boolean"}
octave_channel_split = False #@param {type:"boolean"}
simulated_velocity_volume = 2 #@param {type:"slider", min:2, max:127, step:1}
simulated_velocity_range = 1 #@param {type:"slider", min:1, max:127, step:1}
simulated_velocity_multiplier = 1.2 #@param {type:"slider", min:0, max:2, step:0.1}
simulated_velocity_based_on_pitch = False #@param {type:"boolean"}
simulated_velocity_based_on_top_pitch = True #@param {type:"boolean"}
simulated_velocity_top_pitch_shift_pitch = 1 #@param {type:"slider", min:1, max:120, step:1}
simulated_velocity_baseline_pitch = 1 #@param {type:"slider", min:1, max:127, step:1}
simulated_velocity_chord_size_in_notes = 0 #@param {type:"slider", min:0, max:127, step:1}
reverse_output_dataset = True #@param {type:"boolean"}
combine_reversed_and_original_datasets_together = True #@param {type:"boolean"}
debug = False

os.chdir("./")

ev_matrix = []
rev_matrix = []
not_matrix = []
rnot_matrix = []
durations_matrix = []
velocities_matrix = []
files_count = 0
remnote = 0
remnote_count = 0
notes_counter = 0
every_random_note = 7
itrack = 0
prev_event = []
next_event = []
slice_events = []
slices_pitches = []
slices_events = []
slices_melody_events = []
slices_melody_pitches = []
slices_counter = 0
slices_count = 0
chord_counter = 0
max_event_pitch = 0

def list_average(num):
  sum_num = 0
  for t in num:
      sum_num = sum_num + t           

  avg = sum_num / len(num)
  return avg

#converts all midi files in the current folder
#converting everything into the key of C major or A minor
# major conversions

if transpose_MIDIs_to_one_key:

  majors = dict([("A-", 4),("A", 3),("B-", 2),("B", 1),("C", 0),("D-", -1),("D", -2),("E-", -3),("E", -4),("F", -5),("G-", 6),("G", 5)])
  minors = dict([("A-", 1),("A", 0),("B-", -1),("B", -2),("C", -3),("D-", -4),("D", -5),("E-", 6),("E", 5),("F", 4),("G-", 3),("G", 2)])


  os.chdir("./Dataset/")

  print('Converting all possible MIDI files to C Key.')
  print('This may take a while. Please wait...')

  for file in tqdm.auto.tqdm(glob.glob("*.mid")):
    try:
      score = music21.converter.parse(file)
      key = score.analyze('key')

      #print('Detected Key:', key.tonic.name, key.mode)

      if key.mode == "major":
            halfSteps = majors[key.tonic.name]
            
      elif key.mode == "minor":
            halfSteps = minors[key.tonic.name]

      newscore = score.transpose(halfSteps)
      key = newscore.analyze('key')
      #print('Detected Key:', key.tonic.name, key.mode)
      newFileName = "./C_Dataset/C_" + file
      newscore.write('midi',newFileName)
    except:
      pass

os.chdir("./")

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

if not transpose_MIDIs_to_one_key :
  dataset_addr = "Dataset"
else:
  dataset_addr = "C_Dataset"
files = os.listdir(dataset_addr)
print('Now processing the files.')
print('Please stand-by...')

for file in tqdm.auto.tqdm(files):
    file_address = os.path.join(dataset_addr, file)
    
    score = []

    midi_file = open(file_address, 'rb')
    if debug: print('Processing File:', file_address)

    score2 = MIDI.midi2opus(midi_file.read())
    score1 = MIDI.to_millisecs(score2)
    score3 = MIDI.opus2score(score1)
    score = score3
    midi_file.close()

    if remove_drums:
      score4 = MIDI.grep(score3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15])
    else:
      score4 = score3
  
    if desired_MIDI_channel < 16:
      score = MIDI.grep(score4, [desired_MIDI_channel-1])
    else:
      score = score4
    
    itrack = 1
    while itrack < len(score):
      for event in score[itrack]:
        if event[0] == 'note':
          if flip_input_dataset:
            event[4] = 127 - event[4]

          if five_notes_per_octave_pitch_quantization:
            event[4] = int(math.floor(event[4] / 12 * 5) * 12 / 5)
          
          if octave_channel_split:
            event[4] = int((event[4] + (event[3] - 4) * 12) % (127 - 12 * 2))
          
          if simulated_velocity_volume > 2 and simulated_velocity_range > 1:
            event[5] = simulated_velocity_volume + int(secrets.randbelow(simulated_velocity_range) * simulated_velocity_multiplier)
          
          if simulated_velocity_based_on_pitch:
            if event[4] >= simulated_velocity_baseline_pitch:
              event[5] = int(simulated_velocity_volume * simulated_velocity_multiplier)
            else:
              if event[5] < simulated_velocity_baseline_pitch:
                event[5] = int(simulated_velocity_baseline_pitch * simulated_velocity_multiplier)

          if chord_counter < simulated_velocity_chord_size_in_notes:
            event[5] = int(simulated_velocity_volume * simulated_velocity_multiplier)
            chord_counter += 1
          else:
            chord_counter = 0
            simulated_velocity_volume = int(event[4] * simulated_velocity_multiplier)
          
          if simulated_velocity_based_on_top_pitch:
            if event[5] < simulated_velocity_baseline_pitch: 
              event[5] = int((max_event_pitch + simulated_velocity_top_pitch_shift_pitch) * simulated_velocity_multiplier)
            else:
              event[5] = max_event_pitch + simulated_velocity_top_pitch_shift_pitch
          
          if constant_notes_duration_time_ms > 0:
            event[2] = constant_notes_duration_time_ms
          
          if transpose_notes_pitch:
            event[4] = event[4] + transpose_notes_pitch
          
          if flip_notes:
            event[4] = 127 - event[4]

          if slices_counter != dataset_slices_length_in_notes:
            slices_counter += 1
            #remnote_count += 1
            slices_events.append(event)
            slices_pitches.append(event[4])
 
          else:
            slices_count += 1
            slices_counter = 0
            max_event_pitch = max(slices_pitches)
            max_event_index = slices_pitches.index(max_event_pitch)
            max_event = slices_events[max_event_index]
            slices_melody_events.append(max_event)
            slices_melody_pitches.append(max_event[4])
            slices_events = []
            slices_pitches = []
 
          if remove_random_notes:
            if secrets.randbelow(2) == 1:
              remnote_count += 1
            else:
              not_matrix.append(event[4])
              ev_matrix.append(event)

          if keep_only_notes_above_this_pitch_number > 0:
            if event[4] < keep_only_notes_above_this_pitch_number:
              remnote_count += 1
            else: 
              not_matrix.append(event[4])
              ev_matrix.append(event) 
              slices_events.append(event)
              slices_pitches.append(event[4])

          if remove_every_n_notes > 0:
            if remnote < remove_every_n_notes:
              remnote += 1
              remnote_count += 1
            else:
              remnote = 0
              not_matrix.append(event[4])
              ev_matrix.append(event)
              slices_events.append(event)
              slices_pitches.append(event[4])

          if remove_n_notes_per_slice > 0:
            if slices_counter == remove_n_notes_per_slice:
              not_matrix.append(event[4])
              ev_matrix.append(event)
              slices_events.append(event)
              slices_pitches.append(event[4])

            else:
              remnote_count += 1

          if remove_every_nth_note > 0:
            if remnote == remove_every_nth_note + 1:
              remnote = 0 
              remnote_count += 1
            else:
              remnote += 1
              not_matrix.append(event[4])
              ev_matrix.append(event)
              slices_events.append(event)
              slices_pitches.append(event[4])

          if remove_every_randomth_note:
            if remnote == every_random_note + 1:
              remnote = 0
              remnote_count += 1
              every_random_note = secrets.randbelow(every_random_note+2)
            else:
              remnote += 1
              not_matrix.append(event[4])
              ev_matrix.append(event)
              slices_events.append(event)
              slices_pitches.append(event[4])
          else:
            not_matrix.append(event[4])
            ev_matrix.append(event)
            slices_events.append(event)
            slices_pitches.append(event[4])
            notes_counter += 1


      itrack += 1

  
    # Calculate stats about the resulting dataset
    average_note_pitch = 0
    min_note = 0
    max_note = 0
    itrack = 1

    while itrack < len(score):
        for event in score[itrack]:
          if event[0] == 'note':
            min_note = int(min(min_note, event[4]))
            max_note = int(max(min_note, event[4]))
        itrack += 1

    files_count += 1
    if debug:
      print('File:', midi_file)

if melody_reduction_to_slices_max_pitches:
  not_matrix = slices_melody_pitches
  ev_matrix = slices_melody_events

if reverse_output_dataset:
  print('Augmenting the dataset now to reduce plagiarizm and repetitions.')
  rnot_matrix = not_matrix
  rev_matrix = ev_matrix
  rnot_matrix.reverse()
  rev_matrix.reverse()
  not_matrix = rnot_matrix
  ev_matrix = rev_matrix
if combine_reversed_and_original_datasets_together:
  not_matrix += rnot_matrix
  ev_matrix += rev_matrix
  
average_note_pitch = int(list_average(not_matrix))

print('Task complete :)')
print('==================================================')
print('Number of processed dataset MIDI files:', files_count)
if reverse_output_dataset: print('The dataset was augmented to prevent plagiarism as requested.')
print('Number of notes in the dataset MIDI files:', notes_counter)
if remnote_count > 0: print('Number of notes removed:', remnote_count)
print('Number of notes in the resulting dataset:', len(not_matrix))
if slices_count > 0: print('There are', slices_count, 'slices, each', dataset_slices_length_in_notes, 'notes long.')
#print('Minimum note pitch:', min_note)
#print('Maximum note pitch:', max_note)
print('Number of total MIDI events recorded:', len(ev_matrix))
print('Average note pitch:', average_note_pitch)
print('First 5 notes of the resulting dataset:', ev_matrix[0:6])
if remove_drums: print('Drums MIDI events have been removed as requested.')
# define a list of places
MusicDataset = [not_matrix, ev_matrix]

with open(full_path_to_output_dataset_to, 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(MusicDataset, filehandle)
print('Dataset was saved at:', full_path_to_output_dataset_to)
print('Task complete. Enjoy! :)')