from .BaseController import BaseController
import os
import re

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id):
        project_path  = os.path.join(self.files_dir, project_id)
        
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        return project_path

    def generate_unique_file_path(self, orig_file_name: str, project_id: str):
        
            random_key = self.generate_random_string()
            project_path = ProjectController().get_project_path(project_id=project_id)

            cleaned_file_name = self.get_clean_file_name(
                orig_file_name=orig_file_name
            )

            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

            while os.path.exists(new_file_path):
                random_key = self.generate_random_string()
                new_file_path = os.path.join(
                    project_path,
                    random_key + "_" + cleaned_file_name
                )

            return new_file_path, random_key + "_" + cleaned_file_name


    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name