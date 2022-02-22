import os


class ConfigCMD():
    main_path = r'C:\project'
    input_path = r'C:\project\input'
    output_path = r'C:\project\output'
    user_role_folder = 'users'
    content_folder = 'contents'
    user_role_csv_filename = 'users.csv'
    portal_content_csv_filename = 'portal_contents.csv'

    user_role_out_file = ''
    portal_contents_out_file = ''

    def __init__(self) -> None:
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if not os.path.exists(self.input_path+ '\\' + self.user_role_folder):
            os.makedirs(self.input_path+ '\\' + self.user_role_folder)
        if not os.path.exists(self.output_path+ '\\' + self.user_role_folder):
            os.makedirs(self.output_path+ '\\' + self.user_role_folder)
        if not os.path.exists(self.output_path+ '\\' + self.content_folder):
            os.makedirs(self.output_path+ '\\' + self.content_folder)

        self.user_role_out_file = self.output_path + '\\' + self.user_role_folder + '\\' + self.user_role_csv_filename
        self.portal_contents_out_file = self.output_path + '\\' + self.content_folder + '\\' + self.portal_content_csv_filename
        
