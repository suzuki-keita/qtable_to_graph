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
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

if len(args) == 3:
    READFILE_NAME = args[1]
    WRITEFILE_NAME = args[2]
else:
    print("Error! 第一引数にREADFILE_NAME,第二引数にWRITEFILE_NAME")
    sys.exit(1)

class main:
    def __init__(self):
        #範囲と間隔の設定
        self.filename = []
        self.route_length = []
        self.goal_direction = []
        self.start_direction = []
        with open(READFILE_NAME, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                self.filename.append(row[0])
                self.route_length.append(float(row[1]))
                self.goal_direction.append(float(row[2]))
                self.start_direction.append(float(row[3]))
    
        #標準化
        x = self.zscore(self.route_length)
        y = self.zscore(self.goal_direction)
        #8つのcategoryに分ける
        """
        ①route_lengthの長い、短い
        ②goal_directionの北・東・南・西

        ①・②
        長・北：category0
        長・東：category1
        長・南：category2
        長・西：category3
        短・北：category4
        短・東：category5
        短・南：category6
        短・西：category7
        """
        category_data = []
        for i in range(0, len(self.filename)):
            if x[i] >= X_NORM and self.decide_goal_direction(i) == NORTH:
                category_data.append([self.filename[i], 0])
            elif x[i] >= X_NORM and self.decide_goal_direction(i) == EAST:
                category_data.append([self.filename[i], 1])
            elif x[i] >= X_NORM and self.decide_goal_direction(i) == SOUTH:
                category_data.append([self.filename[i], 2])
            elif x[i] >= X_NORM and self.decide_goal_direction(i) == WEST:
                category_data.append([self.filename[i], 3])
            elif x[i] < X_NORM and self.decide_goal_direction(i) == NORTH:
                category_data.append([self.filename[i], 4])
            elif x[i] < X_NORM and self.decide_goal_direction(i) == EAST:
                category_data.append([self.filename[i], 5])
            elif x[i] < X_NORM and self.decide_goal_direction(i) == SOUTH:
                category_data.append([self.filename[i], 6])
            elif x[i] < X_NORM and self.decide_goal_direction(i) == WEST:
                category_data.append([self.filename[i], 7])
        self.write_category(WRITEFILE_NAME, category_data)

        #2Dプロット
        fig, ax = plt.subplots()
        ax.scatter(np.ravel(x), np.ravel(y))
        ax.set_xlabel("route_length")
        ax.set_ylabel("route_rotation")
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

    def decide_goal_direction(self, _i):
        if self.goal_direction[_i] >= -45 and self.goal_direction[_i] < 45:
            return EAST
        elif self.goal_direction[_i] >= -135 and self.goal_direction[_i] < -45:
            return NORTH
        elif self.goal_direction[_i] >= 45 and self.goal_direction[_i] < 135:
            return SOUTH
        else:
            return WEST
    
if __name__ == '__main__':
    main()
