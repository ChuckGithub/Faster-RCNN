# -*- coding: utf-8 -*-

#---某些xml文件中可能会不存在gt框，会导致训练过程出错----#

import os
import xml.etree.ElementTree as ET


xml_dir = '/path/to/faster_rcnn/datasets/Caltech/Caltech/Annotations/'
save_error_xml = 'error.txt'

ele_none = 0
obj_none = 0

fw = open(save_error_xml,'a')

for parent, dirnames, filenames in os.walk(xml_dir):         #得到所有的xml文件
    for filename in filenames:
        print (parent+filename)
        xml_path  = parent+filename
        root = ET.parse(xml_path)                            # 加载文件
        obj_ele = root.findall('object')                     #找到gt框
        if len(obj_ele) != 0:                                # 获取gt框个数
            # print (len(obj_ele))
            for obj_ele_list in obj_ele:
                for o_ele in obj_ele_list:
                    if o_ele.tag == 'bndbox':                #得到xmin,ymin,xmax,ymax
                        for i in range(0, 4):
                            # print (len(o_ele))
                            if o_ele.getchildren()[i].text is not None:
                                # print ('ele is:' + o_ele.getchildren()[i].text)
                                pass
                            else:
                                fw.write(xml_path)
                                fw.write('\n')
                                ele_none += 1
                                print ('null')
        else:
            fw.write(xml_path)
            fw.write('\n')
            obj_none += 1
            print ('NULL')

fw.close()


print ('Done!')
print ('gt框值有为0的文件个数为：'+ele_none)
print ('object不存在的文件个数为：'+obj_none)
