import maya.cmds as cmds

def get_org():
    orglist = cmds.ls(selection=True)
    orgobjname = orglist[0]
    orgbuffer = orgobjname.split("|")
    org_arraysize = len(orgbuffer)
    if org_arraysize > 1:
        return orgbuffer[1]
    else:
        return orgbuffer[0]

def create_window(title, width, height):
    if cmds.window(title, exists=True):
        cmds.deleteUI(title)
    cmds.window(title, width=width, height=height)

def create_frame_layout(label, collapsable=False):
    cmds.frameLayout(label=label, collapsable=collapsable)

def create_text_field_button_grp(label, text, button_label, command):
    cmds.textFieldButtonGrp(label=label, text=text, buttonLabel=button_label, buttonCommand=command)

def create_separator():
    cmds.separator(style="none")

def create_button(label, command):
    cmds.button(label=label, command=command)

def create_row_column_layout(number_of_columns, column_widths):
    cmds.rowColumnLayout(numberOfColumns=number_of_columns, columnWidth=column_widths)

def set_parent_levels(levels):
    for _ in range(levels):
        cmds.setParent("..")

def show_window(title, width):
    cmds.showWindow(title)
    cmds.window(title, edit=True, width=width)

def main():
    create_window("curve tool box v01", 300, 50)
    create_frame_layout("tools for curs")
    create_row_column_layout(1, [(1, 300), (2, 300), (3, 300)])
    create_button("create locators based on the curve", "locatorsOnCur()")
    create_button("create joints based on the curve", "jointsOnCur()")
    create_button("create splineIk based on the curve", "spIKCur()")
    create_separator()
    set_parent_levels(2)
    show_window("curve tool box v01", 250)

if __name__ == "__main__":
    main()
