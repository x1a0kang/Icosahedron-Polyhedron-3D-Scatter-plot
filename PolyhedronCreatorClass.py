import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy
import math
from enum import Enum

class PolyhedronCreator:

    #初始化使用数组，存放正多面体的顶点
    x_init=[]
    y_init=[]
    z_init=[]

    #调整尺寸使用数组，分段时取出的点并不在外接球上，将所有点拉至外接球上后，存在这个数组中
    x_scaled = []
    y_scaled = []
    z_scaled = []

    #八十面体多取出的120条棱的中点，不需要拉伸至外接球上，存在这个数组中
    x_plus = []
    y_plus = []
    z_plus = []

    #给所有点编号，按编号顺序排列
    x_label = []
    y_label = []
    z_label = []

    #创建过程一直以原点为圆心，将所有点移动至设定的圆心周围后，存在这个数组中
    x_moved = []
    y_moved = []
    z_moved = []
    
    
    def creatIcosahedrons(self,x,y,z,r,s):

        #若正二十面体的中心为(0,0,0)，外接球半径为1，各顶点的坐标为{(±m,0,±n), (0,±n,±m), (±n,±m,0)}
        #这样初始化正二十面体，1号点周围是一个六角形

        # m = pow(50-10*pow(5,0.5),0.5)/10
        # n = pow(50+10*pow(5,0.5),0.5)/10

        # self.x_init=[m,m,-m,-m,0,0,0,0,n,n,-n,-n]
        # self.y_init=[0,0,0,0,n,n,-n,-n,m,-m,m,-m]
        # self.z_init=[n,-n,n,-n,m,-m,m,-m,0,0,0,0]

        #这样初始化正二十面体，1号点周围是一个五角形，和搭建的球相同
        self.x_init=[0.0, 0.7236068248748779, -0.27639326453208923, -0.8944272994995117, -0.2763932943344116, 0.7236067652702332, 0.8944272994995117, 0.27639317512512207, -0.7236068844795227, -0.7236067652702332, 0.276393324136734, 0.0]
        self.y_init=[0.0, 0.525731086730957, 0.8506509065628052, -7.819331671043983e-08, -0.8506507873535156, -0.5257311463356018, 0.0, 0.8506508469581604, 0.525731086730957, -0.5257312059402466, -0.8506507873535156, 0.0]
        self.z_init=[-1.0, -0.4472135901451111, -0.44721364974975586, -0.44721364974975586, -0.4472135901451111, -0.4472135901451111, 0.44721364974975586, 0.4472135901451111, 0.44721364974975586, 0.4472135901451111, 0.4472135901451111, 1.0]

        #1.分段
        self.__split__(s)

        #2.拉伸至外接球
        self.__scale__(r)

        #3.八十面体额外需要取棱的中点
        if(s == 2):
            self.__additional__()

        #4.加编号标签
        self.__label__(s)

        #5.移动至设定的球心
        self.__move__(x,y,z)

        
        
    def __split__(self,s):
        
        #球的棱长a和半径r的关系
        a = round(4 / (pow(10+2*pow(5,0.5),0.5)),3)

        if (s == 1):
            print("创建正二十面体")

        if(s == 2):
            
            print("创建八十面体")

            #取二十面体的所有棱的中点
            for i in range(12):
                for j in range(i+1,12):
                    #计算12个顶点之间的距离，如果等于棱长，则取中点
                    temp_a = pow((self.x_init[i]-self.x_init[j])**2+(self.y_init[i]-self.y_init[j])**2+(self.z_init[i]-self.z_init[j])**2,0.5)
                    
                    if(round(temp_a,3) == a):
                        self.x_init.append((self.x_init[i]+self.x_init[j])/2)
                        self.y_init.append((self.y_init[i]+self.y_init[j])/2)
                        self.z_init.append((self.z_init[i]+self.z_init[j])/2)

            #print("取棱的中点",len(self.x_init))


    def __scale__(self,r):

        #求出球心与各个点的连线的方程和外接球的方程，得到交点
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        z = sympy.Symbol('z')

        for n1 in range(len(self.x_init)):
            
            #如果x坐标为零，可能有3种情况：x,y为零；x,z为零；只有x为零
            if(self.x_init[n1]==0):
                self.x_scaled.append(0)
                
                #x,y为零
                if((self.y_init[n1]==0)):

                    self.y_scaled.append(0)
                    if(self.z_init[n1]>0):
                        self.z_scaled.append(r)
                    else:
                        self.z_scaled.append(-r)

                #x,z为零
                elif(self.z_init[n1]==0):

                    self.z_scaled.append(0)
                    if(self.y_init[n1]>0):
                        self.y_scaled.append(r)
                    else:
                        self.y_scaled.append(-r)

                #只有x为零
                else:
                    points = sympy.solve([y**2+z**2-r**2,z/self.z_init[n1]-y/self.y_init[n1]],[y,z])
                    #这样算出是两个交点，计算这两个交点与原来的点之间的距离，取距离小于半径的点
                    temp_x0 = pow((points[0][0]-self.y_init[n1])**2+(points[0][1]-self.z_init[n1])**2,0.5)
                    if(temp_x0<r):
                        self.y_scaled.append(points[0][0])
                        self.z_scaled.append(points[0][1])
                    else:
                        self.y_scaled.append(points[1][0])
                        self.z_scaled.append(points[1][1])

            
            #如果y坐标为零，可能有2种情况：y,z为零；只有y为零
            elif(self.y_init[n1]==0):
                self.y_scaled.append(0)

                #y,z为零
                if(self.z_init[n1]==0):
                
                    self.z_scaled.append(0)
                    if(self.x_init[n1]>0):
                        self.x_scaled.append(r)
                    else:
                        self.x_scaled.append(-r)

                #只有y为零
                else:
                    points = sympy.solve([x**2+z**2-r**2,z/self.z_init[n1]-x/self.x_init[n1]],[x,z])
                    #这样算出是两个交点，计算这两个交点与原来的点之间的距离，取距离小于半径的点
                    temp_y0 = pow((points[0][0]-self.x_init[n1])**2+(points[0][1]-self.z_init[n1])**2,0.5)
                    if(temp_y0<r):
                        self.x_scaled.append(points[0][0])
                        self.z_scaled.append(points[0][1])
                    else:
                        self.x_scaled.append(points[1][0])
                        self.z_scaled.append(points[1][1])


            #如果z坐标为零，只有z为零
            elif(self.z_init[n1]==0):
                self.z_scaled.append(0)

                points = sympy.solve([y**2+x**2-r**2,x/self.x_init[n1]-y/self.y_init[n1]],[x,y])
                #这样算出是两个交点，计算这两个交点与原来的点之间的距离，取距离小于半径的点
                temp_z0 = pow((points[0][0]-self.x_init[n1])**2+(points[0][1]-self.y_init[n1])**2,0.5)
                if(temp_z0<r):
                    self.x_scaled.append(points[0][0])
                    self.y_scaled.append(points[0][1])
                else:
                    self.x_scaled.append(points[1][0])
                    self.y_scaled.append(points[1][1])

            
            #三个坐标都不为零
            else:    
                points = sympy.solve([x**2+y**2+z**2-r**2, x/self.x_init[n1]-y/self.y_init[n1], x/self.x_init[n1]-z/self.z_init[n1], z/self.z_init[n1]-y/self.y_init[n1]],[x,y,z])
                #这样算出是两个交点，计算这两个交点与原来的点之间的距离，取距离小于半径的点
                temp_0 = pow((points[0][0]-self.x_init[n1])**2+(points[0][1]-self.y_init[n1])**2+(points[0][2]-self.z_init[n1])**2,0.5)
                if(temp_0<r):
                    self.x_scaled.append(points[0][0])
                    self.y_scaled.append(points[0][1])
                    self.z_scaled.append(points[0][2])
                else:
                    self.x_scaled.append(points[1][0])
                    self.y_scaled.append(points[1][1])
                    self.z_scaled.append(points[1][2])

        #令所有数据格式为float
        for i in range (0,len(self.z_scaled)):
            self.x_scaled[i]=float(self.x_scaled[i])
            self.y_scaled[i]=float(self.y_scaled[i])
            self.z_scaled[i]=float(self.z_scaled[i])
    
        #print("拉伸到外界球上42",len(self.x_scaled))


    def __additional__(self):
        
        temp_list = []
        #取八十面体的所有棱的中点，不取的话只有42个顶点，取了中点是162个点
        #计算所有点之间的距离，放在一个数组里，最小的两个距离就是八十面体的两种棱长
        #计算每个点之间的距离，放在数组里，再升序排列
        for i in range(len(self.x_scaled)):
            for j in range(i+1,len(self.x_scaled)):
                temp_list.append(pow((self.x_scaled[i]-self.x_scaled[j])**2+(self.y_scaled[i]-self.y_scaled[j])**2+(self.z_scaled[i]-self.z_scaled[j])**2,0.5))

        temp_list.sort()
        #print(len(temp_list))

        #从第96号开始第二种棱长，到119号
        #八十面体有120条棱，所以数组中的第【0】和【119】号元素是两个棱长
        for i in range(len(self.x_scaled)):
            for j in range(i+1,len(self.x_scaled)):
                temp_b = pow((self.x_scaled[i]-self.x_scaled[j])**2+(self.y_scaled[i]-self.y_scaled[j])**2+(self.z_scaled[i]-self.z_scaled[j])**2,0.5)
                if(round(temp_b,3) == round(temp_list[0],3) or round(temp_b,3) == round(temp_list[119],3)):
                    self.x_plus.append((self.x_scaled[i]+self.x_scaled[j])/2)
                    self.y_plus.append((self.y_scaled[i]+self.y_scaled[j])/2)
                    self.z_plus.append((self.z_scaled[i]+self.z_scaled[j])/2)
                    #print(temp_b)

        #将所有数据限制为float
        for i in range (0,len(self.z_plus)):
            self.x_plus[i]=float(self.x_plus[i])
            self.y_plus[i]=float(self.y_plus[i])
            self.z_plus[i]=float(self.z_plus[i])
        
        #print(len(self.x_plus))


    def __label__(self,s):
        
        self.x_label = self.x_scaled + self.x_plus
        self.y_label = self.y_scaled + self.y_plus
        self.z_label = self.z_scaled + self.z_plus

        x_moved_sorted = []
        y_moved_sorted = []
        z_moved_sorted = []

        #这里用sorted排序后不会修改原列表中的顺序，key后表示的是 按照第二个元素进行排序
        #enumerate()是将列表中的每个元素和序号组成一组，第一个是序号，第二个是内容
        z_moved_sorted = sorted(enumerate(self.z_label), key=lambda x:x[1])
        #print(z_moved_sorted[0][0])

        for i in range(len(self.z_label)):
            x_moved_sorted.append(self.x_label[z_moved_sorted[len(self.z_label)-1-i][0]])
            y_moved_sorted.append(self.y_label[z_moved_sorted[len(self.z_label)-1-i][0]])

        #到这里还不是精确的顺序，每层之内的点顺序还是乱的
        self.x_label = x_moved_sorted.copy()
        self.y_label = y_moved_sorted.copy()
        self.z_label = sorted(self.z_label,reverse=True).copy()
        # print(self.z_label[1:6])
        # print(self.x_label[1:6])
        # print(self.y_label[1:6])


        if(s == 1):
            self.x_label = self.x_scaled.copy()
            self.y_label = self.y_scaled.copy()
            self.z_label = self.z_scaled.copy()

            self.x_label.reverse()
            self.y_label.reverse()
            self.z_label.reverse()
        

        if(s == 2):

            #接下来分层利用角度进行排序
            #a×b表示从a旋转到b，叉乘得到的向量中，z值正表示逆时针，z值负表示顺时针
            #以x轴转向圆心与点所连向量的旋转角为判断条件，由小到大

            angle_all = []
            layer1_angle = []
            layer2_angle = []
            layer3_angle = []
            layer4_angle = []
            layer5_angle = []
            layer6_angle = []
            layer7_angle = []
            layer8_angle = []
            layer9_angle = []
            layer10_angle = []
            layer11_angle = []
            
            for i in range(1,len(self.x_label)-1):
                #layer1.append([self.x_label[i],self.y_label[i],self.z_label[i]])
                #两向量
                vector_x = [1,0,0]
                vector_temp = [self.x_label[i],self.y_label[i],0]
                #点乘和叉乘算角度
                angle = math.acos(np.dot(vector_x,vector_temp)/(np.linalg.norm(vector_x)*np.linalg.norm(vector_temp)))
                normal = np.cross(vector_x,vector_temp)[2]
                if(normal > 0):
                    angle = 2*math.pi - angle
                # elif(normal == 0):
                #     print("叉乘后z轴值为零", i)

                #这里不包括第一个点和最后一个点，所有只有160个值
                angle_all.append(angle)
            
            #print(len(angle_all))

            layer1_angle = angle_all[:5]
            layer1_angle = enumerate(layer1_angle,start=1)
            layer1_angle = sorted(layer1_angle, key=lambda x:x[1])
            #print(len(layer1_angle))
            #print(layer1_angle)
            
            layer2_angle = angle_all[5:15]
            layer2_angle = enumerate(layer2_angle,start=6)
            layer2_angle = sorted(layer2_angle, key=lambda x:x[1])
            #print(len(layer2_angle))
            #print(layer2_angle)
            
            layer3_angle = angle_all[15:30]
            layer3_angle = enumerate(layer3_angle,start=16)
            layer3_angle = sorted(layer3_angle, key=lambda x:x[1])
            #print(len(layer3_angle))
            #print(layer3_angle)

            layer4_angle = angle_all[30:50]
            layer4_angle = enumerate(layer4_angle,start=31)
            layer4_angle = sorted(layer4_angle, key=lambda x:x[1])
            #print(len(layer4_angle))
            #print(layer4_angle)

            layer5_angle = angle_all[50:70]
            layer5_angle = enumerate(layer5_angle,start=51)
            layer5_angle = sorted(layer5_angle, key=lambda x:x[1])
            #print(len(layer5_angle))
            #print(layer5_angle)

            layer6_angle = angle_all[70:90]
            layer6_angle = enumerate(layer6_angle,start=71)
            layer6_angle = sorted(layer6_angle, key=lambda x:x[1])
            #print(len(layer6_angle))
            #print(layer6_angle)
            
            layer7_angle = angle_all[90:110]
            layer7_angle = enumerate(layer7_angle,start=91)
            layer7_angle = sorted(layer7_angle, key=lambda x:x[1])
            #print(len(layer7_angle))
            #print(layer7_angle)
            
            layer8_angle = angle_all[110:130]
            layer8_angle = enumerate(layer8_angle,start=111)
            layer8_angle = sorted(layer8_angle, key=lambda x:x[1])
            #print(len(layer8_angle))
            #print(layer8_angle)
            
            layer9_angle = angle_all[130:145]
            layer9_angle = enumerate(layer9_angle,start=131)
            layer9_angle = sorted(layer9_angle, key=lambda x:x[1])
            #print(len(layer9_angle))
            #print(layer9_angle)
            
            layer10_angle = angle_all[145:155]
            layer10_angle = enumerate(layer10_angle,start=146)
            layer10_angle = sorted(layer10_angle, key=lambda x:x[1])
            #print(len(layer10_angle))
            #print(layer10_angle)

            layer11_angle = angle_all[155:160]
            layer11_angle = enumerate(layer11_angle,start=156)
            layer11_angle = sorted(layer11_angle, key=lambda x:x[1])
            #print(len(layer11_angle))
            #print(layer11_angle)
            
            angle_all.clear()
            angle_all = layer1_angle+layer2_angle+layer3_angle+layer4_angle+layer5_angle+layer6_angle+layer7_angle+layer8_angle+layer9_angle+layer10_angle+layer11_angle
            #print(angle_all[0][0])

            x_moved_sorted.clear()
            y_moved_sorted.clear()
            z_moved_sorted.clear()

            x_moved_sorted.append(self.x_label[0])
            y_moved_sorted.append(self.y_label[0])
            z_moved_sorted.append(self.z_label[0])

            for i in range(len(angle_all)):
                x_moved_sorted.append(self.x_label[angle_all[i][0]])
                y_moved_sorted.append(self.y_label[angle_all[i][0]])
                z_moved_sorted.append(self.z_label[angle_all[i][0]])

            x_moved_sorted.append(self.x_label[161])
            y_moved_sorted.append(self.y_label[161])
            z_moved_sorted.append(self.z_label[161])

            self.x_label = x_moved_sorted.copy()
            self.y_label = y_moved_sorted.copy()
            self.z_label = z_moved_sorted.copy()


        #将所有数据限制为float
        for i in range (0,len(self.z_label)):
            self.x_label[i]=float(self.x_label[i])
            self.y_label[i]=float(self.y_label[i])
            self.z_label[i]=float(self.z_label[i])


    def __move__(self,x,y,z):

        self.x_moved = np.array([x]*len(self.x_label))+np.array(self.x_label)
        self.y_moved = np.array([y]*len(self.y_label))+np.array(self.y_label)
        self.z_moved = np.array([z]*len(self.z_label))+np.array(self.z_label)

        #画图
        fig = plt.figure()
        ax = Axes3D(fig)
        #ax.scatter(self.x_scaled,self.y_scaled,self.z_scaled)
        ax.scatter(self.x_moved,self.y_moved,self.z_moved)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        #标记序号
        for i in range(len(self.x_moved)):
            ax.text(x=self.x_moved[i],y=self.y_moved[i],z=self.z_moved[i],s=i+1,fontsize=8)

        plt.show()



poly = PolyhedronCreator()
poly.creatIcosahedrons(0,0,0,2,2)