import maya.cmds as cmds
import re
import os

def rename_meshes_to_filename(*args):
    # 获取输入框中的文件夹路径
    fbx_directory = cmds.textField("fbxDirectory", q=True, text=True)

    # 记录导入前的顶层Transform节点数量
    initial_transforms = cmds.ls(type="transform")

    # 遍历指定目录及其子目录中的所有FBX文件
    for root, dirs, files in os.walk(fbx_directory):
        fbx_files = [f for f in files if f.endswith('.fbx')]

        for fbx_file in fbx_files:
            # 构建FBX文件的完整路径
            fbx_path = os.path.join(root, fbx_file)

            # 导入FBX文件到Maya场景中
            cmds.file(fbx_path, i=True)

            # 获取导入后新增加的顶层Transform节点
            new_transforms = set(cmds.ls(type="transform")) - set(initial_transforms)

            # 使用FBX文件名作为顶层Transform节点的名称
            new_name = os.path.splitext(fbx_file)[0]

            for transform in new_transforms:
                # 只重命名顶层Transform节点
                if not cmds.listRelatives(transform, parent=True):
                    cmds.rename(transform, new_name)

            # 更新导入前的顶层Transform节点数量
            initial_transforms = cmds.ls(type="transform")

    print('well done!')

def update_texture_paths(*args):
    # 获取输入框中的新基础路径
    new_base_path = cmds.textField("textureDirectory", query=True, text=True)

    # 获取所有文件节点
    file_nodes = cmds.ls(type="file")

    for node in file_nodes:
        # 获取当前文件路径
        current_file_path = cmds.getAttr("{}.fileTextureName".format(node))

        # 获取当前文件名
        file_name = os.path.basename(current_file_path)

        # 构建新的文件路径
        new_file_path = os.path.join(new_base_path, file_name).replace('\\', '/')

        # 设置新的文件路径
        cmds.setAttr("{}.fileTextureName".format(node), new_file_path, type="string")

        # 打印更新信息
        print("Updated {} to {}".format(current_file_path, new_file_path))

def convert_to_png():
    # 获取当前的 Transparency Algorithm 设置
    current_transparency_algorithm = cmds.getAttr("hardwareRenderingGlobals.transparencyAlgorithm")
    # 如果当前设置不是 Alpha Cut，将其更改为 Alpha Cut
    if current_transparency_algorithm != 5:  # 5 对应于 Alpha Cut
        cmds.setAttr("hardwareRenderingGlobals.transparencyAlgorithm", 5)

    # 选择的物体的形状节点
    shapes = cmds.ls(sl=True, o=True, dag=True, s=True)
    for shape in shapes:
        shadingEngines = cmds.listConnections(shape, type="shadingEngine")
        if shadingEngines:
            for shadingEngine in shadingEngines:
                materials = cmds.ls(cmds.listConnections(shadingEngine), materials=True)

                for material in materials:
                    print("Material:", material)

                    # 获取该材质的所有贴图通道
                    texture_channels = cmds.listConnections(material, type="file")

                    if texture_channels:
                        for texture_channel in texture_channels:
                            image_name = cmds.getAttr(texture_channel + ".fileTextureName")
                            print(f"Texture File for {texture_channel}: {image_name}")

                            # 将贴图的格式改为 PNG
                            new_image_name = os.path.splitext(image_name)[0] + ".png"
                            print(f"Changing texture format to .png: {new_image_name}")
                            cmds.setAttr(texture_channel + ".fileTextureName", new_image_name, type="string")

                    # 处理反射度
                    if cmds.attributeQuery("reflectivity", node=material, exists=True):
                        reflectivity_texture = cmds.listConnections(material + ".reflectivity", type="file")
                        if not reflectivity_texture:
                            cmds.setAttr(material + ".reflectivity", 0)
                    # 处理漫反射
                    if cmds.attributeQuery("diffuse", node=material, exists=True):
                        reflectivity_texture = cmds.listConnections(material + ".diffuse", type="file")
                        if not reflectivity_texture:
                            cmds.setAttr(material + ".diffuse", 1)
                    # 处理高光
                    if cmds.attributeQuery("specularColor", node=material, exists=True):
                        incandescence_texture = cmds.listConnections(material + ".specularColor", type="file")
                        if not incandescence_texture:
                            cmds.setAttr(material + ".specularColor",  0, 0, 0, type="double3")
                    # 处理 incandescence
                    if cmds.attributeQuery("incandescence", node=material, exists=True):
                        incandescence_texture = cmds.listConnections(material + ".incandescence", type="file")
                        if not incandescence_texture:
                            cmds.setAttr(material + ".incandescence",  0, 0, 0, type="double3")
                    # 有的材质有ambientColor，会导致渲染发黑
                    if cmds.attributeQuery("ambientColor", node=material, exists=True):
                        reflectivity_texture = cmds.listConnections(material + ".ambientColor", type="file")
                        if not reflectivity_texture:
                            cmds.setAttr(material + ".ambientColor",  1, 1, 1, type="double3")
                    # 检查材质是否有coat属性并设置其值为0
                    if cmds.attributeQuery("coat", node=material, exists=True):
                        # 如果coat属性存在但没有被设置，则将其值修改为0
                        reflectivity_texture = cmds.listConnections(material + ".coat", type="file")
                        if not reflectivity_texture:
                            cmds.setAttr(material + ".coat", 0)
                    # 检查材质是否有emission属性并设置其值为0
                    if cmds.attributeQuery("emission", node=material, exists=True):
                        emission_texture = cmds.listConnections(material + ".emission", type="file")
                        if not emission_texture:
                            cmds.setAttr(material + ".emission", 0)

                    # 处理 normalCamera 通道,有多层结构，后续可以改写
                    if cmds.attributeQuery("normalCamera", node=material, exists=True):  # 检查 normalCamera 属性是否存在
                        normal_map = cmds.listConnections(material + ".normalCamera", type="bump2d")
                        if normal_map:
                            file_node = cmds.listConnections(normal_map[0] + ".bumpValue", type="file")
                            if file_node:
                                image_name = cmds.getAttr(file_node[0] + ".fileTextureName")
                                print(f"Texture File for normalCamera channel: {image_name}")

                                # 检查是否是法线贴图，即文件名包含 '_n' 且以 .png 结尾
                                if "_n" in os.path.splitext(image_name)[0]:
                                    # 将贴图的格式改为 PNG
                                    new_image_name = os.path.splitext(image_name)[0] + ".png"
                                    print(f"Changing normalCamera texture format to .png: {new_image_name}")
                                    cmds.setAttr(file_node[0] + ".fileTextureName", new_image_name, type="string")
                                else:
                                    print(f"Skipping texture: {image_name} (not a normal map)")

def clean_nonexistent_textures():
    # 获取所有的file节点
    file_nodes = cmds.ls(type='file')

    for file_node in file_nodes:
        # 获取文件纹理的路径
        file_path = cmds.getAttr(file_node + '.fileTextureName')

        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"Texture file {file_path} doesn't exist, deleting node {file_node}")

            # 获取所有输出连接
            connections = cmds.listConnections(file_node, plugs=True, connections=True, destination=True)

            if connections:
                # 断开所有存在的连接
                for i in range(0, len(connections), 2):
                    source_attr = connections[i + 1]
                    dest_attr = connections[i]
                    # 检查连接是否存在
                    if cmds.isConnected(source_attr, dest_attr):
                        try:
                            cmds.disconnectAttr(source_attr, dest_attr)
                        except RuntimeError as e:
                            print(f"Failed to disconnect {source_attr} from {dest_attr}: {e}")

            # 删除file节点
            try:
                cmds.delete(file_node)
            except RuntimeError as e:
                print(f"Failed to delete node {file_node}: {e}")

def disconnect_all_transparency_textures():
    def disconnect_transparency_texture(material):
        # 检查透明度通道是否存在
        if cmds.attributeQuery("transparency", node=material, exists=True):
            # 获取透明度通道的贴图连接
            transparency_texture = cmds.listConnections(material + ".transparency", type="file")

            # 断开透明度通道的贴图连接
            if transparency_texture:
                for texture_node in transparency_texture:
                    if cmds.isConnected(texture_node + ".outTransparency", material + ".transparency"):
                        cmds.disconnectAttr(texture_node + ".outTransparency", material + ".transparency")
                        print(f"Disconnected transparency texture: {texture_node} from material: {material}")
                    else:
                        print(
                            f"No connection found between {texture_node}.outTransparency and {material}.transparency. Skipping disconnect.")
            else:
                print(f"No transparency texture connected to material: {material}")
        else:
            print(f"No transparency channel found in material: {material}")

    # 获取场景中的所有材质
    all_materials = cmds.ls(materials=True)

    # 遍历每个材质，并断开其透明通道的贴图连接
    for material in all_materials:
        disconnect_transparency_texture(material)

def assign_alpha_texture():
    # 获取选中物体的形状节点
    shapes = cmds.ls(sl=True, o=True, dag=True, s=True)

    for shape in shapes:
        # 获取物体的 shadingEngine
        shadingEngines = cmds.listConnections(shape, type="shadingEngine")

        if shadingEngines:
            for shadingEngine in shadingEngines:
                # 获取与 shadingEngine 相关联的材质
                materials = cmds.ls(cmds.listConnections(shadingEngine), materials=True)

                for material in materials:
                    # 检查材质是否有 transparency 通道
                    if cmds.attributeQuery("transparency", node=material, exists=True):
                        # 获取透明度通道的贴图
                        transparency_texture = cmds.listConnections(material + ".transparency", type="file")

                        if not transparency_texture:
                            # 构建可能的透明贴图文件名
                            color_texture = cmds.listConnections(material + ".color", type="file")
                            if color_texture:
                                color_image_name = cmds.getAttr(color_texture[0] + ".fileTextureName")
                                alpha_image_name = os.path.splitext(color_image_name)[0] + "_alpha.png"

                                # 检查硬盘上是否存在对应的透明贴图文件
                                if os.path.exists(alpha_image_name):
                                    # 创建一个新的文件节点
                                    alpha_file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
                                    cmds.setAttr(alpha_file_node + ".fileTextureName", alpha_image_name, type="string")

                                    # 将透明贴图赋值给透明度通道
                                    cmds.connectAttr(alpha_file_node + ".outColor", material + ".transparency",
                                                     force=True)
                                    print(f"Assigned alpha texture to transparency channel for material: {material}")
                                else:
                                    print(f"No alpha texture found for material: {material}")
                            else:
                                print(f"No color texture found for material: {material}")
                    else:
                        print(f"No transparency channel found in material: {material}")

def link_normal_map():
    # 获取选择的物体的形状节点
    shapes = cmds.ls(sl=True, o=True, dag=True, s=True)

    for shape in shapes:
        shading_engines = cmds.listConnections(shape, type="shadingEngine")
        if shading_engines:
            for shading_engine in shading_engines:
                materials = cmds.ls(cmds.listConnections(shading_engine), materials=True)

                for material in materials:
                    # 检查 color 通道是否有贴图链接
                    color_texture = cmds.listConnections(material + ".color", type="file")
                    if not color_texture:
                        continue

                    # 获取 color 通道的贴图路径
                    color_file_node = color_texture[0]
                    color_image_name = cmds.getAttr(color_file_node + ".fileTextureName")

                    # 构建法线贴图的路径
                    normal_filename = color_image_name.replace("_D.", "_N.")

                    # 检查法线贴图文件是否存在
                    if not os.path.exists(normal_filename):
                        print(f"Normal map not found: {normal_filename}")
                        continue

                    # 检查并断开 existing connections to normalCamera
                    existing_connections = cmds.listConnections(material + ".normalCamera", plugs=True)
                    if existing_connections:
                        cmds.disconnectAttr(existing_connections[0], material + ".normalCamera")

                    # 创建和连接节点
                    file_node = cmds.shadingNode("file", asTexture=True, name=material + "_normalFile")
                    place2d_node = cmds.shadingNode("place2dTexture", asUtility=True, name=material + "_normalPlace2d")
                    bump2d_node = cmds.shadingNode("bump2d", asUtility=True, name=material + "_normalBump2d")

                    # 设置 bumpInterp 为 1
                    cmds.setAttr(bump2d_node + ".bumpInterp", 1)

                    # 连接 place2dTexture 节点
                    cmds.connectAttr(place2d_node + ".outUV", file_node + ".uvCoord")
                    cmds.connectAttr(place2d_node + ".outUvFilterSize", file_node + ".uvFilterSize")
                    cmds.setAttr(place2d_node + ".coverage", 1, 1, 1)

                    # 连接 file 节点
                    cmds.connectAttr(file_node + ".outAlpha", bump2d_node + ".bumpValue")

                    # 设置法线贴图的路径
                    cmds.setAttr(file_node + ".fileTextureName", normal_filename, type="string")

                    # 连接法线贴图到材质的 normalCamera 通道
                    cmds.connectAttr(bump2d_node + ".outNormal", material + ".normalCamera")

def align_pivots_to_first_selected():
    # 获取选择的物体
    selected_objects = cmds.ls(selection=True)

    if len(selected_objects) < 2:
        cmds.warning("Please select at least two objects.")
        return

    # 第一个选中的物体作为参考物体
    reference_object = selected_objects[0]

    # 获取参考物体的轴心点位置
    reference_pivot = cmds.xform(reference_object, query=True, pivots=True, worldSpace=True)[:3]

    # 将其他选中的物体移动到参考物体的轴心点位置
    for obj in selected_objects[1:]:
        # 获取当前物体的轴心点位置
        obj_pivot = cmds.xform(obj, query=True, pivots=True, worldSpace=True)[:3]

        # 计算移动向量
        move_vector = [reference_pivot[i] - obj_pivot[i] for i in range(3)]

        # 移动物体
        cmds.move(move_vector[0], move_vector[1], move_vector[2], obj, relative=True)

def rename_materials_for_selected_objects():
    # 获取所选的物体
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("未选择任何物体。请先选择要修改材质球的物体。")
        return

    for obj in selected_objects:
        # 获取物体的形状节点
        shapes = cmds.listRelatives(obj, shapes=True)

        if not shapes:
            continue

        for shape in shapes:
            # 获取物体的连接的材质球
            shading_groups = cmds.listConnections(shape, type="shadingEngine")

            if shading_groups:
                for shading_group in shading_groups:
                    # 获取着色引擎的连接材质
                    connected_materials = cmds.listConnections(shading_group + ".surfaceShader")

                    if connected_materials:
                        for material in connected_materials:
                            # 根据材质类型进行重命名
                            material_type = cmds.nodeType(material)
                            if material_type == "lambert":
                                new_material_name = obj + "_lambert"
                            elif material_type == "blinn":
                                new_material_name = obj + "_blinn"
                            elif material_type == "phong":
                                new_material_name = obj + "_phong"
                            else:
                                new_material_name = obj + "_material"

                            # 重命名材质
                            cmds.rename(material, new_material_name)
                            print(f"已将物体 {obj} 的材质球重命名为 {new_material_name}")

def rename_objects(string1, string2):
    # 获取选择的物体
    selected_objects = cmds.ls(selection=True)

    # 遍历选择的物体
    for obj in selected_objects:
        # 获取物体的名称
        old_name = cmds.ls(obj, long=True)[0]

        # 检查字符串1是否在物体名称中
        if string1 in old_name:
            # 将字符串1移到字符串2的后面
            new_name = old_name.replace(string1, "")
            new_name = new_name.replace(string2, string2 + string1)

            # 重命名物体
            cmds.rename(obj, new_name)

def delete_joints():
    # 获取场景中所有物体
    all_objects = cmds.ls(dag=True)

    # 存储要删除的骨骼（joint）类型的对象
    joints_to_delete = []

    # 遍历所有物体
    for obj in all_objects:
        # 检查物体是否为骨骼（joint）类型
        if cmds.objectType(obj) == 'joint':
            # 将骨骼对象添加到删除列表
            joints_to_delete.append(obj)

    # 删除所有骨骼
    if joints_to_delete:
        cmds.delete(joints_to_delete)
        print(f"已删除 {len(joints_to_delete)} 个骨骼对象")

def unlock_and_disconnect_selected():
    """
    解锁并断开选定模型的变换属性连接。
    """
    selected_objects = cmds.ls(selection=True, type='transform')
    if not selected_objects:
        print("未选择任何模型。")
        return

    for obj in selected_objects:
        attributes = ['translateX', 'translateY', 'translateZ',
                      'rotateX', 'rotateY', 'rotateZ',
                      'scaleX', 'scaleY', 'scaleZ']
        for attr in attributes:
            full_attr = f"{obj}.{attr}"
            if cmds.objExists(full_attr):
                try:
                    # 解锁属性
                    cmds.setAttr(full_attr, lock=False)

                    # 如果存在连接，断开连接
                    if cmds.connectionInfo(full_attr, isDestination=True):
                        source = cmds.connectionInfo(full_attr, sourceFromDestination=True)
                        cmds.disconnectAttr(source, full_attr)
                        print(f"断开连接: {source} -> {full_attr}")
                except Exception as e:
                    print(f"处理 {full_attr} 时出错: {e}")

    cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False)
    print("已完成冻结变换。")

def delete_all_layers():
    """
    删除 Maya 场景中的所有 Display 和 Render Layers。
    """
    # 删除 Display Layers
    display_layers = cmds.ls(type='displayLayer')
    for layer in display_layers:
        if layer != 'defaultLayer':  # 默认图层不能删除
            try:
                cmds.delete(layer)
                print(f"删除 Display Layer: {layer}")
            except Exception as e:
                print(f"无法删除 Display Layer {layer}: {e}")

    # 删除 Render Layers
    render_layers = cmds.ls(type='renderLayer')
    for layer in render_layers:
        if layer != 'defaultRenderLayer':  # 默认渲染图层不能删除
            try:
                cmds.delete(layer)
                print(f"删除 Render Layer: {layer}")
            except Exception as e:
                print(f"无法删除 Render Layer {layer}: {e}")

def unify_normals():
    all_meshes = cmds.ls(type='mesh', long=True)
    for mesh in all_meshes:
        print(f"Processing normals for mesh: {mesh}")

        # 获取当前 mesh 的所有面
        face_count = cmds.polyEvaluate(mesh, face=True)
        face_normals = []
        positive_group = []  # 法线与参考方向一致的面
        negative_group = []  # 法线与参考方向相反的面

        for i in range(face_count):
            # 使用 polyInfo 查询法线数据
            normal_info = cmds.polyInfo(f"{mesh}.f[{i}]", faceNormals=True)
            if normal_info:
                # 提取法线向量数据
                normal_values = normal_info[0].split()
                normal = [float(normal_values[-3]), float(normal_values[-2]), float(normal_values[-1])]
                face_normals.append(normal)

                # 使用点积区分正负组，默认参考向量为 [0, 0, 1]
                dot_product = normal[2]  # 这里用 Z 轴作为参考方向
                if dot_product >= 0:
                    positive_group.append(i)
                else:
                    negative_group.append(i)
            else:
                face_normals.append([0, 0, 0])  # 如果未能获取法线，则填充默认值

        # 判断哪个组更小并翻转
        if len(negative_group) < len(positive_group):
            for i in negative_group:
                cmds.polyNormal(f"{mesh}.f[{i}]", normalMode=2)  # 翻转负组的法线
        else:
            for i in positive_group:
                cmds.polyNormal(f"{mesh}.f[{i}]", normalMode=2)  # 翻转正组的法线

        # 统一当前 mesh 的法线方向
        cmds.polyNormal(mesh, normalMode=0)  # 设置为一致方向
        print(f"Normals unified for mesh: {mesh}")

def rename_objects_with_serialization(prefix=""):
    # 获取当前选中的物体
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        print("没有选中的物体")
        return

    # 获取用户输入的新前缀
    new_prefix = cmds.textField(prefixField, query=True, text=True)

    # 计算序列的起始数字（从1开始）
    start_index = 1

    for obj in selected_objects:
        # 构建新的命名
        new_name = f"{new_prefix}{start_index}"

        # 使用rename函数重命名物体
        cmds.rename(obj, new_name)

        print(f"已将物体重命名为：{new_name}")

        # 增加序列计数
        start_index += 1

def remove_before_colon():
    selected_objects = cmds.ls(selection=True, long=True)

    for obj in selected_objects:
        if ':' in obj:
            new_name = obj.split(':')[-1]
            cmds.rename(obj, new_name)

def remove_after_colon():
    selected_objects = cmds.ls(selection=True, long=True)

    for obj in selected_objects:
        if ':' in obj:
            new_name = obj.split(':')[0]
            cmds.rename(obj, new_name)

def replace_multiple_underscores():
    selected_objects = cmds.ls(selection=True, long=True)

    for obj in selected_objects:
        new_name = re.sub('_+', '_', obj)
        cmds.rename(obj, new_name)


def create_ui():
    if cmds.window("artAssetToolWin", exists=True):
        cmds.deleteUI("artAssetToolWin", window=True)

    # 创建主窗口，减小宽度从600到400
    main_window = cmds.window("artAssetToolWin", title="Art Asset Tool v1.0", widthHeight=(400, 700))

    # 创建选项卡布局
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    # ====== 贴图处理选项卡 ======
    texture_tab = cmds.columnLayout(adj=True)

    # 路径设置框架，宽度从590减至390
    cmds.frameLayout(label="路径设置", collapsable=True, collapse=False, width=390)
    cmds.columnLayout(adj=True, rowSpacing=3)
    cmds.text(label="FBX目录路径:")
    cmds.textField("fbxDirectory")
    cmds.button(label="导入并重命名", height=25, command=rename_meshes_to_filename)
    cmds.text(label="贴图路径:")
    cmds.textField("textureDirectory")
    cmds.button(label="更新贴图路径", height=25, command=update_texture_paths)
    cmds.setParent('..')
    cmds.setParent('..')

    # 贴图处理框架
    cmds.frameLayout(label="贴图处理", collapsable=True, collapse=False, width=390)
    cmds.columnLayout(adj=True, rowSpacing=3)
    cmds.button(label="1. 转换为PNG格式", command="convert_to_png()")
    cmds.button(label="2. 清理无效贴图节点", command="clean_nonexistent_textures()")
    cmds.button(label="3. 断开所有透明贴图", command="disconnect_all_transparency_textures()")
    cmds.button(label="4. 连接透明贴图", command="assign_alpha_texture()")
    cmds.button(label="5. 连接法线贴图", command="link_normal_map()")
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    # ====== 模型处理选项卡 ======
    model_tab = cmds.columnLayout(adj=True)
    cmds.frameLayout(label="模型清理", collapsable=True, collapse=False, width=390)
    cmds.columnLayout(adj=True, rowSpacing=3)
    cmds.button(label="对齐到首选物体", command="align_pivots_to_first_selected()")
    cmds.button(label="删除所有骨骼", command="delete_joints()")
    cmds.button(label="解锁并删除约束", command="unlock_and_disconnect_selected()")
    cmds.button(label="删除所有层", command="delete_all_layers()")
    cmds.button(label="统一法线方向", command="unify_normals()")
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    # ====== 命名工具选项卡 ======
    naming_tab = cmds.columnLayout(adj=True)

    # 序列化命名框架
    cmds.frameLayout(label="序列化命名", collapsable=True, collapse=False, width=390)
    cmds.columnLayout(adj=True, rowSpacing=3)
    cmds.text(label="新前缀:")
    global prefixField
    prefixField = cmds.textField(height=25)
    cmds.button(label="序列化重命名", command="rename_objects_with_serialization()")
    cmds.setParent('..')
    cmds.setParent('..')

    # 字符串处理框架
    cmds.frameLayout(label="字符串处理", collapsable=True, collapse=False, width=390)
    cmds.columnLayout(adj=True, rowSpacing=3)
    global string1_field, string2_field
    string1_field = cmds.textFieldGrp(label="字符串 1:", adj=True, columnWidth=[(1, 60), (2, 280)])
    string2_field = cmds.textFieldGrp(label="字符串 2:", adj=True, columnWidth=[(1, 60), (2, 280)])
    cmds.button(label="重排字符串顺序",
                command=lambda *args: rename_objects(
                    cmds.textFieldGrp(string1_field, query=True, text=True),
                    cmds.textFieldGrp(string2_field, query=True, text=True)))
    cmds.setParent('..')
    cmds.setParent('..')

    # 命名清理框架
    cmds.frameLayout(label="命名清理", collapsable=True, collapse=False, width=390)
    cmds.columnLayout(adj=True, rowSpacing=3)
    cmds.button(label="删除冒号前字符", command="remove_before_colon()")
    cmds.button(label="删除冒号后字符", command="remove_after_colon()")
    cmds.button(label="清理多余下划线", command="replace_multiple_underscores()")
    cmds.button(label="重命名材质球", command="rename_materials_for_selected_objects()")
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')

    # 设置选项卡标签
    cmds.tabLayout(tabs, edit=True, tabLabel=(
        (texture_tab, "贴图处理"),
        (model_tab, "模型处理"),
        (naming_tab, "命名工具")))

    cmds.showWindow(main_window)

create_ui()