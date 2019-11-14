
"""
@author: Gauhar Bains
"""

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import random 


def check_plane(plane_equation,dimensions):    
    
    """
            Inputs :
            plane_equation is a tuple/list of four elements
            of the form (a,b,c,d) where a,b,c,d represent 
            the equation of the plane. 
            The equation of the plane is ax+by+cz+d=0            
            
            dimensions is a tuple of the form (d,h,w) 
            where d is the depth. h is the height,
            w is the widht of the 3d image"""
        
    depth,height,width=dimensions
    a,b,c,d=plane_equation    
    truth=True
    for i in [(0,0),(width,0),(0,height),(width,height)]:
        y,z=i
        x= round(-1*(d+c*z+b*y)*(1/a))
        if not x in range(depth+1):
            truth=False            
    return truth       

def get_random_valid_plane(dimensions):
    depth,height,width=dimensions     
    while True:        
        x1,x2,x3=random.sample(range(35),3)
        p1,p2,p3=[np.array([x1,0,0]),np.array([x2,0,height]),np.array([x3,width,height])]
        cp=np.cross(p3-p1,p2-p1)
        a,b,c=cp
        d=-1*np.dot(cp,p3)
        plane_equation=[a,b,c,d]
        if check_plane(plane_equation,dimensions):
            print('The equation is {0}x + {1}y + {2}z = {3}'.format(a/d, b/d, c/d, d/d))
            break
    return plane_equation
       
def get_slice(image_4d):
    image_3d_1channel=image_4d[:,:,:,0]
    """ In the coordinate system used, 
        x is the depth, z the height, 
        and y the width of the image"""
    x_len,z_len,y_len=image_3d_1channel.shape
    dimensions=(x_len,z_len,y_len)     
    plane_equation=get_random_valid_plane(dimensions) 
    a,b,c,d=plane_equation                                                       
    projection_1=np.zeros((z_len,y_len))
    projection_2=np.zeros((z_len,y_len))    
    row,col=(z_len-1,0)
    count=0
    output=[]   
    for z in range(z_len):
        for y in range(y_len):
            x= (-d-b*y-c*z)/a
            x=int(round(x))             
            if x in range(0,x_len):         
                projection_1[row,col]=image_4d[x_len-x-1,z_len-z-1,y,0]
                projection_2[row,col]=image_4d[x_len-x-1,z_len-z-1,y,1]                
                col+=1
                count+=1
        row-=1
        col=0 
    plt.imshow(projection_1)
    plt.show()    
    output=np.dstack((projection_1,projection_2))   
    return output    

path_to_image=''    
image_4d = io.imread(path_to_image)
"""Plane equation is of the form ax+by+cz-d=0"""

output_image=get_slice(image_4d)


        
        
        
        

