class conllision:
    def __init__(self,**NAME):
        N = ''
        if 'n' in NAME:
            N = NAME['n']
        if 'name' in NAME:
            N = NAME['name']
        
        
        
        self.__up_to_lowe_multMatrix=pm.createNode('multMatrix',n='up_to_lowe_multMatrix'+N)
        self.__conllision_blendColors=pm.createNode('blendColors',n='conllision_blendColors'+N)
        self.__lowe_to_up_multMatrix=pm.createNode('multMatrix',n='lowe_to_up_multMatrix'+N)
        self.__up_to_lowe_decomposeMatrix=pm.createNode('decomposeMatrix',n='up_to_lowe_decomposeMatrix'+N)
        self.__lowe_to_up_decomposeMatrix=pm.createNode('decomposeMatrix',n='lowe_to_up_decomposeMatrix'+N)
        self.__is_conllision_multiplyDivide=pm.createNode('multiplyDivide',n='is_conllision_multiplyDivide'+N)
        
        
        pm.setAttr(self.__up_to_lowe_multMatrix+'.caching',False)
        pm.setAttr(self.__up_to_lowe_multMatrix+'.frozen',False)
        pm.setAttr(self.__up_to_lowe_multMatrix+'.nodeState',0)
        pm.setAttr(self.__conllision_blendColors+'.caching',False)
        pm.setAttr(self.__conllision_blendColors+'.frozen',False)
        pm.setAttr(self.__conllision_blendColors+'.nodeState',0)
        pm.setAttr(self.__conllision_blendColors+'.color1G',0.0)
        pm.setAttr(self.__conllision_blendColors+'.color1B',0.0)
        pm.setAttr(self.__conllision_blendColors+'.color2R',0.0)
        pm.setAttr(self.__conllision_blendColors+'.color2B',1.0)
        pm.setAttr(self.__conllision_blendColors+'.renderPassMode',1)
        pm.setAttr(self.__conllision_blendColors+'.outputR',0.0)
        pm.setAttr(self.__conllision_blendColors+'.outputG',0.0)
        pm.setAttr(self.__conllision_blendColors+'.outputB',1.0)
        pm.setAttr(self.__conllision_blendColors+'.aiBlender',0.5)
        pm.setAttr(self.__conllision_blendColors+'.aiColor1R',1.0)
        pm.setAttr(self.__conllision_blendColors+'.aiColor1G',0.0)
        pm.setAttr(self.__conllision_blendColors+'.aiColor1B',0.0)
        pm.setAttr(self.__conllision_blendColors+'.aiColor2R',0.0)
        pm.setAttr(self.__conllision_blendColors+'.aiColor2G',0.0)
        pm.setAttr(self.__conllision_blendColors+'.aiColor2B',1.0)
        pm.setAttr(self.__lowe_to_up_multMatrix+'.caching',False)
        pm.setAttr(self.__lowe_to_up_multMatrix+'.frozen',False)
        pm.setAttr(self.__lowe_to_up_multMatrix+'.nodeState',0)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.caching',False)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.frozen',False)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.nodeState',0)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.inputRotateOrder',0)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.outputTranslateX',1.06581410364e-14)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.outputTranslateY',0.0)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.outputTranslateZ',1.06581410364e-14)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.outputRotateX',-2.2860236773e-15)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.outputRotateY',-0.0)
        pm.setAttr(self.__up_to_lowe_decomposeMatrix+'.outputRotateZ',7.95138670366e-16)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.caching',False)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.frozen',False)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.nodeState',0)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.inputRotateOrder',0)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.outputTranslateX',3.5527136788e-15)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.outputTranslateY',0.0)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.outputTranslateZ',-7.1054273576e-15)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.outputRotateX',-2.2860236773e-15)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.outputRotateY',-0.0)
        pm.setAttr(self.__lowe_to_up_decomposeMatrix+'.outputRotateZ',7.95138670366e-16)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.caching',False)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.frozen',False)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.nodeState',0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.operation',1)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.input1Z',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.input2Z',1.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.outputX',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.outputY',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.outputZ',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiInput1X',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiInput1Y',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiInput1Z',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiInput2X',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiInput2Y',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiInput2Z',0.0)
        pm.setAttr(self.__is_conllision_multiplyDivide+'.aiOperation',0)
        
        pm.connectAttr(self.__lowe_to_up_decomposeMatrix+'.outputTranslateY',self.__conllision_blendColors+'.color1R',f=True)
        pm.connectAttr(self.__up_to_lowe_decomposeMatrix+'.outputTranslateY',self.__conllision_blendColors+'.color2G',f=True)
        pm.connectAttr(self.__up_to_lowe_multMatrix+'.matrixSum',self.__up_to_lowe_decomposeMatrix+'.inputMatrix',f=True)
        pm.connectAttr(self.__lowe_to_up_multMatrix+'.matrixSum',self.__lowe_to_up_decomposeMatrix+'.inputMatrix',f=True)
        pm.connectAttr(self.__conllision_blendColors+'.outputR',self.__is_conllision_multiplyDivide+'.input1X',f=True)
        pm.connectAttr(self.__conllision_blendColors+'.outputG',self.__is_conllision_multiplyDivide+'.input1Y',f=True)
        
        
        pm.refresh()
        
    def delete(self):
        pm.delete(self.__up_to_lowe_multMatrix)
        pm.delete(self.__conllision_blendColors)
        pm.delete(self.__lowe_to_up_multMatrix)
        pm.delete(self.__up_to_lowe_decomposeMatrix)
        pm.delete(self.__lowe_to_up_decomposeMatrix)
        pm.delete(self.__is_conllision_multiplyDivide)
    def in_obj(self,con_curve_up_l_con_loc_2_con,con_curve_lowe_l_con_loc_2_con):
        pm.connectAttr(con_curve_lowe_l_con_loc_2_con+'.worldMatrix[0]',self.__lowe_to_up_multMatrix+'.matrixIn[0]',f=True)
        pm.connectAttr(con_curve_up_l_con_loc_2_con+'.worldMatrix[0]',self.__up_to_lowe_multMatrix+'.matrixIn[0]',f=True)
    def out_obj(self,con_curve_up_l_con_loc_2_con_collision_loc,con_curve_lowe_l_con_loc_2_con_collision_loc):
        pm.connectAttr(con_curve_up_l_con_loc_2_con_collision_loc+'.parentInverseMatrix[0]',self.__lowe_to_up_multMatrix+'.matrixIn[1]',f=True)
        pm.connectAttr(con_curve_lowe_l_con_loc_2_con_collision_loc+'.parentInverseMatrix[0]',self.__up_to_lowe_multMatrix+'.matrixIn[1]',f=True)
        pm.connectAttr(self.__is_conllision_multiplyDivide+'.outputX',con_curve_up_l_con_loc_2_con_collision_loc+'.translateY',f=True)
        pm.connectAttr(self.__is_conllision_multiplyDivide+'.outputY',con_curve_lowe_l_con_loc_2_con_collision_loc+'.translateY',f=True)
    def conllision_node(self,conllision_multiplyDivide):
        pm.connectAttr(conllision_multiplyDivide+'.outputY',self.__conllision_blendColors+'.blender',f=True)
        pm.connectAttr(conllision_multiplyDivide+'.outputX',self.__is_conllision_multiplyDivide+'.input2X',f=True)
        pm.connectAttr(conllision_multiplyDivide+'.outputX',self.__is_conllision_multiplyDivide+'.input2Y',f=True)

loc_up,loc_lowe = pm.selected()
con_a = loc_up.getParent()
con_b = loc_lowe.getParent()


conllision_cls = conllision()

conllision_cls.in_obj(con_a, con_b)
conllision_cls.out_obj(loc_up, loc_lowe)
conllision_cls.conllision_node(pm.PyNode("conllision_multiplyDivide_r"))
pm.transformLimits(loc_up, ty = (0, 1), ety = (1, 0))
pm.transformLimits(loc_lowe, ty = (-1, 0), ety = (0, 1))