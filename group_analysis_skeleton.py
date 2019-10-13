#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil

#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename

path = os.getcwd() #please start from ps2-yourname
destpath = path + '/rawdata'
testingrooms = ['A','B','C']

for room in testingrooms:
    #enter each testing room
    pathroom = path + '/testingroom' + room
    os.chdir(pathroom)
    print('entered testingroom',room)
    #get filename
    filename = 'experiment_data.csv'
    print('old filename =',filename) #old filename
    #rename file
    os.rename(filename,'experiment_data'+room+'.csv')
    filename = ('experiment_data'+room+'.csv')
    print('new filename =',filename) #new filename
    #move file
    source = pathroom + '/' + filename
    destination = path + '/rawdata' + '/' + filename
    shutil.copyfile(source,destination)
    print(filename + ' ~~~ has been copied')

    print('files in /rawdata:')
    print(os.listdir(path + '/rawdata'))

#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT

os.chdir(path + '/rawdata')

for room in testingrooms:
    #import data
    filename = 'experiment_data'+room+'.csv'
    tmp = sp.loadtxt(filename,delimiter=',')
    if room == testingrooms[0]:
        data = tmp
    elif room > testingrooms[0]:
        data = np.vstack([data,tmp])

#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.mean(data[:,3])   # 91.48%
mrt_avg = np.mean(data[:,4])   # 477.3ms

#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
words_acc = 0
faces_acc = 0
words_rt = 0
faces_rt = 0
num_words = 0
num_faces = 0
loop = -1

for row in data[:,1]:
    loop += 1
    int(row)
    if row == 1:
        words_acc += data[loop,3]
        words_rt += data[loop,4]
        num_words += 1
    elif row == 2:
        faces_acc += data[loop,3]
        faces_rt += data[loop,4]
        num_faces += 1

words_acc_avg = words_acc/num_words
words_rt_avg = words_rt/num_words
faces_acc_avg = faces_acc/num_faces
faces_rt_avg = words_rt/num_faces

# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms

#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp_avg = np.mean(data[data[:,2]==1,3])  # 94.0%
acc_bp_avg = np.mean(data[data[:,2]==2,3])  # 88.9%
mrt_wp_avg = np.mean(data[data[:,2]==1,4])  # 469.6ms
mrt_bp_avg = np.mean(data[data[:,2]==2,4])  # 485.1ms

#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#

words_rt_wp_avg = np.mean(data[(data[:,1]+data[:,2])==2,4])# words - white/pleasant: 478.4ms
words_rt_bp_avg = np.mean(data[(data[:,1]-data[:,2])==-1,4])# words - black/pleasant: 500.3ms
faces_rt_wp_avg = np.mean(data[(data[:,1]-data[:,2])==1,4])# faces - white/pleasant: 460.8ms
faces_rt_bp_avg = np.mean(data[(data[:,1]+data[:,2])==4,4])# faces - black/pleasant: 469.9ms

#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

words_rt_ttest_wpbp = scipy.stats.ttest_rel(data[(data[:,1]+data[:,2])==2,4],data[(data[:,1]-data[:,2])==-1,4])# words: t=-5.36, p=2.19e-5
faces_rt_ttest_wpbp = scipy.stats.ttest_rel(data[(data[:,1]-data[:,2])==1,4],data[(data[:,1]+data[:,2])==4,4])# faces: t=-2.84, p=0.0096

#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('ACC/RT OVERALL: {:.2f} %, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('ACC/RT WORDS: {:.2f} %, {:.1f} ms'.format(100*words_acc_avg,words_rt_avg))
print('ACC/RT FACES: {:.2f} %, {:.1f} ms'.format(100*faces_acc_avg,faces_rt_avg))
print('ACC/RT WP: {:.2f} %, {:.1f} ms'.format(100*acc_wp_avg,mrt_wp_avg))
print('ACC/RT BP: {:.2f} %, {:.1f} ms'.format(100*acc_bp_avg,mrt_bp_avg))
print('RT WORDS x WP vs. BP: {:.1f} ms, {:.1f} ms, t = {:.2f}, p = {:.2f}'.format(100*words_rt_wp_avg,100*words_rt_bp_avg,words_rt_ttest_wpbp[0],words_rt_ttest_wpbp[1]))
print('RT FACES x WP vs. BP: {:.1f} ms, {:.1f} ms, t = {:.2f}, p = {:.2f}'.format(100*faces_rt_wp_avg,100*faces_rt_bp_avg,faces_rt_ttest_wpbp[0],faces_rt_ttest_wpbp[1]))


