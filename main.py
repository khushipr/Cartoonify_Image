import cv2 #for image processing
import easygui #to open the filebox
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *

# Main window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))

def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    # read the image
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

    if originalImage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    resized1 = cv2.resize(originalImage, (960, 540))

    # converting original image into gray-scale
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    resized2 = cv2.resize(grayScaleImage, (960, 540))

    # applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    resized3 = cv2.resize(smoothGrayScale, (960, 540))

    # retrieving edges for cartoon effect using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    resized4 = cv2.resize(getEdge, (960, 540))

    # applying bilateral filter to remove noise and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalImage, 9, 300, 300)
    resized5 = cv2.resize(colorImage, (960, 540))

    # masking edged image with beautified image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    resized6 = cv2.resize(cartoonImage, (960, 540))

    # displaying the whole transition
    images = [resized1, resized2, resized3, resized4, resized5, resized6]
    fig, axes = plt.subplots(3, 2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    # Save button for cartoonised image
    save1 = Button(top, text="Save cartoon image", command=lambda: save(resized6, ImagePath), padx=30, pady=5)
    save1.configure(background='#364156', font=('calibri', 10, 'bold'))
    save1.pack(side=TOP, pady=50)

    plt.show()

def save(resized6, ImagePath):
    # saving an image using imwrite()
    modified = "cartoonified_image"
    path_name = os.path.dirname(ImagePath)
    extension_name = os.path.splitext(ImagePath)[1]
    final_path = os.path.join(path_name, modified+extension_name)
    cv2.imwrite(final_path, cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR))
    confirmation = "Image saved by name " + modified + " at " + final_path
    tk.messagebox.showinfo(title=None, message=confirmation)

# Uploading an image button
upload = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)

# For running the main window of tkinter
top.mainloop()