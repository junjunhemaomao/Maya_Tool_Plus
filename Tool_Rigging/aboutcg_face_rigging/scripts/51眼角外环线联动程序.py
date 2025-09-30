# 眼皮联动程序
import pymel.core as pm

if not "size" in globals():
    size = 0

con_obj,obj = pm.selected()
con = con_obj.getParent()
obj_grp = obj.getParent()

loc = pm.spaceLocator(n = obj.name() + "_con_switch_loc")
pm.delete(pm.parentConstraint(con_obj, loc))

parentcon_node = pm.parentConstraint(con_obj, obj_grp, mo = True)
pm.parentConstraint(loc, obj_grp, mo = True)
pm.parent(loc, obj_grp.getParent())

if not "con_switch" in pm.listAttr(obj):
    pm.addAttr(obj, ln = "con_switch", at = "double", min = 0, max = 1, dv = 0.5)
    pm.setAttr(obj.con_switch,keyable = True)
if size == 0:
    reverse_node = pm.createNode("reverse", n = obj.name() + "_reverse")
if size == 0:
    obj.con_switch >> reverse_node.ix
    obj.con_switch >> parentcon_node.target[0].targetWeight
    reverse_node.ox >> parentcon_node.target[1].targetWeight
elif size == 1:
    obj.con_switch >> reverse_node.iy
    obj.con_switch >> parentcon_node.target[0].targetWeight
    reverse_node.oy >> parentcon_node.target[1].targetWeight
elif size == 2:
    obj.con_switch >> reverse_node.iz

    obj.con_switch >> parentcon_node.target[0].targetWeight
    reverse_node.oz >> parentcon_node.target[1].targetWeight
size = (size + 1)%3
# con_Outer_ring_l_up_con_loc_3_con.con_switch con_Outer_ring_l_up_con_loc_3_con_grp_parentConstraint1.target[0].targetWeight;
# 眼角联动程序
import pymel.core as pm

if not "size" in globals():
    size = 0

con_obj,obj = pm.selected()
con = con_obj.getParent()
con = con_obj
obj_grp = obj.getParent()

loc = pm.spaceLocator(n = obj.name() + "_con_switch_loc")
pm.delete(pm.parentConstraint(con_obj, loc))

parentcon_node = pm.parentConstraint(con_obj, obj_grp, mo = True)
pm.parentConstraint(loc, obj_grp, mo = True)
pm.parent(loc, obj_grp.getParent())

if not "con_switch" in pm.listAttr(obj):
    pm.addAttr(obj, ln = "con_switch", at = "double", min = 0, max = 1, dv = 0.5)
    pm.setAttr(obj.con_switch,keyable = True)
if size == 0:
    reverse_node = pm.createNode("reverse", n = obj.name() + "_reverse")
if size == 0:
    obj.con_switch >> reverse_node.ix
    obj.con_switch >> parentcon_node.target[0].targetWeight
    reverse_node.ox >> parentcon_node.target[1].targetWeight
elif size == 1:
    obj.con_switch >> reverse_node.iy
    obj.con_switch >> parentcon_node.target[0].targetWeight
    reverse_node.oy >> parentcon_node.target[1].targetWeight
elif size == 2:
    obj.con_switch >> reverse_node.iz

    obj.con_switch >> parentcon_node.target[0].targetWeight
    reverse_node.oz >> parentcon_node.target[1].targetWeight
size = (size + 1)%3
# con_Outer_ring_l_up_con_loc_3_con.con_switch con_Outer_ring_l_up_con_loc_3_con_grp_parentConstraint1.target[0].targetWeight;