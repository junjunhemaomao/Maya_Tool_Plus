import pymel.core as pm

d_node = pm.ls(dn = True)

delete_objs = list()
no_delte_objs = list()


objs = pm.ls(type = "locator")
for i in objs:
    outs = [i for i in i.outputs() if not i in d_node]
    if len(outs) <= 0:
        delete_objs.append(i)
    else:
        no_delte_objs.append(i)
pm.delete(delete_objs)
pm.select(no_delte_objs)