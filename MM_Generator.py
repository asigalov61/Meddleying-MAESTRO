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

print('Meddleying MAESTRO Algorithmic Intelligence Music Generator. Version 2.6')
print('Starting up...')

"""# Load/Re-load the processed dataset"""
import pickle
#@title Load pre-processed dataset from a file to memory
full_path_to_dataset_file = "./Meddleying-MAESTRO-Music-Dataset.data" #@param {type:"string"}
print('Loading the dataset...')
not_matrix = []
ev_matrix = []

with open(full_path_to_dataset_file, 'rb') as filehandle:
    # read the data as binary data stream
    MusicDataset = pickle.load(filehandle)
    not_matrix = MusicDataset[0]
    ev_matrix = MusicDataset[1]
    events_matrix = ev_matrix
    notes_matrix = not_matrix

print('Task complete.')
print('==================================================')
print('Number of notes in the dataset:', len(not_matrix))
print('Number of total MIDI events recorded:', len(ev_matrix))
print('Done! Enjoy! :)')


"""# Generate Music

Standard MIDI timings are 400/120(80).
Recommended settings are: notes per slice = 30 and notes timings multiplier range is 0.95 <> 1 
"""


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
from IPython.display import display, Image
import MIDI
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI
ticks_per_note = 50
ctime = 0
cev_matrix = []
cnotes_matrix = []
debug = False


#@title Play with the settings until you get what you like 
attention_span = "augmentation1" #@param ["augmentation1", "augmentation2"]
start_note = 80 #@param {type:"slider", min:1, max:127, step:1}
notes_per_slice = 60 #@param {type:"slider", min:5, max:60, step:1}
number_of_slices = 15 #@param {type:"slider", min:5, max:400, step:5}
relative_note_timings = True #@param {type:"boolean"}
try_to_find_intro_for_composition = False #@param {type:"boolean"}
output_ticks = 400 #@param {type:"slider", min:0, max:2000, step:100}
ticks_per_note = 180 #@param {type:"slider", min:0, max:2000, step:10}
ticks_durations_multiplier = 1
notes_timings_multiplier = 0.97 #@param {type:"slider", min:0, max:2, step:0.01}
notes_durations_multiplier = 1.25 #@param {type:"slider", min:0.5, max:1.5, step:0.01}
notes_velocities_multiplier = 1.5 #@param {type:"slider", min:0.1, max:2, step:0.1}
transpose_velocity = -30 #@param {type:"slider", min:-60, max:60, step:1}
transpose_composition = 0 #@param {type:"slider", min:-30, max:30, step:1}
set_all_MIDI_patches_to_piano = True #@param {type:"boolean"}
MIDI_channel_patch_00 = 0 #@param {type:"number"}
MIDI_channel_patch_01 = 24 #@param {type:"number"}
MIDI_channel_patch_02 = 32 #@param {type:"number"}
MIDI_channel_patch_03 = 40 #@param {type:"number"}
MIDI_channel_patch_04 = 42 #@param {type:"number"}
MIDI_channel_patch_05 = 46 #@param {type:"number"}
MIDI_channel_patch_06 = 56 #@param {type:"number"}
MIDI_channel_patch_07 = 71 #@param {type:"number"}
MIDI_channel_patch_08 = 73 #@param {type:"number"}
MIDI_channel_patch_09 = 0 #@param {type:"number"}
MIDI_channel_patch_10 = 0 #@param {type:"number"}
MIDI_channel_patch_11 = 0 #@param {type:"number"}
MIDI_channel_patch_12 = 0 #@param {type:"number"}
MIDI_channel_patch_13 = 0 #@param {type:"number"}
MIDI_channel_patch_14 = 0 #@param {type:"number"}
MIDI_channel_patch_15 = 0 #@param {type:"number"}


#===TODO===
melody_only_output_for_melody_datasets = False
#===
output_events_matrix = []
output_events_matrix1 = []
midi_data = []
midi_dats1 = []
events_matrix = []
notes_matrix = []
index = 0
index1 = 0
time = 0
x = 0
output = []
output1 = []
average_note_pitch = 100
time_r = 0
ovent = []
ovent_r = []
ovent_a = []
start_event = []
event4 = []
event3 = []
event2 = []
event1 = [] 
event = []
event01 = [] 
event02 = []
event03 = [] 
event04 = []
global_time = []

if set_all_MIDI_patches_to_piano:
  output = [output_ticks, [['track_name', 0, b'Meddleying MAESTRO']]]
else:
  output = [output_ticks,
            [['track_name', 0, b'Meddleying MAESTRO'], 
              ['patch_change', 0, 0, MIDI_channel_patch_00], 
              ['patch_change', 0, 1, MIDI_channel_patch_01],
              ['patch_change', 0, 2, MIDI_channel_patch_02],
              ['patch_change', 0, 3, MIDI_channel_patch_03],
              ['patch_change', 0, 4, MIDI_channel_patch_04],
              ['patch_change', 0, 5, MIDI_channel_patch_05],
              ['patch_change', 0, 6, MIDI_channel_patch_06],
              ['patch_change', 0, 7, MIDI_channel_patch_07],
              ['patch_change', 0, 8, MIDI_channel_patch_08],
              ['patch_change', 0, 9, MIDI_channel_patch_09],
              ['patch_change', 0, 10, MIDI_channel_patch_10],
              ['patch_change', 0, 11, MIDI_channel_patch_11],
              ['patch_change', 0, 12, MIDI_channel_patch_12],
              ['patch_change', 0, 13, MIDI_channel_patch_13],
              ['patch_change', 0, 14, MIDI_channel_patch_14],
              ['patch_change', 0, 15, MIDI_channel_patch_15],]]
output1 = output
output_events_matrix = [['track_name', 0, b'Composition Track']]
output_events_matrix1 = [['track_name', 0, b'Composition Track']]        

#output.append(output_events_matrix)    
#output1.append(output_events_matrix1)
ctime = 0
if ctime > 0:
  time = ctime
else:
  time = 0

if melody_only_output_for_melody_datasets:
  try:
    index1 = slices_melody_pitches.index(start_note)
    index = index1+augmentation_strength*2
  except:
    index1 = slices_melody_pitches.index(average_note_pitch)
    index = index1+augmentation_strength*2

try:
  if len(cev_matrix) != 0:
    events_matrix = ev_matrix
    notes_matrix = not_matrix
    output_events_matrix = cev_matrix
    start_note = cnotes_matrix[-1]
    index = cindex
    print('Priming_sequence: MIDI event:', cev_matrix[-1])
    cev_matrix = 0
    ctime = 0
  else:
    index = 0
    flag = True
    events_matrix = ev_matrix
    notes_matrix = not_matrix
    print('Priming_sequence: MIDI note #', [start_note])
    index = not_matrix.index(start_note, secrets.choice(range(len(not_matrix))))
    if try_to_find_intro_for_composition:
      print('Trying to find intro starting point...')
      for i in range(len(notes_matrix)):
        if events_matrix[i][1] == 0:
          if secrets.randbelow(2) == 0:
            if flag == True:
              start_note = notes_matrix[i]
              index = i
              flag = False
              print('Success! :)') 
      if flag is True: print ('Could not find sutable intro point. :(')  
except: 
  print('The Generator could not find the starting note in a dataset note sequence. Please adjust the parameters.')
  print('Meanwhile, trying to generate a sequence with the MIDI note # [60]')

  try:
    index = not_matrix.index(60, secrets.choice(range(len(not_matrix))))

  except:
    print('Unfortunatelly, that did not work either. Please try again/restart run-time.')
    sys.exit()
  
print('Final starting index:', index)

for i in tqdm.auto.tqdm(range(number_of_slices)):
  for k in range(notes_per_slice):
    if attention_span == 'augmentation1' or 'augmentation2':
      if k > 3:
        #try:
          event03 = ev_matrix[index+k-4]
          event02 = ev_matrix[index+k-3]
          event01 = ev_matrix[index+k-2]
          event0 = ev_matrix[index+k-1]
        
          event = ev_matrix[index+k]

          event1 = ev_matrix[index+k+1]
          event2 = ev_matrix[index+k+2]
          event3 = ev_matrix[index+k+3]
          event4 = ev_matrix[index+k+4]
          
          if relative_note_timings:
            #if abs(event1[1]-event[1]) > 0:
              #time += int(min(event02[2], event01[2], event0[2], event[2], event1[2], event2[2], event3[2]) * notes_timings_multiplier)
              #time += int(min(event[2], event0[2], event1[2]))
            if event1[1] != event[1]: 
              time += abs(output_ticks - int((event[5] + ticks_per_note) * ticks_durations_multiplier))
            else:
              time += 0
          else:
            if event1[1] != event[1]:
             time += abs(int(ticks_per_note * ticks_durations_multiplier))
            else:
              time += 0
          #ovent_a = ['note', int(time * notes_timings_multiplier), int(event[2] * notes_durations_multiplier), event[3], event[4] + transpose_composition, (int(event4[5] * notes_velocities_multiplier) + transpose_velocity)]
          #ovent_a = ['note', int(time * notes_timings_multiplier), int(event4[2] * notes_durations_multiplier), event4[3], event4[4] + transpose_composition, (int(event4[5] * notes_velocities_multiplier) + transpose_velocity)]        
          ovent_a = ['note', int(time * notes_timings_multiplier), int(event4[2] * notes_durations_multiplier), event4[3], event4[4] + transpose_composition, (int(event[5] * notes_velocities_multiplier) + transpose_velocity)]                  
          output_events_matrix.append(ovent_a)        
          x += 1
        #except:
        #  print('The generator could not generate full pattern. Please try again.')
        #  print('Please try again, maybe even with different parameters or a larger dataset.')
        #  print('If error persists, please restart/factory reset the run-time.')
        #  sys.exit()      
      


  if attention_span == 'augmentation1':
    try:
      for i in range(len(notes_matrix)-8):
        if notes_matrix[i] == event03[4]:
          if events_matrix[i][2] == event03[2]:
            if events_matrix[i][5] == event03[5]:
              if events_matrix[i][3] == event03[3]:                   
                if notes_matrix[i+1] == event02[4]:
                  #if events_matrix[i+1][2] == event02[2]:
                  # if events_matrix[i+1][5] == event02[5]:
                  #   if events_matrix[i+1][3] == event02[3]:                     
                  if notes_matrix[i+2] == event01[4]:
                    if notes_matrix[i+3] == event0[4]:                     
                      if notes_matrix[i+4] == event[4]:
                        if notes_matrix[i+5] == event1[4]:
                          if notes_matrix[i+6] == event2[4]:
                            if notes_matrix[i+7] == event3[4]:
                              if notes_matrix[i+8] == event4[4]:
                                index = i + 8


    except:
      print('Cound not find enough tokens to generate. Please try again!')
      sys.exit()
      
  if attention_span == 'augmentation2':
    try:
      for i in range(len(notes_matrix)-8):
        if notes_matrix[i] == event03[4]:
          if events_matrix[i][2] == event03[2]:
            if events_matrix[i][5] == event03[5]:
              if events_matrix[i][3] == event03[3]:                   
                if notes_matrix[i+1] == event02[4]:
                  if events_matrix[i+1][2] == event02[2]:
                    if events_matrix[i+1][5] == event02[5]:
                      if events_matrix[i+1][3] == event02[3]:                     
                        if notes_matrix[i+2] == event01[4]:
                          if notes_matrix[i+3] == event0[4]:                     
                            if notes_matrix[i+4] == event[4]:
                              if notes_matrix[i+5] == event1[4]:
                                if notes_matrix[i+6] == event2[4]:
                                  if notes_matrix[i+7] == event3[4]:
                                    if notes_matrix[i+8] == event4[4]:
                                      index = i + 8


    except:
      print('Cound not find enough tokens to generate. Please try again!')
      sys.exit()

if melody_only_output_for_melody_datasets:   
  events_matrix = [output_ticks, slices_melody_events]
  itrack = 1
  i=0
  while itrack < len(events_matrix):
    for event in events_matrix[itrack]:
      if i >= index1 and i < index1 + number_of_slices * notes_per_slice:
        if event[0] == 'note':

          output_r.append(event)
          event[2] = ticks_per_note
          output1.append(event)
          x+=1
      i+=1
    itrack += 1
  output.append(output1)

output += [output_events_matrix]

midi_data = MIDI.opus2midi(MIDI.score2opus(output))

if not relative_note_timings:
  with open('output-absolute.mid', 'wb') as midi_file1:
      midi_file1.write(midi_data)
      midi_file1.close()
else:
  with open('output-relative.mid', 'wb') as midi_file1:
    midi_file1.write(midi_data)
    midi_file1.close()

print('First Note:', output[2][1], '=== Last Note:', output[2][-1])
print('MIDI Stats:', MIDI.score2stats(output))
print('Total notes:', x, 'out of expected:', len(output[2]) - len(cnotes_matrix) - 1)
print('Done!')
print('Downloading your MIDI now :)')
print('Enjoy! :)')

"""# Fun MIR stats"""

#@title Basic statistical analysis of the output MIDI file

MIDI_DIR = "./*.mid"
### https://github.com/brennan2602/FYP


def get_piano_roll(midifile):
	midi_pretty_format = pretty_midi.PrettyMIDI(midifile)
	piano_midi = midi_pretty_format.instruments[0] # Get the piano channels
	piano_roll = piano_midi.get_piano_roll(fs=20)
	return piano_roll

#uses split encoding scheme (here only encoding the note values)
#works by looping through time increments of the piano roll array and writing the notes being played
#at a given time sample as a number on the corresponding line of a string # is written when no notes played for that
#sample
def encode(arr):
    timeinc=0
    outString=""
    for time in arr:
        notesinc = -1
        #print(time)
        if np.all(time==0):
            outString=outString+"#"
        for vel in arr[timeinc]:
            notesinc=notesinc+1
            if vel != 0:
                noteRep=str(notesinc) + " "
                #print(noteRep)
                outString=outString+noteRep
        outString=outString+"\n"
        timeinc = timeinc+1
    return outString


def getSilences(test):
    test=test[:-1] #removing last line in string (always blank)
    output=test.split("\n") #splitting into array
    res = len(output)
    #initialising counters
    maxcounter=0
    counter=0
    silenceCount=0

    for x in output:
        if x == "#": #when a "#" is seen nothing is being played that sample
            counter=counter+1 #this tracks a streak of silences
            silenceCount+=1 #this tracks total silences
        if x != "#":
            counter=0 #reseting streak
        if counter>maxcounter:
            maxcounter=counter #updating longest silence streak when appropriate
    return maxcounter,silenceCount


#by looking at the length of song and the amount of silences this returns % silence
def getPercentSilence(gen,silences):
    test = gen
    test = test[:-1]
    output = test.split("\n")
    res = len(output)
    percent=silences/res
    return percent


def getStatsNotes(test):
    test=test[:-1] #get rid of blank line at the end
    notes=[]
    output = test.split("\n") #split string on new lines

    #initial values updated while looping through
    maxPerSamp=0
    silenceSamp=0
    notesPlayed=0
    maxNotes=0
    maxVal=0
    minVal=127

    for x in output:
        samp=x.split(" ")
        samp=samp[:-1] #theres a blank result at the end of array from split this indexing removes it
        while "0" in samp:
            samp.remove("0") #sometimes 0 samples exist this removes them as they aren't notes played
        if len(samp)==0:
            silenceSamp+=1 #counting silences
        notesPlayed=notesPlayed+len(samp) #counting notes played
        if len(samp)>0:
            #getting max and min note values at this time step
            minimum=min(samp)
            maximum=max(samp)
            #updating max and min values note values for song if appropriate
            if int(minimum)<minVal:
                minVal=int(minimum)
            if int(maximum)>maxVal:
                maxVal=int(maximum)
        #updating maximum number of notes per sample if appropriate
        if len(samp)>maxNotes:
            maxNotes=len(samp)
    rangeNotes=maxVal-minVal #spread of notes
    avgNotes = notesPlayed / len(output) #average notes per sample
    adjNotes=notesPlayed /(len(output)-silenceSamp) #average notes per sample adjusted to remove silent samples
    return rangeNotes, maxVal, minVal,maxNotes,avgNotes,adjNotes


files=glob.glob(MIDI_DIR)#point towards directory with midi files (here same folder)
#print(files)

for f in files:
    print(f)
    pr = get_piano_roll(f) #gets piano roll representation of the midi file
    arr = pr.T
    outString= encode(arr) #gets a string representation of the midi file
    maxsilences, silences = getSilences(outString) #by passing in the encoded string get longest silence and the total
                                                   #number of samples which are silent
    noteRange, maxVal, minVal, maxNotes, avgNotes, adjAvg =getStatsNotes(outString) # getting some stats by looping
                                                                                    # through encoded data
    percentSilence= getPercentSilence(outString,silences) # get % silence from silence / outString length

    #printing out to the user
    print("longest silence is ",maxsilences,"samples long")
    print("silence covers:",round(percentSilence,4),"%")
    print("notes span range:",noteRange)
    print("max note value:",maxVal)
    print("min note value:",minVal)
    print("average number of notes per sample:",round(avgNotes,4))
    print("average number of notes per sample (adjusted to remove silence samples):",round(adjAvg,4))
    print("max number of notes played in a sample:",maxNotes)
    print("\n")

#NOTE some minor discrepencies vs reading in from generated file directly
#However this does provide a uniform check to use for songs generated by both encoding schemes
#Can also be used to evaluate training file
#uses split encoding to get the text representation for ease of development

#@title Basic graph of the last output
seconds_to_show = 30 #@param {type:"slider", min:1, max:180, step:1}
show_whole_track = False #@param {type:"boolean"}
graph_color = "red" #@param ["blue", "red", "green"]

x = []
y = []
z = []

t = 0
itrack = 1
fig = plt.figure(figsize=(12,5))
while itrack < len(output1):
  for event in output1[itrack]:
      if event[0] == 'note':
        y.append(event[4])
        x.append(t)
        plt.plot(x, y, color=graph_color)
        t += 0.25       
        if not show_whole_track:
          if t == seconds_to_show: break
  itrack +=1
plt.show()

#@title Output MIDI bokeh plot

preset = Preset(plot_width=850)
plotter = Plotter(preset, plot_max_length_bar=4)

if not relative_note_timings:
  pm = PrettyMIDI("./output-absolute.mid")
else:
  pm = PrettyMIDI("./output-relative.mid")
plotter.show_notebook(pm)