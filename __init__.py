bl_info = {
    "name":"Avatar Exporter",
    "blender": (4,1,0),
    "category": "3D View"
}

import bpy
from bpy.types import Context
import os
import sys
import subprocess

# エクスポート単位のカスタムプロパティアイテムの定義

class AVTSETTING_UL_BoneList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # この関数は各アイテムの描画を行います
        bone = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=bone.name, icon='BONE_DATA', translate=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='BONE_DATA', translate=False)

class AVTSETTING_UL_MeshList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # この関数は各アイテムの描画を行います
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.mesh:
                layout.label(text=item.mesh.name, icon='OUTLINER_OB_MESH', translate=False)
            else:
                layout.label(text="No Mesh", icon='ERROR')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='OUTLINER_OB_MESH', translate=False)

# ボーンリスト用のプロパティグループ
class BoneList(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="")

# メッシュリスト用のプロパティグループ
class MeshList(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(
        name="Mesh",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'MESH',
        description="Export Mesh"
    )

class AvatarExportSetting(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Untitiled")
    file_path: bpy.props.StringProperty(name="FilePath", default="", subtype='DIR_PATH')

    reset_shapekey: bpy.props.BoolProperty(name="Reset ShapeKey", default=True, description="Reset Shapekey on output.")

    armature:  bpy.props.PointerProperty(
        name="Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE',
        description="Select an Armature"
    )

    export_meshes: bpy.props.CollectionProperty(type=MeshList)
    export_meshes_index: bpy.props.IntProperty(name="Export Mesh Index", default=0)

    # 「exclude_bones」を「include_bones」に変更
    include_bones: bpy.props.CollectionProperty(type=BoneList)
    include_bones_index: bpy.props.IntProperty(name="Active Include Bone Index", default=0)
    show_expended: bpy.props.BoolProperty(name="Show Expended", default=True)

class AvatarExporterPanel(bpy.types.Panel):
    bl_label="Avatar Exporter"
    bl_idname="VIEW3D_PT_avatar_exporter_panel"
    bl_space_type='VIEW_3D'
    bl_region_type='UI'
    bl_category='Avatar Exporter'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("avtsetting.new_item", icon='ADD',text="Add Job")

        for index, setting in enumerate(scene.avatar_export_setting_list):
            col = layout.column(align=True)
            box = col.box()
            box_row = box.row()
            icon = 'DISCLOSURE_TRI_DOWN' if setting.show_expended else 'DISCLOSURE_TRI_RIGHT'
            box_row.prop(setting, 'show_expended', icon=icon, text="", emboss=False)
            box_row.prop(setting, 'name', text="", expand=True)
            op = box_row.operator('avtsetting.delete_item', icon='TRASH',text="")
            op.index = index
            op = box_row.operator('avtsetting.start_export_job', icon='EXPORT',text="")
            op.index = index
            if setting.show_expended:
                box2 = col.box()
                row = box2.row(align=True) # Use a row for alignment
                row.prop(setting, 'file_path', text="Output Dir")
                op = row.operator('avtsetting.open_output_dir', icon='FILEBROWSER', text="") # Add the button
                op.index = index
                box2.prop(setting, 'reset_shapekey')
                box2.prop(setting, 'armature')

                # アーマチュアが設定されていたら、包含ボーンリストの設定を表示する
                if setting.armature:
                    col = box2.column()
                    col.label(text="Include Bone List", text_ctxt="")
                    row = col.row()
                    op = row.operator('avtsetting.set_include_bone', icon='BONE_DATA', text="Set Active Bone")
                    op.index = index
                    op = row.operator('avtsetting.clear_include_bone', icon='TRASH', text="Clear List")
                    op.index = index

                    if setting.include_bones and len(setting.include_bones) > 0:
                        col.template_list("AVTSETTING_UL_BoneList", "AVTSETTING_UL_BoneList_" + str(index), setting, 'include_bones', setting, 'include_bones_index')

                col = box2.column()
                op = col.operator('avtsetting.set_export_meshes', icon='OUTLINER_OB_MESH', text="Set Export Mesh")
                op.index = index
                col.template_list("AVTSETTING_UL_MeshList", "AVTSETTING_UL_MeshList_" + str(index), setting, 'export_meshes', setting, 'export_meshes_index')


# Operator to open the output directory
class AVTSETTING_OT_OpenOutputDir(bpy.types.Operator):
    bl_idname = "avtsetting.open_output_dir"
    bl_label = "Open Output Directory"
    bl_description = "Open the specified output directory in the file explorer"

    index: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context):
        setting = context.scene.avatar_export_setting_list[self.index]
        output_dir = bpy.path.abspath(setting.file_path)

        if not output_dir or not os.path.isdir(output_dir):
            self.report({'WARNING'}, f"Output directory not set or does not exist: {output_dir}")
            return {'CANCELLED'}

        try:
            # Use os.startfile for Windows compatibility
            if sys.platform == "win32":
                 os.startfile(output_dir)
            # Fallback for non-Windows systems (requires 'xdg-open' or 'open')
            elif sys.platform == "darwin":
                subprocess.Popen(["open", output_dir])
            else:
                subprocess.Popen(["xdg-open", output_dir])

            self.report({'INFO'}, f"Opened directory: {output_dir}")
        except OSError as e:
             self.report({'ERROR'}, f"Failed to open directory: {e}. Please ensure 'xdg-open' (Linux) or 'open' (macOS) is available.")
             return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"An unexpected error occurred: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class AVTSETTING_OT_NewItem(bpy.types.Operator):
    bl_idname="avtsetting.new_item"
    bl_label="Add New Item"

    def execute(self, context):
        scene = context.scene
        newItem = scene.avatar_export_setting_list.add()
        newItem.name = "Job #" + str(len(scene.avatar_export_setting_list) - 1)
        return {'FINISHED'}

class AVTSETTING_OT_DeleteItem(bpy.types.Operator):
    bl_idname="avtsetting.delete_item"
    bl_label="Delete Item"

    index: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        scene.avatar_export_setting_list.remove(self.index)
        return {'FINISHED'}

def get_all_layer_collections(layer_collection, collections_list):
        """再帰的にレイヤーコレクションをリストに追加する関数"""
        collections_list.append(layer_collection)
        for child in layer_collection.children:
            get_all_layer_collections(child, collections_list)

class AVTSETTING_OT_StartExportJob(bpy.types.Operator):
    bl_idname="avtsetting.start_export_job"
    bl_label="Start Export Job"

    index: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context: Context):
        setting = context.scene.avatar_export_setting_list[self.index]

        filepath = os.path.join(bpy.path.abspath(setting.file_path), setting.name + ".fbx")

        self.report({'INFO'}, "Export FBX: " + filepath )

        # 書き出すメッシュ以外不可視にする
        all_objects = bpy.context.scene.objects

        # LayerCollectionの形でシーン内のコレクションをすべて収集する
        root_layer_collection = bpy.context.view_layer.layer_collection
        layer_collections = []
        get_all_layer_collections(root_layer_collection, layer_collections)

        # Collection型でシーン内のコレクションを取得
        collections = bpy.data.collections

        # コレクションの可視性を記録しつつすべて表示に
        layer_collection_visible = {}
        for layer_collection in layer_collections:
            layer_collection_visible[layer_collection] = layer_collection.hide_viewport
            layer_collection.hide_viewport = False

        collection_visible = {}
        for collection in collections:
            collection_visible[collection] = collection.hide_viewport
            collection.hide_viewport = False

        object_visible = {}
        layer_object_visible = {}

        # オブジェクトの可視性を記録しつつ不可視にする
        for obj in all_objects:
            object_visible[obj] = obj.hide_viewport
            layer_object_visible[obj] = obj.hide_get()
            obj.hide_viewport = True
            obj.hide_set(False)


        # ボーンのデフォームを変更する

        # ボーンの現在の設定を記録
        bone_deform_states = {}
        if setting.armature: # Check if armature is set
            for bone in setting.armature.data.bones:
                bone_deform_states[bone.name] = bone.use_deform

            # include_bonesに含まれたボーンのみTrue、それ以外はFalse
            include_bone_names = [b.name for b in setting.include_bones]
            for bone in setting.armature.data.bones:
                if bone.name in include_bone_names:
                    bone.use_deform = True
                else:
                    bone.use_deform = False

            setting.armature.hide_viewport = False

        for mesh in setting.export_meshes:
            if mesh.mesh: # Check if mesh exists
                mesh.mesh.hide_viewport = False

        # シェイプキーを0にリセットする
        if setting.reset_shapekey:
            for mesh in setting.export_meshes:
                 if mesh.mesh and mesh.mesh.data.shape_keys: # Check if mesh and shape_keys exist
                    for key_block in mesh.mesh.data.shape_keys.key_blocks:
                        key_block.value = 0.0

        # FBXでエクスポート
        try:
            bpy.ops.export_scene.fbx(
                filepath= filepath,
                check_existing=False,
                use_selection=False,
                use_visible=True,
                object_types={'ARMATURE', 'MESH'},
                apply_scale_options='FBX_SCALE_ALL', # すべてFBX
                use_armature_deform_only=True, # デフォームボーンのみ
                add_leaf_bones=False, # リーフボーンオフ
                bake_anim=False, #アニメーションはエクスポートしない
            )
        except Exception as e:
            self.report({'ERROR'}, f"FBX Export failed: {e}")
            # Restore visibility even if export fails
            if setting.armature:
                for bone in setting.armature.data.bones:
                    if bone.name in bone_deform_states:
                        bone.use_deform = bone_deform_states[bone.name]
            for collection, hide_viewport in collection_visible.items():
                collection.hide_viewport = hide_viewport
            for layer_collection, hide_viewport in layer_collection_visible.items():
                layer_collection.hide_viewport = hide_viewport
            for obj, hide_viewport in object_visible.items():
                obj.hide_viewport = hide_viewport
            for obj, hide_viewport in layer_object_visible.items():
                obj.hide_set(hide_viewport)
            return {'CANCELLED'}


        # デフォーム状態を変更前に元に戻す
        if setting.armature:
            for bone in setting.armature.data.bones:
                 if bone.name in bone_deform_states:
                    bone.use_deform = bone_deform_states[bone.name]

        # 表示状態を元に戻す

        # コレクションの可視性を元に戻す
        for collection, hide_viewport in collection_visible.items():
            collection.hide_viewport = hide_viewport
        for layer_collection, hide_viewport in layer_collection_visible.items():
            layer_collection.hide_viewport = hide_viewport

        # オブジェクトの可視性を元に戻す
        for obj, hide_viewport in object_visible.items():
            obj.hide_viewport = hide_viewport

        for obj, hide_viewport in layer_object_visible.items():
            obj.hide_set(hide_viewport)

        return {'FINISHED'}

# 「Exclude Bone」を「Include Bone」に変更
class AVTSETTING_OT_SetIncludeBones(bpy.types.Operator):
    bl_idname="avtsetting.set_include_bone"
    bl_label="Add Include Bone"

    index: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context: Context):
        obj = context.active_object
        scene = context.scene
        setting = scene.avatar_export_setting_list[self.index]

        # Check if the active object is the armature assigned to the setting
        if obj is None or obj != setting.armature:
             self.report({'WARNING'}, "Select the Armature specified in the setting first.")
             return {'CANCELLED'}

        if obj.mode == 'POSE':
            selected_bones = [bone for bone in obj.pose.bones if bone.bone.select]
        elif obj.mode == 'EDIT':
            selected_bones = [bone for bone in obj.data.edit_bones if bone.select]
        else:
            self.report({'WARNING'}, "Switch to Pose or Edit mode on the Armature.")
            return {'CANCELLED'}

        setting.include_bones.clear()

        for bone in selected_bones:
            boneName = setting.include_bones.add()
            boneName.name = bone.name
        return {'FINISHED'}

class AVTSETTING_OT_ClearIncludeBones(bpy.types.Operator):
    bl_idname="avtsetting.clear_include_bone"
    bl_label="Clear Include Bone"

    index: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context: Context):
        scene = context.scene
        scene.avatar_export_setting_list[self.index].include_bones.clear()
        return{'FINISHED'}

class AVTSETTING_OT_SetExportMeshes(bpy.types.Operator):
    bl_idname="avtsetting.set_export_meshes"
    bl_label="Set Export Meshes"

    index: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context: Context):

        # 選択されたオブジェクトを取得する
        selected_objects = bpy.context.selected_objects
        # メッシュオブジェクトのみをフィルタリング
        mesh_objects = [obj for obj in selected_objects if obj.type == 'MESH']

        if not mesh_objects:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}

        context.scene.avatar_export_setting_list[self.index].export_meshes.clear()

        for mesh in mesh_objects:
            mesh_prop = context.scene.avatar_export_setting_list[self.index].export_meshes.add()
            mesh_prop.mesh = mesh

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BoneList)
    bpy.utils.register_class(MeshList)
    bpy.utils.register_class(AvatarExportSetting)
    bpy.utils.register_class(AvatarExporterPanel)
    bpy.utils.register_class(AVTSETTING_OT_NewItem)
    bpy.utils.register_class(AVTSETTING_UL_BoneList)
    bpy.utils.register_class(AVTSETTING_UL_MeshList)
    bpy.utils.register_class(AVTSETTING_OT_DeleteItem)
    bpy.utils.register_class(AVTSETTING_OT_StartExportJob)
    bpy.utils.register_class(AVTSETTING_OT_SetIncludeBones)
    bpy.utils.register_class(AVTSETTING_OT_ClearIncludeBones)
    bpy.utils.register_class(AVTSETTING_OT_SetExportMeshes)
    bpy.utils.register_class(AVTSETTING_OT_OpenOutputDir) # Register the new operator
    bpy.types.Scene.avatar_export_setting_list = bpy.props.CollectionProperty(type=AvatarExportSetting)
    bpy.types.Scene.avatar_export_setting_properties = bpy.props.PointerProperty(type=AvatarExportSetting)

def unregister():
    bpy.utils.unregister_class(BoneList)
    bpy.utils.unregister_class(MeshList)
    bpy.utils.unregister_class(AvatarExportSetting)
    bpy.utils.unregister_class(AvatarExporterPanel)
    bpy.utils.unregister_class(AVTSETTING_OT_NewItem)
    bpy.utils.unregister_class(AVTSETTING_UL_BoneList)
    bpy.utils.unregister_class(AVTSETTING_UL_MeshList)
    bpy.utils.unregister_class(AVTSETTING_OT_DeleteItem)
    bpy.utils.unregister_class(AVTSETTING_OT_StartExportJob)
    bpy.utils.unregister_class(AVTSETTING_OT_SetIncludeBones)
    bpy.utils.unregister_class(AVTSETTING_OT_ClearIncludeBones)
    bpy.utils.unregister_class(AVTSETTING_OT_SetExportMeshes)
    bpy.utils.unregister_class(AVTSETTING_OT_OpenOutputDir) # Unregister the new operator
    del bpy.types.Scene.avatar_export_setting_list
    del bpy.types.Scene.avatar_export_setting_properties

if __name__ == "__main__":
    register()
