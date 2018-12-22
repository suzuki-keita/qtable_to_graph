#!/usr/local/bin python
# -*- coding:utf-8 -+-
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

args = sys.argv
"""
X_NORM = 0.26621526175145216
Y_NORM = -0.13772006553375682
Z_NORM = -0.1213336553313068
"""
X_NORM = 0
Y_NORM = 0
Z_NORM = 0

if len(args) == 3:
    READFILE_NAME = args[1]
    WRITEFILE_NAME = args[2]
else:
    print("Error! 第一引数にREADFILE_NAME,第二引数にWRITEFILE_NAME")
    sys.exit(1)

class main:
    def __init__(self):
        #範囲と間隔の設定
        filename = []
        route_length = []
        route_rotation = []
        route_possibility = []
        with open(READFILE_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                filename.append(row[0])
                route_length.append(float(row[1]))
                route_rotation.append(float(row[2]))
                route_possibility.append(float(row[3]))
    
        #標準化
        x = self.zscore(route_length)
        y = self.zscore(route_rotation)
        z = self.zscore(route_possibility)

        #8つのcategoryに分ける
        """
        ①route_lengthの長い、短い
        ②route_rotationの多い、少ない
        ③route_possibilityの多い、少ない

        ①・②・③
        長・多・多：category0
        長・多・少：category1
        長・少・多：category2
        長・少・少：category3
        短・多・多：category4
        短・多・少：category5
        短・少・多：category6
        短・少・少：category7
        """
        category_data = []
        for i in range(0,len(filename)):
            if x[i] >= X_NORM and y[i] >= Y_NORM and z[i] >= Z_NORM:
                category_data.append([filename[i],0])
            elif x[i] >= X_NORM and y[i] >= Y_NORM and z[i] < Z_NORM:
                category_data.append([filename[i], 1])
            elif x[i] >= X_NORM and y[i] < Y_NORM and z[i] >= Z_NORM:
                category_data.append([filename[i], 2])
            elif x[i] >= X_NORM and y[i] < Y_NORM and z[i] < Z_NORM:
                category_data.append([filename[i], 3])
            elif x[i] < X_NORM and y[i] >= Y_NORM and z[i] >= Z_NORM:
                category_data.append([filename[i], 4])
            elif x[i] < X_NORM and y[i] >= Y_NORM and z[i] < Z_NORM:
                category_data.append([filename[i], 5])
            elif x[i] < X_NORM and y[i] < Y_NORM and z[i] >= Z_NORM:
                category_data.append([filename[i], 6])
            elif x[i] < X_NORM and y[i] < Y_NORM and z[i] < Z_NORM:
                category_data.append([filename[i], 7])
        self.write_category(WRITEFILE_NAME, category_data)

        #3Dプロット
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter3D(np.ravel(x),np.ravel(y),np.ravel(z))
        ax.set_xlabel("route_length")
        ax.set_ylabel("route_rotation")
        ax.set_zlabel("route_possibility")
        #プロットにテキスト表示（重い）
        """
        for (i,s) in enumerate(zip(x,y,z)):
            ax.text(s[0],s[1],s[2],str(i),size=7)
        """
        plt.show()
 
        
    def zscore(self,x, axis = None):
        xmean = np.mean(x,axis=axis, keepdims=True)
        xstd  = np.std(x, axis=axis, keepdims=True)
        zscore = (x-xmean)/xstd
        return zscore

    def write_category(self, _filename, _data):
        with open(_filename, mode="w") as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerows(_data)
        return 0
    
if __name__ == '__main__':
    main()
