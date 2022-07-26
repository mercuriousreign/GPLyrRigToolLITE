# ##### BEGIN GPL LICENSE BLOCK #####
#
#   GPLyrRigTool Lite is an addon for Blender created by Zaima Atoshi(MercuryRaven)
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
bl_info = {
    "name": "GPLyrRigTool Lite",
    "description": "ToolBox that speeds up greasepencil layer and bone rigging workflow for Blender 2D animation",
    "author": "MercuryRaven",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "3D View > GPLyrRig Tool",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}
import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       CollectionProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       Bone,
                       GPencilLayer
                       )






#=========General properties==============

class GENERAL_Props(PropertyGroup):
    my_path: StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )

    text_console : StringProperty(
        name = "",
        description = "Set the names of new layers here",
        default = "",

    )


    gp_target : PointerProperty(type=bpy.types.GreasePencil,name="")

    arm_target : PointerProperty(type=bpy.types.Armature,name="")






#=========Individual operator==============

class STRCNSL_OT_clearConsole(Operator):
    """clear all text from console"""
    bl_label = "Clear all text from console"
    bl_idname = "gplyrigtool.clear_console"


    def execute (self,context):
        scene = context.scene
        propts = scene.le_props
        propts.text_console = ""
        return{"FINISHED"}


class STRCNSL_OT_delLayerbyText(Operator):
    """Delete layers from the text in console
    Format : Layer1,Layer2,Layer3"""
    bl_label = "Delete layer by text"
    bl_idname = "gplyrigtool.dellayer_bytext"


    def execute (self,context):
        scene = context.scene
        propts = scene.le_props
        strings = propts.text_console.split(',')
        gp = propts.gp_target


        if gp == []:
            self.report({'INFO'}, "nothing is selected")
            return {"CANCELLED"}


        for str in strings:

            if str in gp.layers:
                lyr = gp.layers.remove(gp.layers[str])

        self.report({'INFO'},"Deleted all layers based on input")
        return {"FINISHED"}


class STRCNSL_OT_createLayerbyText(Operator):
    """Creates layer from the text in the console,
    Format : Layer1,Layer2,Layer3"""
    bl_label = "Create ONLY layer by text"
    bl_idname = "gplyrigtool.layer_bytext"


    def execute (self,context):
        scene = context.scene
        propts = scene.le_props
        strings = propts.text_console.split(',')
        gp = propts.gp_target


        if gp == None:
            self.report({'INFO'}, "nothing is selected")
            return {"CANCELLED"}


        for str in strings:
            if str not in gp.layers:

                  lyr = gp.layers.new(str)

        self.report({'INFO'},"All layers have been created based on input")
        return {"FINISHED"}




#====== top operators =============

class GENERAL_OT_createLayersbyBnsname (Operator):
    bl_label = "Create Layers by all Bones in armature"
    bl_idname = "gplyrigtool.layer_bybone"
    err1 : bpy.props.StringProperty(name="Nothing selected")


    def execute (self, context):

        scene = context.scene
        myprops = scene.le_props

        arm = bpy.data.objects[myprops.arm_target.name]
        gp =  myprops.gp_target
        print("the arrm")

        if arm == None or gp == None :
            self.report({'INFO'}, "nothing is selected")

            return {"CANCELLED"}



        for bone in arm.data.bones:
            lyr = gp.layers.new(bone.name)
            #lyr.parent = myprops.arm_target
            lyr.parent = arm
            lyr.parent_type = 'BONE'
            lyr.parent_bone = bone.name
        return {"FINISHED"}




#-----------------------------------------------
class GPLYRIGTOOL_UL_lyrANDbone(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        bn = None
        lyrs = None
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(bn)
            layout.prop(lyrs)

#----------UI panel-------------------------------------

class GPLyrRigTool :
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GPLyrRigTool Lite"



class GENERAL_PT_setObjs(GPLyrRigTool, bpy.types.Panel):
    bl_idname = "GPLYRIGTOOL_PT_mainMenu"
    bl_label = "Set Objects"


    def draw (self, context):
        layout = self.layout
        scene = context.scene
        myprops = scene.le_props
        k = layout.box()
        p = k.column()
        d = k.row()
        g = k.row()
        layout.label(text="Set GreasePencil object and Armature to bind ")
        d.label(text="GreasePencil")
        d.label(text="Armature")
        g.prop(myprops,"gp_target")
        g.prop(myprops,"arm_target")


        layout.separator()

        layout.operator("gplyrigtool.layer_bybone")



class STRCNSL_PT_console(GPLyrRigTool, bpy.types.Panel):
    bl_idname = "GPLYRIGTOOL_PT_layerbytext"
    bl_label = "Text Console"

    def draw (self, context):
        layout = self.layout
        scene = context.scene
        myprops = scene.le_props


        layout.label(text="Input Layer names and/or Bone names for the listed functions usage ")

        layout.prop(myprops,"text_console")

        layout.operator("gplyrigtool.clear_console")
        layout.operator("gplyrigtool.layer_bytext")
        layout.operator("gplyrigtool.dellayer_bytext")




class panelList(GPLyrRigTool, bpy.types.Panel):
    bl_idname = "GPLyrRigTool_PT_list"
    bl_label = "Set Individual"


    def draw (self, context):
        layout = self.layout
        scene = context.scene
        myprops = scene.le_props
        k = layout.box()
        p = k.column()
        g = k.row()


#+..................................................................


classes = (
   GENERAL_Props,
   STRCNSL_OT_createLayerbyText,
   STRCNSL_OT_delLayerbyText,
   STRCNSL_OT_clearConsole,
   GENERAL_OT_createLayersbyBnsname,
   GENERAL_PT_setObjs,
   STRCNSL_PT_console

)



def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.le_props = PointerProperty(type=GENERAL_Props)



def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.le_props

if __name__ == "__main__":
    register()
