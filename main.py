


import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image, ImageFilter, ImageFont, ImageOps
import os
from PIL import ImageDraw






class ApplyLUTtoImage():

  accepted_extensions=['jpg','jpeg']
  def __init__(self, Imagelink, FolderName):
    link = Imagelink.split('.')

    #check the accepted files to read
    if link[1] not in self.accepted_extensions:
      raise ValueError('Invalid file extension') 
    print(os.getcwd())
    listLUTs = os.listdir(os.getcwd())
    if len(listLUTs)==0:
      raise ValueError('No LUT file found')


    try:
        self.image = Image.open(Imagelink)
    except Exception as e:
        print(type(e).__name__)

    self.listLUTs = listLUTs
    self.folderName = FolderName


  def applyFilter(self,lutName):
    data = []
    lut_size = None
    # check the file type
    luts_ = lutName.split('.')
    if luts_[1]=='cube'or 'CUBE' :
      with open(self.folderName+'/'+lutName,'r') as file:
        for line in file:
          line = line.strip()
          if not line or line.startswith('#'):
            continue

          if line.startswith('LUT_3D_SIZE'):
            parts = line.split()
            if len(parts)==2:
              lut_size = int(parts[1])
            else:
              raise ValueError('Invalid Lut size')
          elif lut_size is not None:
            data.append((line))

        
      row2val = lambda row: tuple([float(val) for val in row])
      lut_table =[row2val(row.split(" ")) for row in data]
      self.lut_table = lut_table
      filter = ImageFilter.Color3DLUT(lut_size,lut_table)
      filteredImage = self.image.filter(filter)
      filteredImage.save(f'{luts_[0]}.jpeg')
      # format the filtered  image with title
      return None
    else:
      # capture the other error codes
      raise ValueError('some random error')
    
    




singleImage = ApplyLUTtoImage('scenary.jpeg','LUTsFolder')

# save multiple image of the single image with the applied filters

# a varaiable name and then to the listdir
listLuts = os.listdir('LUTsFolder')

for luts in listLuts:
  singleImage.applyFilter(luts)