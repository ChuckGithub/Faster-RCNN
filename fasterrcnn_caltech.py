# -*- coding:utf-8 -*-

#---根据yolo v2文件训练格式（class_id x_center y_center width height）（后面四个数值为相对位置）转化为Faster RCNN训练要求格式（参考Pascal VOC）---#

import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom


def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作

def CreateXml(savepath,filename,li,isobject):
    if li is not None:
        # 创建根节点
        annotation_ele = ET.Element("annotation")
        # 创建folder子节点
        folder_ele = ET.SubElement(annotation_ele, "folder")
        folder_ele.text = "Caltech"

        # filename节点
        filename_ele = ET.SubElement(annotation_ele, "filename")
        filename_ele.text = filename + '.jpg'

        # source节点
        source_ele = ET.SubElement(annotation_ele, "source")

        # source节点的database子节点
        s_database_ele = ET.SubElement(source_ele, "database")
        s_database_ele.text = "Caltech Database"

        # source节点的annotation子节点
        s_annotation_ele = ET.SubElement(source_ele, "annotation")
        s_annotation_ele.text = "VOC2007"

        # source节点的image子节点
        s_image_ele = ET.SubElement(source_ele, "image")
        s_image_ele.text = "NULL"

        # source节点的flickrid子节点
        s_flickrid_ele = ET.SubElement(source_ele, "flickrid")
        s_flickrid_ele.text = "NULL"

        # owner节点
        owner_ele = ET.SubElement(annotation_ele, "owner")

        # owner节点的flickrid子节点
        o_flickrid_ele = ET.SubElement(owner_ele, "flickrid")
        o_flickrid_ele.text = "NULL"

        # owner节点的name子节点
        o_name_ele = ET.SubElement(owner_ele, "name")
        o_name_ele.text = "chuck"

        # size节点
        size_ele = ET.SubElement(annotation_ele, "size")

        # size节点的width子节点
		#Caltech图片大小固定（640*480）
        se_width_ele = ET.SubElement(size_ele, "width")
        se_width_ele.text = "640"

        se_height_ele = ET.SubElement(size_ele, "height")
        se_height_ele.text = "480"

        se_depth_ele = ET.SubElement(size_ele, "depth")
        se_depth_ele.text = "3"

        # segmented节点
        segmented_ele = ET.SubElement(annotation_ele, "segmented")
        segmented_ele.text = "0"

        li_len = len(li)
        for i in range(0, li_len):
            # object节点
            object_ele = ET.SubElement(annotation_ele, "object")

            # object节点的子节点
            obj_name_ele = ET.SubElement(object_ele, "name")
            obj_name_ele.text = "person"

            obj_pose_ele = ET.SubElement(object_ele, "pose")
            obj_pose_ele.text = "Unspecified"

            obj_truncated_ele = ET.SubElement(object_ele, "truncated")
            obj_truncated_ele.text = "0"

            obj_difficult_ele = ET.SubElement(object_ele, "difficult")
            obj_difficult_ele.text = "0"

            # object节点的bndbox子节点
            obj_bndbox_ele = ET.SubElement(object_ele, "bndbox")

            # object节点的bndbox节点的子节点
            obj_bndbox_xmin_ele = ET.SubElement(obj_bndbox_ele, "xmin")
            obj_bndbox_xmin_ele.text = str(li[i][0])

            obj_bndbox_ymin_ele = ET.SubElement(obj_bndbox_ele, "ymin")
            obj_bndbox_ymin_ele.text = str(li[i][1])

            obj_bndbox_xmax_ele = ET.SubElement(obj_bndbox_ele, "xmax")
            obj_bndbox_xmax_ele.text = str(li[i][2])

            obj_bndbox_ymax_ele = ET.SubElement(obj_bndbox_ele, "ymax")
            obj_bndbox_ymax_ele.text = str(li[i][3])

        # 创建elementtree对象，写文件
        prettyXml(annotation_ele, '\t', '\n')
        tree = ET.ElementTree(annotation_ele)
        tree.write(savepath + filename + '.xml')

datadir = '/path/to/yolo/obj/'              #YOLO 训练集路径（包含图片和标签txt）
saveimgdir = '/path/to/faster_rcnn/datasets/Caltech/Caltech/JPEGImages/'
savexmldir = '/path/to/faster_rcnn/datasets/Caltech/Caltech/Annotations/'


if __name__=='__main__':
    count = 0
    file_size_count = 0
    line_num_count = 0
    for parent, dirnames, filenames in os.walk(datadir):
        for filename in filenames:
            # print (parent+filename)
            allname = parent+filename
            extrasuf = allname.split('.')[-1]
            # print (extrasuf)
            if extrasuf == 'txt':
                txtpath = allname
                img_path = allname[0:-4]+'.jpg'
                txtname = allname.split('/')[-1]          #得到txt文件名
                xmlname = txtname.split('.')[0]           #取文件名（不包含后缀）
                xml_jpgname = xmlname+'.jpg'
                xml_savename = xmlname+'.xml'
                # newtxtname = savetxtdir+txtname          #新文件保存位置
                if os.path.getsize(txtpath) != 0:
                    alli = []  # 保存所有的人体框
                    with open(txtpath, 'r')as f:
                        lines = f.readlines()
                        # linenum = len(lines)  # 得到行数
                        # if linenum == 0:
                        #     line_num_count += 1
                        #     continue
                        # else:
                        for li in lines:
                            spline = li.split('\n')[0]
                            eachline = spline.split(' ')
                            calssnum = eachline[0].strip()
                            first_num = float(eachline[1].strip())
                            second_num = float(eachline[2].strip())
							
							#Caltech解析得到的图片大小为640*480
							
                            w = float(eachline[3].strip()) * 640
                            h = float(eachline[4].strip()) * 480

                            x_left_top = int(first_num * 640 - w / 2.0)  # 左上角
                            y_left_top = int(second_num * 480 - h / 2.0)
                            x_right_bot = int(first_num * 640 + w / 2.0)  # 右下角
                            y_right_bot = int(second_num * 480 + h / 2.0)

                            if x_left_top >= 0 and y_left_top >= 0 and x_right_bot <= 640 and y_right_bot <= 480:
                                eachli = []
                                eachli.append(x_left_top)
                                eachli.append(y_left_top)
                                eachli.append(x_right_bot)
                                eachli.append(y_right_bot)
                                alli.append(eachli)
                    f.close()
                    if alli is not None:
                        shutil.copyfile(img_path, saveimgdir + xml_jpgname)  # 拷贝图片
                        count += 1
                        CreateXml(savexmldir, xmlname, alli, True)
print ("Done!")
print ("Count is: "+str(count))
print ("File size count is: "+str(file_size_count))
print ("Line num count is: "+str(line_num_count))