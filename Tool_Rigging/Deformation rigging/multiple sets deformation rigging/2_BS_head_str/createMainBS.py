# -*- coding: utf-8 -*-

#####step6######

"""
应用于批量生成blendshape，一次选中需创建BS的物体，确保代码中的前缀（BS_main）和生成blendshape的物体前缀一致，
如（需要给face_01_geo创建BS，则对应的物体的名称应为BS_main_face_01_geo）。也可以修改代码中的前缀名称来匹配模型名称。
"""

string $born[]=`ls -sl`;
for($i=0;$i<size($born);$i++){
select -r ("BS_main_"+$born[$i]) ;
select -add $born[$i] ;
blendShape -n ($born[$i]+"_main_BS") -frontOfChain -exclusive "deformPartition#";
 setAttr (($born[$i]+"_main_BS")+"."+("BS_main_"+$born[$i])) 1;
}