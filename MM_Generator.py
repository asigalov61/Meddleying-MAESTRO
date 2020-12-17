# -*- coding: utf-8 -*-
"""MM_Generator.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GrdWC0M9hvezXydE0gpp0C2ycUMIiD16

Original GitHub repo is located at:
    https://github.com/asigalov61/Meddleying-MAESTRO

# Meddleying MAESTRO (ver 3.1)

***

## Full-featured Algorithmic Intelligence Music Augmentator (AIMA) with full multi-instrument MIDI output and Karaoke support.

***

### Project Los Angeles

### Tegridy Code 2020

***

# Setup Environment, clone needed code, and install all required dependencies
"""

print('Meddleying MAESTRO Algorithmic Intelligence Music Augmentator. Version 3.1')
print('Starting up...')

"""# Load/Re-load the processed dataset"""

import pickle

#@title Load pre-processed dataset from a file to memory
full_path_to_dataset_file = "Meddleying-MAESTRO-Music-Dataset.data" #@param {type:"string"}

not_matrix = []
ev_matrix = []
try_karaoke = False
with open(full_path_to_dataset_file, 'rb') as filehandle:
    # read the data as binary data stream
    MusicDataset = pickle.load(filehandle)
    not_matrix = MusicDataset[0]
    ev_matrix = MusicDataset[1]
    events_matrix = ev_matrix
    notes_matrix = not_matrix
    if ev_matrix[-1][0] == 'karaoke' and not_matrix[-1] == -1:
      try_karaoke = True
      print('Detected MM Version 2.7+ Karaoke Dataset')
    else:
      print('Detected MM Legacy/non-Karaoke Dataset')
print('Task complete. Enjoy! :)')
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
import toolz
import music21
from music21 import *
import pickle
import time
from datetime import datetime
import math
import sys
import tqdm.auto
import secrets
import pretty_midi
import statistics
#import librosa
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mido import MidiFile
from IPython.display import display, Image
import MIDI
from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI
from midi2audio import FluidSynth

#===some defaults===


ticks_per_note = 50
ctime = 0
cev_matrix = []
cnotes_matrix = []
debug = False


#@title Play with the settings until you get what you like 
relative_note_timings = True #@param {type:"boolean"}
start_note = 60 #@param {type:"slider", min:1, max:127, step:1}
start_with_random_introduction = True #@param {type:"boolean"}
notes_per_slice = 100 #@param {type:"slider", min:1, max:200, step:1}
number_of_notes_to_match_slices = 80 #@param {type:"slider", min:0, max:100, step:1}
number_of_slices = 5 #@param {type:"slider", min:1, max:100, step:1}
extra_match_slices = "Durations" #@param ["Notes Only", "Durations", "Velocities", "Channels", "Full Match"]
try_to_find_intro_for_composition = False
output_ticks = 400 #@param {type:"slider", min:0, max:2000, step:100}
ticks_per_note = 180 #@param {type:"slider", min:0, max:2000, step:10}
ticks_durations_multiplier = 1
notes_timings_multiplier = 1 #@param {type:"slider", min:0, max:2, step:0.01}
notes_durations_multiplier = 1 #@param {type:"slider", min:0.5, max:1.5, step:0.01}
notes_velocities_multiplier = 1.5 #@param {type:"slider", min:0.1, max:2, step:0.1}
transpose_velocity = -30 #@param {type:"slider", min:-60, max:60, step:1}
transpose_composition = 0 #@param {type:"slider", min:-30, max:30, step:1}
set_all_MIDI_patches_to_piano = False #@param {type:"boolean"}
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
nts = 0
nts1 = 0
dts = 0
kar = 0
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
block_events = []
block_notes = []
end_index = 0


ch0_ev_matrix = []
ch1_ev_matrix = []
ch2_ev_matrix = []
ch3_ev_matrix = []
ch4_ev_matrix = []
ch5_ev_matrix = []
ch6_ev_matrix = []
ch7_ev_matrix = []
ch8_ev_matrix = []
ch9_ev_matrix = []
ch10_ev_matrix = []
ch11_ev_matrix = []
ch12_ev_matrix = []
ch13_ev_matrix = []
ch14_ev_matrix = []
ch15_ev_matrix = []

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

print('Prepping the dataset...')
print('Splitting the dataset into channels...')
for i in range(len(ev_matrix)):
  if ev_matrix[i][3] == 0:
    ch0_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 1:
    ch1_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 2:
    ch2_ev_matrix.append(ev_matrix[i])
  
  if ev_matrix[i][3] == 3:
    ch3_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 4:
    ch4_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 5:
    ch5_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 6:
    ch6_ev_matrix.append(ev_matrix[i])
  
  if ev_matrix[i][3] == 7:
    ch7_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 8:
    ch8_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 9:
    ch9_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 10:
    ch10_ev_matrix.append(ev_matrix[i])
  
  if ev_matrix[i][3] == 11:
    ch11_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 12:
    ch12_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 13:
    ch13_ev_matrix.append(ev_matrix[i])

  if ev_matrix[i][3] == 14:
    ch14_ev_matrix.append(ev_matrix[i])
  
  if ev_matrix[i][3] == 15:
    ch15_ev_matrix.append(ev_matrix[i])    


print('Sorting channel events...')

ch0_ev_matrix.sort(key=lambda x: x[6])
ch1_ev_matrix.sort(key=lambda x: x[6])
ch2_ev_matrix.sort(key=lambda x: x[6])
ch3_ev_matrix.sort(key=lambda x: x[6])
ch4_ev_matrix.sort(key=lambda x: x[6])
ch5_ev_matrix.sort(key=lambda x: x[6])
ch6_ev_matrix.sort(key=lambda x: x[6])
ch7_ev_matrix.sort(key=lambda x: x[6])
ch8_ev_matrix.sort(key=lambda x: x[6])
ch9_ev_matrix.sort(key=lambda x: x[6])
ch10_ev_matrix.sort(key=lambda x: x[6])
ch11_ev_matrix.sort(key=lambda x: x[6])
ch12_ev_matrix.sort(key=lambda x: x[6])
ch13_ev_matrix.sort(key=lambda x: x[6])
ch14_ev_matrix.sort(key=lambda x: x[6])
ch15_ev_matrix.sort(key=lambda x: x[6])

print('Chordifying MIDI channels events...')

#ev_matrix = [j for i in zip(ch0_ev_matrix, ch1_ev_matrix) for j in i]
ev_matrix1 = [ch0_ev_matrix, 
             ch1_ev_matrix, 
             ch2_ev_matrix,
             ch3_ev_matrix, 
             ch4_ev_matrix,
             ch5_ev_matrix, 
             ch6_ev_matrix,
             ch7_ev_matrix, 
             ch8_ev_matrix,
             ch9_ev_matrix, 
             ch10_ev_matrix,
             ch11_ev_matrix, 
             ch12_ev_matrix,             
             ch13_ev_matrix, 
             ch14_ev_matrix,                                                                  
             ch15_ev_matrix]

ev_matrix2 = [ele for ele in ev_matrix1 if ele != []] 
ev_matrix = list(toolz.itertoolz.interleave(ev_matrix2))

print('Final sorting and notes list creation...')
ev_matrix.sort(key=lambda x: x[6])
not_matrix = [row[4] for row in ev_matrix]


if ctime > 0:
  time = ctime
else:
  time = 0

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

    if start_with_random_introduction:
      print('Trying to find a random intro for the composition...')
      start = False
      while start == False:
       index = secrets.choice(range(len(ev_matrix)))
       for i in range(index, (len(ev_matrix))):
        event = ev_matrix[i]
        if event[7] == 1:
          start = True
          index = event[6]
          print('Success! Found a sutable composition introduction!')
          break
except: 
  print('The Generator could not find the starting note in a dataset note sequence. Please adjust the parameters.')
  print('Meanwhile, trying to generate a sequence with the MIDI note # [60]')

  try:
    index = not_matrix.index(60, secrets.choice(range(len(not_matrix))))
    print('Trying a random starting note...')
    index = not_matrix.index(secrets.randbelow(128), secrets.choice(range(len(not_matrix))))
  except:
    print('Unfortunatelly, that did not work either. Please try again/restart run-time.')
    sys.exit()



  
print('Final starting index:', index)
print('Beginning the pattern search and generation...')

if extra_match_slices != 'Notes Only':
  print('Extra slices matching type requested:', extra_match_slices)

for i in tqdm.auto.tqdm(range(number_of_slices)):

  block_events = []
  block_notes = []

  for i in range(notes_per_slice):
    previous_event = ev_matrix[index-1+i]
    event = ev_matrix[index+i]
    next_event = ev_matrix[index+1+i]



    if ev_matrix[index+i][4] > 0 and event[0] == 'note':

      if relative_note_timings:
        if previous_event[1] != event[1]: 
          time += abs(output_ticks - int((event[5] + ticks_per_note) * ticks_durations_multiplier))
        else:
          time += 0

      else:
        if previous_event[1] != event[1]:
          time += abs(int(ticks_per_note * ticks_durations_multiplier))
        else:
          time += 0

      ovent_a = ['note', int(time * notes_timings_multiplier), int(event[2] * notes_durations_multiplier), event[3], event[4] + transpose_composition, (int(event[5] * notes_velocities_multiplier) + transpose_velocity)]                  
      output_events_matrix.append(ovent_a)

      nts1 += 1
      if i >= notes_per_slice - number_of_notes_to_match_slices:
        block_events.append(ovent_a)
        block_notes.append(ovent_a[4])
        if debug: print(block_notes)

      
    #how to add stuff...
    if ev_matrix[index+i][4] == -1 and event[0] == 'text_event' or event[0] == 'lyric': 
      ovent_a = ['text_event', int(time), event[2]]                          
      output_events_matrix.append(ovent_a)
      block_events.append(ovent_a)
          
      kar += 1
    #this is it :)     
      


    
  found_pattern = False

  for x in range(len(ev_matrix) - number_of_notes_to_match_slices - notes_per_slice):
    z = 0  
    if ev_matrix[x][0] == 'note':

      for y in range(len(block_events)):       
        if ev_matrix[x+y][0] == 'note' and block_events[y][0] == 'note':
          if extra_match_slices == 'Full Match':
            if block_events[y][3] == ev_matrix[x+y][3] and block_events[y][4] == ev_matrix[x+y][4] and block_events[y][2] == ev_matrix[x+y][2] and block_events[y][5] == ev_matrix[x+y][5]:
                z += 1
                nts += 1
                continue 
          
          if extra_match_slices == 'Notes Only':
            if block_events[y][4] == ev_matrix[x+y][4]:            
                z += 1
                nts += 1
                continue        

          if extra_match_slices == 'Durations':
            if block_events[y][2] == ev_matrix[x+y][2]:
              z += 1
              nts += 1
              continue

          if extra_match_slices == 'Velocities':
            if block_events[y][5] == ev_matrix[x+y][5]:
              z += 1
              nts += 1
              continue

          if extra_match_slices == 'Channels':
            if block_events[y][3] == ev_matrix[x+y][3]:       
              z += 1
              nts += 1 
            
      if z == len(block_events):
        end_index = x + y
        found_pattern = True
        break

  if debug: print('End Index', end_index)
  if end_index != 0:
    index = end_index
    dts += 1

output += [output_events_matrix]

midi_data = MIDI.opus2midi(MIDI.score2opus(output))

if not relative_note_timings:
  with open('output.mid', 'wb') as midi_file1:
      midi_file1.write(midi_data)
      midi_file1.close()
else:
  with open('output.mid', 'wb') as midi_file1:
    midi_file1.write(midi_data)
    midi_file1.close()

now = ''
now_n = str(datetime.now())
now_n = now_n.replace(' ', '_')
now_n = now_n.replace(':', '_')
now = now_n.replace('.', '_')
    
if not relative_note_timings:
  fname_abs = './Saved_Output/output-absolute_' + str(now) + '.mid'  
  with open(fname_abs , 'wb') as midi_file1:
      midi_file1.write(midi_data)
      midi_file1.close()
else:
  fname_rel = './Saved_Output/output-relative_' + str(now) + '.mid'    
  with open(fname_rel, 'wb') as midi_file1:
    midi_file1.write(midi_data)
    midi_file1.close()

print('Done! Crunching quick stats...')
print('First Note:', output[2][1], '=== Last Note:', output[2][-1])
print('MIDI Stats:', MIDI.score2stats(output))
print('The dataset was scanned', dts, 'times.')
print('Examined', nts, 'notes from the dataset.')
print('Generated notes total:', nts1, 'out of expected', len(output[2]) - len(cnotes_matrix) - 1, 'MIDI events...')
if try_karaoke: print('Generated', kar, 'Karaoke events.')
print('Task complete!')
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
seconds_to_show = 180 #@param {type:"slider", min:1, max:180, step:1}
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

#@title Plot, Graph, and Listen to the Output :)
#graphs_length_inches = 18 #@param {type:"slider", min:0, max:20, step:1}
#notes_graph_height = 6 #@param {type:"slider", min:0, max:20, step:1}
#highest_displayed_pitch = 92 #@param {type:"slider", min:1, max:128, step:1}
#lowest_displayed_pitch = 24 #@param {type:"slider", min:1, max:128, step:1}



#midi_data = pretty_midi.PrettyMIDI('./output.mid')

#def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
    # Use librosa's specshow function for displaying the piano roll
#    librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
#                             hop_length=1, sr=fs, x_axis='time', #y_axis='cqt_note',
#                             fmin=pretty_midi.note_number_to_hz(start_pitch))



#roll = np.zeros([int(graphs_length_inches), 128])
# Plot the output

#track = Multitrack('./output.mid', name='track')
#plt.figure(figsize=[graphs_length_inches, notes_graph_height])
#fig, ax = track.plot()
#fig.set_size_inches(graphs_length_inches, notes_graph_height)
#plt.figure(figsize=[graphs_length_inches, notes_graph_height])
#ax2 = plot_piano_roll(midi_data, int(lowest_displayed_pitch), int#(highest_displayed_pitch))
#plt.show(block=False)

#https://sites.google.com/site/soundfonts4u/
FluidSynth("./SGM-v2.01-YamahaGrand-Guit-Bass-v2.7.sf2", 44000).midi_to_audio('./output.mid', './output.wav')