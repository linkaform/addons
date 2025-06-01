# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from lkf_addons import items 


class ScriptResource(items.Items):
    """
    A class for managing and installing scripts in the Linkaform system.
    Inherits from the Items class and provides functionality for script installation and management.
    """

    def install_scripts(self, instalable_scripts: dict, **kwargs) -> None:
        """
        Install scripts in a specified order.
        
        Args:
            instalable_scripts (dict): Dictionary containing script details and installation order
            **kwargs: Additional keyword arguments passed to the install_script method
            
        Returns:
            None
            
        Raises:
            None - Errors during installation are caught and ignored
        """
        install_order = []
        inst = list(instalable_scripts.keys())
        inst.sort()
        print('################ Reading Scripts ################' )
        for x in inst:
            print(f"# {x} ".ljust(48) +'#')
        print('#'*49 )
        
        # Get installation order from scripts dictionary or use default
        if instalable_scripts.get('install_order'):
            install_order = instalable_scripts.pop('install_order')
        else:
            install_order = []
            
        # Install scripts in order
        for script_name in install_order:
            properties = None
            if instalable_scripts:
                detail = instalable_scripts[script_name]
                if detail.get('properties') and detail['properties']:
                    properties = self.load_module_template_file(self.path, detail['properties'])
                image = detail.get('image')
                script_location = self.file_path_to_load(script_name, detail)
                try:
                    res = self.lkf.install_script(
                        self.module, 
                        script_location, 
                        image=image, 
                        script_properties=properties, 
                        local_path=detail.get('path'), 
                        **kwargs
                    )
                except:
                    continue
    def get_script_modules(self, all_items: list, parent_path: str = None) -> dict:
        """
        Recursively scan and organize script modules from a list of files.
        
        Args:
            all_items (list): List of files or nested dictionaries containing files
            parent_path (str): Optional parent path for relative file paths
            
        Returns:
            dict: Organized dictionary of script modules with their properties and file extensions
        """
        data_file = []
        form_file = {}
        default_image = 'linkaform/addons:latest'
        
        # Process each file in the list
        for file in all_items:
            if isinstance(file, dict):
                # Handle nested directories
                path = list(file.keys())[0]
                if parent_path:
                    path = f'{parent_path}/{path}'
                form_file.update(self.get_script_modules(list(file.values())[0], parent_path=path))
                continue
                
            # Process regular files
            file_ext = file.split('.')
            if len(file_ext) != 2:
                print(f'Not a supported file: {file}')
                continue
                
            file_name = file_ext[0]
            file_type = file_name.split('_')[-1]
            
            if file_type == 'properties':
                data_file.append(file)
            else:
                form_file[file_name] = {
                    'properties': '',
                    'image': default_image,
                    'file_ext': file_ext[-1]
                }
                if parent_path:
                    form_file[file_name]['path'] = parent_path
                    
        # Match properties files with their corresponding scripts
        for item in list(form_file.keys()):
            for file in data_file:
                file_ext = file.split('.')
                file_name = file_ext[0]
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    # TODO: Implement multi-extension support
                    form_file[item][file_type] = file_name
        
        return form_file

    def instalable_scripts(self, install_order: list = None) -> dict:
        """
        Get a dictionary of installable scripts with their installation order.
        
        Args:
            install_order (list): Optional list specifying the order of script installation
            
        Returns:
            dict: Dictionary containing script details and installation order
        """
        items_files = self.get_anddons_and_modules_items('scripts')
        scripts_data = self.get_script_modules(items_files)
        
        if install_order:
            scripts_data['install_order'] = install_order
        else:
            scripts_data['install_order'] = list(scripts_data.keys())
        
        return scripts_data
