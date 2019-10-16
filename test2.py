#---------------Funtions-----------------
#rpm to rad/s converter 
def rpm2rad(rpm):
  rads = rpm*2*np.pi/60
  return np.round(rads,dec)

def findRow(rowName):
  for row in range(num_rows):
    if row_names[row] == rowName:
      return str(row+1)

print('GArry')