import os

folder = 'text_files/'
files = ['token.txt', 'admin.txt', 'chancmd.txt']

for file in files:
    open(folder+file, mode='a').close()