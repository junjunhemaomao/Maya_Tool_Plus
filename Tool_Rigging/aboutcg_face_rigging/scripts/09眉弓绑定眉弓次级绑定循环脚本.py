# -*- coding: utf-8 -*-

#注意需要将Lib/CPDGLib/Matrix.py中的代码复制过来先执行
main_con_grp = pm.PyNode("eyebr_con_grp")#放控制器的组
main_skin_joint_grp = pm.PyNode("eyebr_skin_joint_grp")#放蒙皮关节的组
con_mode = pm.PyNode("con_mode")#控制器的模板
sel = pm.selected(type = "joint")#选择关节执行
for i in sel:
    pos_joint_name = i.name().replace("|", "_")
    con = pm.duplicate(con_mode)[0]
    pm.select(cl = True)
    grp = pm.group(n = "con_grp" + pos_joint_name)
    pm.rename(con, "con" + pos_joint_name)
    loc = pm.spaceLocator(n = "loc" + pos_joint_name)
    pm.select(cl = True)
    jin = pm.joint(n = "joint" + pos_joint_name)
    pm.parent(con, grp)
    pm.parent(grp, main_con_grp)
    pm.parent(loc, main_con_grp)
    pm.parent(jin, main_skin_joint_grp)
    ma_con = constraint(n = pos_joint_name)
    ma_con.complete(con, loc)
    loc.t >> jin.t
    loc.r >> jin.r
    loc.s >> jin.s
    loc.sh >> jin.sh
    pm.delete(pm.pointConstraint(i, grp))
