import os

files = ['token.txt', 'admin.txt', 'chancmd.txt']

for file in files:
    open(file, mode='a').close()