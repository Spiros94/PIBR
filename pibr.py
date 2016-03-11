import Tkinter, tkFileDialog, tkSimpleDialog
import numpy as np
import csv
from PIL import Image  # For reading the image


def main():
    root = Tkinter.Tk()
    root.withdraw()
    inputImg = tkFileDialog.askopenfilename()
    print '[+] Open File'
    print "[+] Input File: " + inputImg

    if inputImg == "":
        raise NameError("Input image not found")

    outputFile = tkFileDialog.asksaveasfilename(**{'title': "Save As", 'defaultextension': '.csv', 'initialfile': 'output'})
    print "[+] Output File Name: " + outputFile

    # Columns:Upper Left X		Upper Left Y	 Down Right X	 Down Right Y	 Block Interval
    TABLE = {'UL_X': [],      'UL_Y': [],      'DR_X': [],     'DR_Y': [],     'interval': [], 'imgWidth': [], 'imgHeight': [], 'pixelValue': []}
    img = Image.open(inputImg, 'r')  # Read the image

    A = np.zeros((img.height, img.width), dtype=np.int)  # zero out a table equal to the image size
    Num = 1

    #  Init values
    tableAppend(TABLE, 0, 0, 0, 0, 1, img.width, img.height, img.getpixel((0, 0)))
    A[0][0] = Num

    # Get values from the first line only
    for i in xrange(1, img.width):  # min-index of pixels = 0, starting from the second pixel
        if img.getpixel((i, 0)) == img.getpixel((i-1, 0)):
            TABLE['DR_X'][-1] = i  # change the last element of DR_X list
            TABLE['interval'][-1] += 1  # increase the interval of the last element
        else:
            tableAppend(TABLE, i, 0, i, 0, 1, img.width, img.height, img.getpixel((i, 0)))
            Num += 1
            A[0][i] = Num

    tableAppend(TABLE, 0, 1, 0, 1, 1, img.width, img.height, img.getpixel((0, 1)))  # start a new line
    for j in xrange(1, img.height):  # for every column
        tableChangeLastLines(TABLE, 0, j, 0, j, 1, img.width, img.height, img.getpixel((0, j)))  # start a new line
        for i in xrange(1, img.width):  # for every row
            if img.getpixel((i, j)) == img.getpixel((i-1, j)):  # if two pixels in a row are the same
                TABLE['DR_X'][-1] = i
                TABLE['interval'][-1] += 1
            else:
                interval = TABLE['interval'][-1]  # get last interval
                AA = A[j-1][(TABLE['UL_X'][-1])]

                if (AA > 0) and (TABLE['pixelValue'][-1] == TABLE['pixelValue'][AA-1]) and (TABLE['interval'][-1] == TABLE['interval'][AA-1]):
                    TABLE['DR_Y'][AA-1] = j
                    A[j][i - interval] = AA
                else:
                    tableDuplicateLastLines(TABLE)
                    Num += 1
                    A[j][i - interval] = Num
                TABLE['UL_X'][-1] = i
                TABLE['DR_X'][-1] = i
                TABLE['interval'][-1] = 1
                TABLE['pixelValue'][-1] = img.getpixel((i, j))

        interval2 = TABLE['interval'][-1]
        AA2 = A[j-1][(TABLE['UL_X'][-1])]

        if (AA2 > 0) and (TABLE['pixelValue'][-1] == TABLE['pixelValue'][AA2-1]) and (TABLE['interval'][AA2-1] == TABLE['interval'][-1]):
            TABLE['DR_Y'][AA2-1] = j
            A[j][(img.width-interval2)] = AA2
        else:
            tableDuplicateLastLines(TABLE)
            Num += 1
            A[j][(img.width-interval2)] = Num

    for key, value in TABLE.iteritems():  # remove the last buffer elements
        del TABLE[key][-1]
    print "[+] Exporting Results"
    with open(outputFile, 'wb') as f:  # output the results
        w = csv.DictWriter(f, TABLE.keys())
        w.writeheader()
        w.writerow(TABLE)
    print "[+] Done!"
# <>main


def tableAppend(TABLE, UL_X, UL_Y, DR_X, DR_Y, interval, imgWidth, imgHeight, pixelValue):
    # Pass by reference mutable table(dictionary) and add one element in each list
    TABLE['UL_X'].append(UL_X)
    TABLE['UL_Y'].append(UL_Y)
    TABLE['DR_X'].append(DR_X)
    TABLE['DR_Y'].append(DR_Y)
    TABLE['interval'].append(interval)
    TABLE['imgWidth'].append(imgWidth)
    TABLE['imgHeight'].append(imgHeight)
    TABLE['pixelValue'].append(pixelValue)


def tableChangeLastLines(TABLE, UL_X, UL_Y, DR_X, DR_Y, interval, imgWidth, imgHeight, pixelValue):
    # Pass by reference mutable table(dictionary) and change the elements
    TABLE['UL_X'][-1] = UL_X
    TABLE['UL_Y'][-1] = UL_Y
    TABLE['DR_X'][-1] = DR_X
    TABLE['DR_Y'][-1] = DR_Y
    TABLE['interval'][-1] = interval
    TABLE['imgWidth'][-1] = imgWidth
    TABLE['imgHeight'][-1] = imgHeight
    TABLE['pixelValue'][-1] = pixelValue


def tableDuplicateLastLines(TABLE):
    # Duplicates the last element of every list in the table
    for key, value in TABLE.iteritems():
        TABLE[key].append(TABLE[key][-1])


if __name__ == "__main__":
    main()
