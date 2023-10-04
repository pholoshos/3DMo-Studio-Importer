import bpy
import os
import requests
from bpy_extras.io_utils import ImportHelper

# Define a custom category for your operators and panels
bl_category = "Mo3D Studio"

# Define a custom property group to store model URLs
class CustomModelGroup(bpy.types.PropertyGroup):
    model_url: bpy.props.StringProperty(
        name="Model URL",
        description="URL of the model to download",
    )

# Define a custom property for the access key
class CustomSettings(bpy.types.PropertyGroup):
    access_key: bpy.props.StringProperty(
        name="Access Key",
        description="Access key for authentication",
        default="",
    )

# Define an operator to import a selected model
class ImportModelOperator(bpy.types.Operator):
    bl_idname = "import.import_model"
    bl_label = "Import Model"
    bl_options = {'UNDO'}

    model_index: bpy.props.IntProperty()  # Store the model index

    def execute(self, context):
        model_url = context.scene.download_models[self.model_index].model_url
        local_path = bpy.path.abspath("//downloaded_model.obj")

        # Add authentication (compare access_key with the stored key)
        if context.scene.custom_settings.access_key != "YourSecretKey":
            self.report({'ERROR'}, "Invalid access key. Please enter a valid access key.")
            return {'CANCELLED'}

        # Download the model from the website
        response = requests.get(model_url)
        with open(local_path, 'wb') as f:
            f.write(response.content)

        # Import the downloaded model into Blender
        bpy.ops.import_scene.obj(filepath=local_path)

        return {'FINISHED'}

# Define a custom panel to display your operators and model list
class MyCustomPanel(bpy.types.Panel):
    bl_label = "My Models"
    bl_idname = "PT_MyModels"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = bl_category  # Assign the custom category

    def draw(self, context):
        layout = self.layout

        # Display the list of models in the panel
        for idx, model in enumerate(context.scene.download_models):
            row = layout.row()
            row.label(text=f"Model {idx + 1}: {model.model_url}")
            row.operator("import.import_model", text="Import").model_index = idx  # Set the model index

        # Add a text input for the access key
        layout.prop(context.scene.custom_settings, "access_key")

# Register the custom operator, panel, and property group
def register():
    bpy.utils.register_class(CustomModelGroup)
    bpy.utils.register_class(ImportModelOperator)
    bpy.utils.register_class(MyCustomPanel)
    bpy.utils.register_class(CustomSettings)

    bpy.types.Scene.download_models = bpy.props.CollectionProperty(type=CustomModelGroup)
    bpy.types.Scene.custom_settings = bpy.props.PointerProperty(type=CustomSettings)

    # Add example model URLs to the collection property
    example_model_urls = bpy.context.scene.download_models
    example_model_urls.add()
    example_model_urls[0].model_url = "https://example.com/model1.obj"
    example_model_urls.add()
    example_model_urls[1].model_url = "https://example.com/model2.obj"

# Unregister the custom operator, panel, and property group
def unregister():
    bpy.utils.unregister_class(CustomModelGroup)
    bpy.utils.unregister_class(ImportModelOperator)
    bpy.utils.unregister_class(MyCustomPanel)
    bpy.utils.unregister_class(CustomSettings)

    del bpy.types.Scene.download_models
    del bpy.types.Scene.custom_settings

# Run the registration when the script is executed
if __name__ == "__main__":
    register()
