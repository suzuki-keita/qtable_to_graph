#!/usr/local/bin python
# -*- coding:utf-8 -+-
import csv
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
DATAFILE_NAME = "infomation.csv"

class main:
    def __init__(self):
        #範囲と間隔の設定
        filename = []
        route_length = []
        route_rotation = []
        route_possibility = []
        with open(DATAFILE_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                filename.append(row[0])
                route_length.append(float(row[1]))
                route_rotation.append(float(row[2]))
                route_possibility.append(float(row[3]))
    
        #正規化
        x = self.zscore(route_length)
        y = self.zscore(route_rotation)
        z = self.zscore(route_possibility)

        fig = plt.figure()
        ax = Axes3D(fig)
        #プロット
        ax.scatter3D(np.ravel(x),np.ravel(y),np.ravel(z))
        ax.set_xlabel("route_length")
        ax.set_ylabel("route_rotation")
        ax.set_zlabel("route_possibility")
        
        #プロットにテキスト表示（重い）
        for (i,s) in enumerate(zip(x,y,z)):
            ax.text(s[0],s[1],s[2],str(i),size=7)
        plt.show()

    def zscore(self,x, axis = None):
        xmean = np.mean(x,axis=axis, keepdims=True)
        xstd  = np.std(x, axis=axis, keepdims=True)
        zscore = (x-xmean)/xstd
        return zscore

if __name__ == '__main__':
    main()