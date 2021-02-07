import bpy
import os.path
import subprocess
import pathlib

bl_info = {
    "name": "Trackmania Tools",
    "description": "Adds unofficial Trackmania 2020 support to Blender.",
    "author": "Andre Taulien",
    "version": (0, 1),
    "blender": (2, 90, 0),
    "category": "Import-Export",
    "location": "File > Export",
    "tracker_url": "https://github.com/ataulien/blender-trackmania-tools/issues",
    "wiki_url": "https://github.com/ataulien/blender-trackmania-tools",
    "support": "COMMUNITY",
}

MATERIALS = [
    'PlatformTech',
    'Grass',
    'Pylon',
    'RoadBump',
    'RoadDirt',
    'RoadIce',
    'RoadTech',
    'TrackWall',
    'ItemPillar',
    'ItemBase',
    'CustomBricks',
    'CustomConcrete',
    'CustomDirt',
    'CustomGrass',
    'CustomIce',
    'CustomMetal',
    'CustomPlastic',
    'CustomRock',
    'CustomRoughWood',
    'CustomSand',
    'CustomSnow',
    'DecoHill',
    'TrackBorders',
    'DecalCurbs',
    'DecalMarks',
    'DecalMarksRamp',
    'DecalMarksStart',
    'DecalSpecialTurbo',
    'DecalSponsor1x1BigA',
    'ItemBorder',
    'ItemCactus',
    'ItemLamp',
    'ItemRamp',
    'ItemRoadSign',
    'ItemTrackBarrier',
    'ItemTrackBarrierB',
    'ItemTrackBarrierC',
    'Speedometer',
    'SpeedometerLight_Dyna',
    'SyntheticFloor',
    'Technics',
    'TechnicsTrims',
    'TrackWallClips'
]

class TrackmaniaInstallation:
    
    def trackmania_path():
        possible_locations = [
                'C:\\Program Files\\Epic Games\\TrackmaniaNext\\Trackmania.exe',
                'C:\\Program Files\\Ubisoft\\Ubisoft Game Launcher\\games\\Trackmania\\Trackmania.exe',
                'C:\\Program Files\\Trackmania\\Trackmania.exe'
        ]
        
        for p in possible_locations:
            if os.path.exists(p):
                return os.path.dirname(p)
            
        return None

    def nadeo_importer_path():
        tm_path = TrackmaniaInstallation.trackmania_path()
        nadeo_importer_path = os.path.join(tm_path, 'NadeoImporter.exe')
        
        
        if not os.path.isfile(nadeo_importer_path):
            raise Exception("Failed to find NadeoImporter at: " + nadeo_importer_path)
            return None
        
        return nadeo_importer_path
    
    def user_directory():
        return os.path.expanduser('~/Documents/Trackmania')
    
    def work_directory():
        return os.path.join(TrackmaniaInstallation.user_directory(), 'work')
    
    def addon_work_directory():
        return os.path.join(TrackmaniaInstallation.user_directory(), 'work', 'Items', 'BlenderTrackmaniaExport')

class NadeoImporter:
    def __init__():
        pass
    
    def execute(args):
        nadeo_importer_path = TrackmaniaInstallation.nadeo_importer_path()
        
        if not nadeo_importer_path:
            raise Exception('Failed to find NadeoImporter. Have you installed it correctly?')
         
        try:   
            output = subprocess.check_output([nadeo_importer_path] + args, shell=False)
        except subprocess.CalledProcessError as e:
            cmdline = f'"{nadeo_importer_path}" ' + ' '.join(args)
            return cmdline + '\n\n' + str(e.output)
    
        return True
    
    def convert_item(item_xml_path):
        item_path_relative_to_work = os.path.relpath(item_xml_path, start=TrackmaniaInstallation.work_directory())
        
        return NadeoImporter.execute(['item', item_path_relative_to_work])

class ItemDefinition:
    def __init__(self, name, author_name):
        self.name = name
        self.author_name = author_name
        
    def as_xml(self):
        
        text = ''
        text += f'<Item Type="StaticObject" Collection="Stadium" AuthorName="{self.author_name}">\n'
        text += f'    <MeshParamsLink/>\n'
        text += f'</Item>\n'

        return text

    def target_filepath(self):
        return os.path.join(TrackmaniaInstallation.addon_work_directory(), f'{self.name}.Item.xml')

    def write(self):
        os.makedirs(os.path.dirname(self.target_filepath()), exist_ok=True)

        with open(self.target_filepath(), 'w', encoding='utf-8') as f:
            f.write(self.as_xml())

class MeshDefinition:
    def __init__(self, name, materials_map):
        self.materials_map = materials_map
        self.name = name
    
    def as_xml(self):
        text = ''

        text += '<MeshParams MeshType="Static" Collection="Stadium">\n'
        text += '   <Materials>\n'

        for name, kind in self.materials_map.items():
            text += f'        <Material Name="{name}" Link="{kind}" />\n'

        text += '   </Materials>\n'
        text += '</MeshParams>\n'

        return text

    def target_filepath(self):
        return os.path.join(TrackmaniaInstallation.addon_work_directory(), 'Mesh', f'{self.name}.MeshParams.xml')

    def target_fbx_filepath(self):
        return os.path.join(TrackmaniaInstallation.addon_work_directory(), 'Mesh', f'{self.name}.fbx')

    def write_meshparams(self):
        os.makedirs(os.path.dirname(self.target_filepath()), exist_ok=True)

        with open(self.target_filepath(), 'w', encoding='utf-8') as f:
            f.write(self.as_xml())

    def write_fbx(self):
        bpy.ops.export_scene.fbx(filepath=self.target_fbx_filepath(), check_existing=False, use_selection=False)
                         
def fix_uv_maps():
    """
    NadeoImporter requires your meshes to have 2 UV-Channels, called
    "BaseMaterial" and "Lightmap". If one of those is not available, the
    conversion will fail. To make getting Data into the game easier, the Addon
    can fix those up using reasonable defaults.
    """
    context = bpy.context
    scene = context.scene

    # all meshes on mesh objects in scene
    meshes = [o.data for o in scene.objects
            if o.type == 'MESH']
 
    for m in meshes:
        if len(m.uv_layers) == 0:
            m.uv_layers.new(name='BaseMaterial')
        elif m.uv_layers[0].name != 'BaseMaterial':
            m.uv_layers[0].name = 'BaseMaterial'
        
        if len(m.uv_layers) <= 1:
            lightmap = m.uv_layers.new(name='Lightmap')
        elif 'UVMap' in m.uv_layers[1].name:
            m.uv_layers[1].name = 'Lightmap'


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

def render_thumbnail(target_file):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'TARGA'
    scene.render.filepath = target_file
    scene.render.resolution_x = 64
    scene.render.resolution_y = 64
    
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    
    bpy.ops.render.render(write_still = 1)

class ExportNadeoGbx(Operator):
    """Export as Trackmania Item"""
    bl_idname = "export_trackmania.trackmania" 
    bl_label = "Export Trackmania Item (.item.gbx)"

    item_name: StringProperty(
        name="Item Name",
        description="Name of the item that is shown in the Track Editor",
        default=pathlib.Path(bpy.data.filepath).stem if hasattr(bpy.data, 'filepath') else "Untitled",
    )

    author_name: StringProperty(
        name="Author Name",
        description="Name of the creator (probably you) that will be embedded into the item.",
        default=os.getlogin(),
    )

    fix_uv_maps: BoolProperty(
        name="Create Missing UVs",
        description="Creates UV maps that are required for the NadeoImporter and adds them to all meshes in your scene that need them. You may need to fix them and re-export your item afterwards!",
        default=True,
    )

    render_icon: BoolProperty(
        name="Render Icon",
        description="Renders an icon for the item. (Uses the scenes camera)",
        default=True,
    )

    # is_visible: BoolProperty(
    #     name="Visible",
    #     description="If invisible, the Item will be invisible but can still have collision.",
    #     default=True,
    # )

    # has_collision: BoolProperty(
    #     name="Collision",
    #     description="If enabled, cars will be able to bonk against the item.",
    #     default=True,
    # )

    # def build_fbx_name(self):
    #     name = self.item_name

    #     if not self.is_visible:
    #         name = '_notvisible_' + name

    #     if not self.has_collision:
    #         name = '_notcollidable_' + name

    #     return name

    def invoke(self, context, _event):
        context.window_manager.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        context = bpy.context
        scene = context.scene

        # all meshes on mesh objects in scene
        meshes = [o.data for o in scene.objects
                if o.type == 'MESH']
    
        material_map = {}

        for m in meshes:
            for mat in m.materials:

                mat_type = 'PlatformTech'

                if mat.name in MATERIALS:
                    mat_type = mat.name

                material_map[mat.name] = mat_type

            if len(material_map) == 0:
                self.report({"ERROR"}, f"Mesh {m.name} has no materials!")
                return {'CANCELLED'}

        if self.fix_uv_maps:
            fix_uv_maps()

        item = ItemDefinition(self.item_name, self.author_name)
        mesh_definition = MeshDefinition(self.item_name, material_map)

        item.write()
        mesh_definition.write_meshparams()
        mesh_definition.write_fbx()

        if self.render_icon:
            icon_dir = os.path.join(TrackmaniaInstallation.addon_work_directory(), 'Icon')
            os.makedirs(icon_dir, exist_ok=True)

            render_thumbnail(os.path.join(icon_dir, item.name + '.tga'))

        result = NadeoImporter.convert_item(item.target_filepath())
        
        if result != True:
            self.report({"ERROR"}, f"NadeoImporter failed:\n\n{result}")
            return {'CANCELLED'}
            
        return {'FINISHED'}

# class MaterialSettings(bpy.types.PropertyGroup):
#     my_int: bpy.props.IntProperty()
#     my_float: bpy.props.FloatProperty()
#     my_string: bpy.props.StringProperty()
#     diffuse: bpy.props.PointerProperty(type=bpy.types.Image)

# class TrackmaniaMaterialPanel(bpy.types.Panel):
#     """Creates a Panel in the Material properties window"""
#     bl_label = "Trackmania Material"
#     bl_idname = "OBJECT_PT_tm_material"
#     bl_space_type = 'PROPERTIES'
#     bl_region_type = 'WINDOW'
#     bl_context = "material"

#     def draw(self, context):
#         layout = self.layout

#         material = context.material

#         row = layout.row()
#         row.label(text="Hello world!", icon='WORLD_DATA')

#         row = layout.row()
#         row.label(text="Active material is: " + material.name)
#         row = layout.row()
#         row.prop(material, "name")
        
#         row = layout.row()
#         row.prop(material.trackmania_material, "my_string")
        
#         row = layout.row()
#         row.prop(material.trackmania_material, "diffuse")

#         row = layout.row()
#         row.operator("mesh.primitive_cube_add")

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportNadeoGbx.bl_idname, text="Trackmania Item (.item.gbx)")

classes = [
    ExportNadeoGbx,
    # MaterialSettings,
    # TrackmaniaMaterialPanel,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # bpy.types.Material.trackmania_material = bpy.props.PointerProperty(type=MaterialSettings)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()