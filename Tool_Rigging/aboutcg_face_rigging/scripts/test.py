import pymel.core as pm
class zipper_class:
    def __init__(self,**NAME):
        N = ''
        if 'n' in NAME:
            N = NAME['n']
        if 'name' in NAME:
            N = NAME['name']
        
        
        
        self.__zipper_clamp=pm.createNode('clamp',n='zipper_clamp'+N)
        self.__zipper_range=pm.createNode('setRange',n='zipper_range'+N)
        self.__zipper_add=pm.createNode('plusMinusAverage',n='zipper_add'+N)
        self.__zipper_lowe_switch_blendColors=pm.createNode('blendColors',n='zipper_lowe_switch_blendColors'+N)
        self.__zipper_up_switch_blendColors=pm.createNode('blendColors',n='zipper_up_switch_blendColors'+N)
        self.__get_zipper_pos_blendColors=pm.createNode('blendColors',n='get_zipper_pos_blendColors'+N)
        
        
        pm.setAttr(self.__zipper_clamp+'.caching',False)
        pm.setAttr(self.__zipper_clamp+'.frozen',False)
        pm.setAttr(self.__zipper_clamp+'.nodeState',0)
        pm.setAttr(self.__zipper_clamp+'.minR',0.0)
        pm.setAttr(self.__zipper_clamp+'.minG',0.0)
        pm.setAttr(self.__zipper_clamp+'.minB',0.0)
        pm.setAttr(self.__zipper_clamp+'.maxR',1.0)
        pm.setAttr(self.__zipper_clamp+'.maxG',0.0)
        pm.setAttr(self.__zipper_clamp+'.maxB',0.0)
        pm.setAttr(self.__zipper_clamp+'.inputG',0.0)
        pm.setAttr(self.__zipper_clamp+'.inputB',0.0)
        pm.setAttr(self.__zipper_clamp+'.renderPassMode',1)
        pm.setAttr(self.__zipper_clamp+'.outputR',0.0)
        pm.setAttr(self.__zipper_clamp+'.outputG',0.0)
        pm.setAttr(self.__zipper_clamp+'.outputB',0.0)
        pm.setAttr(self.__zipper_clamp+'.aiMinR',0.0)
        pm.setAttr(self.__zipper_clamp+'.aiMinG',0.0)
        pm.setAttr(self.__zipper_clamp+'.aiMinB',0.0)
        pm.setAttr(self.__zipper_clamp+'.aiMaxR',1.0)
        pm.setAttr(self.__zipper_clamp+'.aiMaxG',1.0)
        pm.setAttr(self.__zipper_clamp+'.aiMaxB',1.0)
        pm.setAttr(self.__zipper_clamp+'.aiInputR',0.0)
        pm.setAttr(self.__zipper_clamp+'.aiInputG',0.0)
        pm.setAttr(self.__zipper_clamp+'.aiInputB',0.0)
        pm.setAttr(self.__zipper_range+'.caching',False)
        pm.setAttr(self.__zipper_range+'.frozen',False)
        pm.setAttr(self.__zipper_range+'.nodeState',0)
        pm.setAttr(self.__zipper_range+'.valueZ',0.0)
        pm.setAttr(self.__zipper_range+'.minX',0.0)
        pm.setAttr(self.__zipper_range+'.minY',0.0)
        pm.setAttr(self.__zipper_range+'.minZ',0.0)
        pm.setAttr(self.__zipper_range+'.maxX',1.0)
        pm.setAttr(self.__zipper_range+'.maxY',1.0)
        pm.setAttr(self.__zipper_range+'.maxZ',0.0)
        pm.setAttr(self.__zipper_range+'.oldMinX',0.0)
        pm.setAttr(self.__zipper_range+'.oldMinY',8.0)
        pm.setAttr(self.__zipper_range+'.oldMinZ',0.0)
        pm.setAttr(self.__zipper_range+'.oldMaxX',2.0)
        pm.setAttr(self.__zipper_range+'.oldMaxY',10.0)
        pm.setAttr(self.__zipper_range+'.oldMaxZ',0.0)
        pm.setAttr(self.__zipper_range+'.outValueX',0.0)
        pm.setAttr(self.__zipper_range+'.outValueY',0.0)
        pm.setAttr(self.__zipper_range+'.outValueZ',0.0)
        pm.setAttr(self.__zipper_range+'.aiValueX',0.0)
        pm.setAttr(self.__zipper_range+'.aiValueY',0.0)
        pm.setAttr(self.__zipper_range+'.aiValueZ',0.0)
        pm.setAttr(self.__zipper_range+'.aiMinX',0.0)
        pm.setAttr(self.__zipper_range+'.aiMinY',0.0)
        pm.setAttr(self.__zipper_range+'.aiMinZ',0.0)
        pm.setAttr(self.__zipper_range+'.aiMaxX',0.0)
        pm.setAttr(self.__zipper_range+'.aiMaxY',0.0)
        pm.setAttr(self.__zipper_range+'.aiMaxZ',0.0)
        pm.setAttr(self.__zipper_range+'.aiOldMinX',0.0)
        pm.setAttr(self.__zipper_range+'.aiOldMinY',0.0)
        pm.setAttr(self.__zipper_range+'.aiOldMinZ',0.0)
        pm.setAttr(self.__zipper_range+'.aiOldMaxX',0.0)
        pm.setAttr(self.__zipper_range+'.aiOldMaxY',0.0)
        pm.setAttr(self.__zipper_range+'.aiOldMaxZ',0.0)
        pm.setAttr(self.__zipper_add+'.caching',False)
        pm.setAttr(self.__zipper_add+'.frozen',False)
        pm.setAttr(self.__zipper_add+'.nodeState',0)
        pm.setAttr(self.__zipper_add+'.operation',1)
        pm.setAttr(self.__zipper_add+'.output1D',0.0)
        pm.setAttr(self.__zipper_add+'.output2Dx',0.0)
        pm.setAttr(self.__zipper_add+'.output2Dy',0.0)
        pm.setAttr(self.__zipper_add+'.output3Dx',0.0)
        pm.setAttr(self.__zipper_add+'.output3Dy',0.0)
        pm.setAttr(self.__zipper_add+'.output3Dz',0.0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.caching',False)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.frozen',False)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.nodeState',0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.renderPassMode',1)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.outputR',11.2006883621)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.outputG',66.2106628418)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.outputB',26.2694263458)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiBlender',0.5)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiColor1R',1.0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiColor1G',0.0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiColor1B',0.0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiColor2R',0.0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiColor2G',0.0)
        pm.setAttr(self.__zipper_lowe_switch_blendColors+'.aiColor2B',1.0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.caching',False)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.frozen',False)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.nodeState',0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.renderPassMode',1)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.outputR',10.5958747864)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.outputG',69.2312850952)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.outputB',26.6159534454)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiBlender',0.5)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiColor1R',1.0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiColor1G',0.0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiColor1B',0.0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiColor2R',0.0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiColor2G',0.0)
        pm.setAttr(self.__zipper_up_switch_blendColors+'.aiColor2B',1.0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.caching',False)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.frozen',False)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.nodeState',0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.blender',0.5)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.renderPassMode',1)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.outputR',10.8982810974)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.outputG',67.7209777832)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.outputB',26.4426898956)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiBlender',0.5)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiColor1R',1.0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiColor1G',0.0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiColor1B',0.0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiColor2R',0.0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiColor2G',0.0)
        pm.setAttr(self.__get_zipper_pos_blendColors+'.aiColor2B',1.0)
        
        pm.connectAttr(self.__zipper_add+'.output1D',self.__zipper_clamp+'.inputR',f=True)
        pm.connectAttr(self.__zipper_range+'.outValueX',self.__zipper_add+'.input1D[1]',f=True)
        pm.connectAttr(self.__zipper_range+'.outValueY',self.__zipper_add+'.input1D[2]',f=True)
        pm.connectAttr(self.__zipper_clamp+'.outputR',self.__zipper_lowe_switch_blendColors+'.blender',f=True)
        pm.connectAttr(self.__get_zipper_pos_blendColors+'.output',self.__zipper_lowe_switch_blendColors+'.color1',f=True)
        pm.connectAttr(self.__zipper_lowe_switch_blendColors+'.blender',self.__zipper_up_switch_blendColors+'.blender',f=True)
        pm.connectAttr(self.__get_zipper_pos_blendColors+'.output',self.__zipper_up_switch_blendColors+'.color1',f=True)
        
        self.zipper_range = self.__zipper_range
        
        pm.refresh()
        
    def delete(self):
        pm.delete(self.__zipper_clamp)
        pm.delete(self.__zipper_range)
        pm.delete(self.__zipper_add)
        pm.delete(self.__zipper_lowe_switch_blendColors)
        pm.delete(self.__zipper_up_switch_blendColors)
        pm.delete(self.__get_zipper_pos_blendColors)
    def in_obj(self,con_curve_up_l_con_loc_1,con_curve_lowe_l_con_loc_1):
        pm.connectAttr(con_curve_up_l_con_loc_1+'.translate',self.__get_zipper_pos_blendColors+'.color1',f=True)
        pm.connectAttr(con_curve_lowe_l_con_loc_1+'.translate',self.__get_zipper_pos_blendColors+'.color2',f=True)
        pm.connectAttr(con_curve_up_l_con_loc_1+'.translate',self.__zipper_up_switch_blendColors+'.color2',f=True)
        pm.connectAttr(con_curve_lowe_l_con_loc_1+'.translate',self.__zipper_lowe_switch_blendColors+'.color2',f=True)
    def con_obj(self,main_con,main_con_switch_multiplyDivide):
        pm.connectAttr(main_con_switch_multiplyDivide+'.outputY',self.__zipper_add+'.input1D[0]',f=True)
        pm.connectAttr(main_con+'.zipper_inside',self.__zipper_range+'.valueX',f=True)
        pm.connectAttr(main_con+'.zipper_outside',self.__zipper_range+'.valueY',f=True)
    def out_curve(self,con_curve_up_lShape,con_curve_lowe_lShape,index):
        pm.connectAttr(self.__zipper_up_switch_blendColors+'.output',con_curve_up_lShape+'.controlPoints[' + str(index) + ']',f=True)
        pm.connectAttr(self.__zipper_lowe_switch_blendColors+'.output',con_curve_lowe_lShape+'.controlPoints[' + str(index) + ']',f=True)
up_curve, lowe_curve = pm.selected()#选择上下曲线
main_con = pm.PyNode("main_r_con")#总控制器 需要zipper_inside、zipper_outside、closure属性
close_obj = pm.PyNode("main_r_conx_switch_multiplyDivide_")#需要一个0-1的outputY属性


up_curve_shape = up_curve.getShape()
lowe_curve_shape = lowe_curve.getShape()
attr_size = 6#控制点属性的数量

# translate
up_point_attr = up_curve_shape.controlPoints
lowe_point_attr = lowe_curve_shape.controlPoints
attr_ids = range(1,6)

for i in attr_ids:
    up_con_obj = pm.listConnections(up_point_attr[i], c=True)[0][1]
    lowe_con_obj = pm.listConnections(lowe_point_attr[i], c=True)[0][1]
    pm.disconnectAttr(up_con_obj.t, up_point_attr[i])
    pm.disconnectAttr(lowe_con_obj.t, lowe_point_attr[i])

    zipper_obj = zipper_class(n=str(i))
    zipper_obj.in_obj(up_con_obj, lowe_con_obj)
    zipper_obj.con_obj(main_con, close_obj)
    zipper_obj.out_curve(up_curve_shape, lowe_curve_shape, i)
    