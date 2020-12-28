import numpy as np
import cv2
import os
from skimage.measure import label
from skimage.color import label2rgb
import time
from time import sleep
import tkinter as tk
from tkinter import filedialog
import imutils
from PIL import Image

root = tk.Tk()
root.withdraw()

print('Browse to Path to Original Test Image Directory')
opath = filedialog.askdirectory(title='Path to Test Image Directory')
print('Now Locate Path to Prediction Label Directory')
ppath = filedialog.askdirectory(title='Path to Prediction Image Directory')
print('Finally, Set Save Path Directory for Adjusted Labels')
saveP = filedialog.askdirectory(title='Save Path Directory for Adjusted Labels')

#opath = '/home/chris/Trunk/PythonProjects/Images/test/resize'
#ppath = '/home/chris/Trunk/PythonProjects/Images/test/GTV3'
#saveP = '/home/chris/Trunk/PythonProjects/Images'

rows = 1024
cols = 1024
N = rows
M = cols
ex = 100
clr = 255
container = np.zeros((M,N+ex,3))
container[0:100,N:N+ex] = (0.5,0.5,0)
container[100:200,N:N+ex] = (0,0.5,0.5)
container[200:300,N:N+ex] = (0.5,0,0.5)
container[300:400,N:N+ex] = (0.5,0.3,0.1)
container[400:500,N:N+ex] = (0.1,0.3,0.5)
container[500:600,N:N+ex] = (0.5,0.1,0.3)
container[600:700,N:N+ex] = (0.3,0.1,0.5)
container[700:800,N:N+ex] = (0.3,0.5,0.1)
container[800:900,N:N+ex] = (0.1,0.5,0.3)
container[900:1000,N:N+ex] = (0.3,0.3,0.3)
container[1000:1024,N:N+ex] = (1,1,1)

def bin_ndarray(ndarray, new_shape, operation='mean'):

	operation = operation.lower()
	if not operation in ['sum', 'mean']:
		raise ValueError("Operation not supported.")
	if ndarray.ndim != len(new_shape):
		raise ValueError("Shape mismatch: {} -> {}".format(ndarray.shape,
														   new_shape))
	compression_pairs = [(d, c//d) for d,c in zip(new_shape,
												  ndarray.shape)]
	flattened = [l for p in compression_pairs for l in p]
	ndarray = ndarray.reshape(flattened)
	for i in range(len(new_shape)):
		op = getattr(ndarray, operation)
		ndarray = op(-1*(i+1))
	return ndarray

name = [f for f in os.listdir(opath) if os.path.isfile(os.path.join(opath,f))]
nme = 0
NME = name[nme]
MX = len(name)
MN = 0

def load_image(imgname, opath, saveP, ppath, rows, cols):
	image_path = os.path.join(opath,imgname)
	save_path = os.path.join(saveP,imgname)
	label_path = os.path.join(ppath,imgname)

	orig = cv2.imread(image_path, 0)
	pred = cv2.imread(label_path, 0)

	orig = np.asarray(Image.fromarray(orig).resize((rows,cols), Image.NEAREST))
	sh = orig.shape
	pred = np.asarray(Image.fromarray(pred).resize((rows,cols), Image.NEAREST))
	#rt,pred = cv2.threshold(pred,20,250,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	orig3 = cv2.cvtColor(orig, cv2.COLOR_GRAY2RGB)
	#pred3 = np.zeros_like(orig3)
	#pred3[:,:,0] = pred
	#pred3[:,:,1] = pred
	pred3 = label(pred)
	pred3 = pred3.astype('uint8')

	#over = np.zeros_like(orig3)
	mask = np.zeros_like(pred)
	mask = cv2.resize(mask,(mask.shape[0]+2, mask.shape[1]+2))
	
	return pred3, orig3, mask

def save_image(pred3, saveP, imgname):
	#out = cv2.cvtColor(pred3, cv2.COLOR_RGB2GRAY)
	save_path = os.path.join(saveP,imgname)
	out = label(pred3)
	if rows > 512:
		out = cv2.resize(out.astype('uint8'), (512, 512), cv2.INTER_NEAREST)

	cv2.imwrite(save_path, out)

pred3, orig3, mask = load_image(NME, opath, saveP, ppath, rows, cols)
drawing=False # true if mouse is pressed
mode=0 # 0: pan image; 1: left click draw black; 2: left click draw white; 3: left click remove object; 4: left click fill object;
predc = pred3.copy()

def draw(event,former_x,former_y,flags,param):
	global current_former_x, current_former_y, drawing, mode, predc, pred3, orig3, clr

	if event==cv2.EVENT_LBUTTONDOWN:
		
		drawing=True
		current_former_x,current_former_y=former_x,former_y
		if former_y < 100 and former_y > 0:
			if former_x < N+ex and former_x > N:
				mode = 1
				container[0:100,N:N+ex] = (0.55,0.55,0)
				cv2.putText(container, 'Erase (1)', (N+12,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
				predc = pred3.copy()
		elif former_y < 200 and former_y > 100:
			if former_x < N+ex and former_x > N:
				mode = 2
				container[100:200,N:N+ex] = (0,0.55,0.55)
				cv2.putText(container, 'Draw (2)', (N+14,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
				predc = pred3.copy()
		elif former_y < 300 and former_y > 200:
			if former_x < N+ex and former_x > N:
				mode = 3
				container[200:300,N:N+ex] = (0.55,0,0.55)
				cv2.putText(container, 'Remove (3)', (N+3,250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 400 and former_y > 300:
			if former_x < N+ex and former_x > N:
				mode = 4
				container[300:400,N:N+ex] = (0.55,0.35,0.15)
				cv2.putText(container, 'Fill (4)', (N+24,350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 500 and former_y > 400:
			if former_x < N+ex and former_x > N:
				mode = 5
				container[400:500,N:N+ex] = (0.15,0.35,0.55)
				cv2.putText(container, 'Pick (5)', (N+18,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 600 and former_y > 500:
			if former_x < N+ex and former_x > N:
				mode = 6
				container[500:600,N:N+ex] = (0.55,0.15,0.35)
				cv2.putText(container, 'Next (f)', (N+16,550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 700 and former_y > 600:
			if former_x < N+ex and former_x > N:
				mode = 7
				container[600:700,N:N+ex] = (0.35,0.15,0.55)
				cv2.putText(container, 'Prev (b)', (N+16,650), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 800 and former_y > 700:
			if former_x < N+ex and former_x > N:
				mode = 8
				container[700:800,N:N+ex] = (0.35,0.55,0.15)
				cv2.putText(container, 'Save (s)', (N+15,750), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 900 and former_y > 800:
			if former_x < N+ex and former_x > N:
				mode = 9
				container[800:900,N:N+ex] = (0.15,0.55,0.35)
				cv2.putText(container, 'Quit (q,esc)', (N+2,850), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
		elif former_y < 1000 and former_y > 900:
			if former_x < N+ex and former_x > N:
				pred3 = predc.copy()
				container[900:1000,N:N+ex] = (0.35,0.35,0.35)
				cv2.putText(container, 'Undo (z)', (N+16,950), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)

	elif event==cv2.EVENT_MOUSEMOVE:
		container[0:100,N:N+ex] = (0.5,0.5,0)
		container[100:200,N:N+ex] = (0,0.5,0.5)
		container[200:300,N:N+ex] = (0.5,0,0.5)
		container[300:400,N:N+ex] = (0.5,0.3,0.1)
		container[400:500,N:N+ex] = (0.1,0.3,0.5)
		container[500:600,N:N+ex] = (0.5,0.1,0.3)
		container[600:700,N:N+ex] = (0.3,0.1,0.5)
		container[700:800,N:N+ex] = (0.3,0.5,0.1)
		container[800:900,N:N+ex] = (0.1,0.5,0.3)
		container[900:1000,N:N+ex] = (0.3,0.3,0.3)
		container[1000:1024,N:N+ex] = (1,1,1)

		cv2.putText(container, 'Erase (1)', (N+12,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Draw (2)', (N+14,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Remove (3)', (N+3,250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Fill (4)', (N+24,350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Pick (5)', (N+18,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Next (f)', (N+16,550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Prev (b)', (N+16,650), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Save (s)', (N+15,750), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Quit (q,esc)', (N+2,850), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		cv2.putText(container, 'Undo (z)', (N+16,950), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
		
		if drawing==True:
			if mode==1:
				cv2.line(pred3,(current_former_x,current_former_y),(former_x,former_y),(0,0,0),2)
				current_former_x = former_x
				current_former_y = former_y
			elif mode==2:
				cv2.line(pred3,(current_former_x,current_former_y),(former_x,former_y),(clr, clr, clr),2)
				current_former_x = former_x
				current_former_y = former_y
		if drawing==False:
			if former_y < 100 and former_y > 0:
				if former_x < N+ex and former_x > N:
					container[0:100,N:N+ex] = (0.45,0.45,0)
					cv2.putText(container, 'Erase (1)', (N+9,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 200 and former_y > 100:
				if former_x < N+ex and former_x > N:
					container[100:200,N:N+ex] = (0,0.45,0.45)
					cv2.putText(container, 'Draw (2)', (N+11,150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 300 and former_y > 200:
				if former_x < N+ex and former_x > N:
					container[200:300,N:N+ex] = (0.45,0,0.45)
					cv2.putText(container, 'Remove (3)', (N,250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 400 and former_y > 300:
				if former_x < N+ex and former_x > N:
					container[300:400,N:N+ex] = (0.45,0.25,0.05)
					cv2.putText(container, 'Fill (4)', (N+21,350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 500 and former_y > 400:
				if former_x < N+ex and former_x > N:
					container[400:500,N:N+ex] = (0.05,0.25,0.45)
					cv2.putText(container, 'Pick (5)', (N+15,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 600 and former_y > 500:
				if former_x < N+ex and former_x > N:
					container[500:600,N:N+ex] = (0.45,0.05,0.25)
					cv2.putText(container, 'Next (f)', (N+13,550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y <700 and former_y > 600:
				if former_x < N+ex and former_x > N:
					container[600:700,N:N+ex] = (0.25,0.05,0.45)
					cv2.putText(container, 'Prev (b)', (N+13,650), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 800 and former_y > 700:
				if former_x < N+ex and former_x > N:
					container[700:800,N:N+ex] = (0.25,0.45,0.05)
					cv2.putText(container, 'Save (s)', (N+12,750), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 900 and former_y > 800:
				if former_x < N+ex and former_x > N:
					container[800:900,N:N+ex] = (0.05,0.45,0.25)
					cv2.putText(container, 'Quit (q,esc)', (N,850), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			elif former_y < 1000 and former_y > 900:
				if former_x < N+ex and former_x > N:
					container[900:1000,N:N+ex] = (0.25,0.25,0.25)
					cv2.putText(container, 'Undo (z)', (N+16,950), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

	elif event==cv2.EVENT_LBUTTONUP:
		drawing=False
		if mode==1:
			cv2.line(pred3,(current_former_x,current_former_y),(former_x,former_y),(0,0,0),2)
			current_former_x = former_x
			current_former_y = former_y
		elif mode==2:
			cv2.line(pred3,(current_former_x,current_former_y),(former_x,former_y),(clr, clr, clr),2)
			current_former_x = former_x
			current_former_y = former_y
		elif mode==3:
			predc = pred3.copy()
			maskc = mask.copy()
			try:
				cv2.floodFill(pred3, maskc, (former_x,former_y), 0)
			except Exception:
				pass
		elif mode==4:
			predc = pred3.copy()
			maskc = mask.copy()
			try:
				cv2.floodFill(pred3, maskc, (former_x,former_y), clr)
			except Exception:
				pass
		elif mode==5 and former_x < N:
			clr = pred3[former_y,former_x]
			clr = int(clr)		

	return former_x,former_y

cv2.namedWindow('Select')
#cv2.resizeWindow('Select', 512, 512)
cv2.setMouseCallback('Select',draw)
		
while(1):
	K = cv2.waitKey(10) & 0xFF
	overlay = label2rgb(pred3, image=orig3, bg_label=0)
	#over = cv2.addWeighted(orig3, 0.5, pred3, 0.5, 0, over)
	container[0:M,0:N,:] = overlay
	display = container
	cv2.imshow('Select',display)

	if K == ord('f') or mode==6:	# Advance to Next Image
		if nme < MX:
			nme = nme + 1
		else:
			nme = nme
		NME = name[nme]
		print(NME)
		pred3, orig3, mask = load_image(NME, opath, saveP, ppath, rows, cols)
		mode = 0
	elif K == ord('b') or mode==7:	# Go Back to Previous Image
		if nme > MN:
			nme = nme - 1
		else:
			nme = nme
		NME = name[nme]
		print(NME)
		try:
			pred3, orig3, mask = load_image(NME, opath, saveP, saveP, rows, cols)
		except Exception:
			pred3, orig3, mask = load_image(NME, opath, saveP, ppath, rows, cols)
		mode = 0
	elif K == ord('s') or mode==8:		# Save Current Labels
		save_image(pred3, saveP, NME)
		mode = 0
	elif K == ord('q') or K == 27 or mode == 9:		# Quit
		quit()
	elif K == 48: # key: 0
		mode = 0
	elif K == 49: # key: 1
		mode = 1
	elif K == 50: # key: 2
		mode = 2
	elif K == 51: # key: 3
		mode = 3
	elif K == 52: # key: 4
		mode = 4
	elif K == 53: # key: 5
		mode = 5

	elif K == ord('z'):			# Undo Last
		#preda = pred3.copy()
		pred3 = predc.copy()
		
	elif K == ord('r'):			# Redo All
		pred3 = label(pred)
		pred3 = pred3.astype('uint8')
		
	elif K == ord('t'):
		zz = 1
		rows = int(rows*1.1)
		cols = int(cols*1.1)
		M=rows
		N=cols
		container = np.zeros((rows,cols+ex,3))
		pred3 = np.asarray(Image.fromarray(pred3).resize((rows,cols), Image.NEAREST))
		orig3 = np.asarray(Image.fromarray(orig3).resize((rows,cols), Image.NEAREST))

	elif K == ord('w'):
		zz = 2
		rows = int(rows*0.909)
		cols = int(cols*0.909)
		container = np.zeros((rows,cols+ex,3))
		M=rows
		N=cols
		pred3 = np.asarray(Image.fromarray(pred3).resize((rows,cols), Image.NEAREST))
		orig3 = np.asarray(Image.fromarray(orig3).resize((rows,cols), Image.NEAREST))
		#if rows >= sh[0] or cols >= sh[1]:
		#	 orig3 = cv2.cvtColor(orig3, cv2.COLOR_RGB2GRAY)
		#	 pred3 = cv2.resize(pred3, (rows, cols), cv2.INTER_NEAREST)
		#	 orig3 = bin_ndarray(orig3, (rows, cols), operation='mean')
		#	 orig3 = cv2.cvtColor(orig3.astype('uint8'), cv2.COLOR_GRAY2RGB)

cv2.destroyAllWindows()
