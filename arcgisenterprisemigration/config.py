import os


class ConfigCMD():
    main_path = r'C:\local\project'
    input_path = r'C:\local\project\input'
    output_path = r'C:\local\project\output'
    user_role_folder = 'users'
    content_folder = 'contents'
    deploy_sd_folder = 'deploy-sd'
    deploy_folder = 'deploy'
    arcgisinput_folder = 'arcgisinput'

    user_role_csv_filename = 'users.csv'
    portal_content_csv_filename = 'portal_contents.csv'
    server_content_csv_filename = 'server_contents.csv'
    deploy_service_report_filename = 'deploy_report.csv'

    user_role_out_file = ''
    portal_contents_out_file = ''
    deploy_report_service_file = ''
    deploy_sd_folder = ''


    arcgisinput_folder_path = ''
    deploy_folder_input_path = ''
    deploy_folder_output_path = ''

    path_os_separator = '\\'


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
        if not os.path.exists(self.output_path+ '\\' + self.deploy_sd_folder):
            os.makedirs(self.output_path+ '\\' + self.deploy_sd_folder)
        if not os.path.exists(self.input_path+self.path_os_separator+self.deploy_folder):
            os.makedirs(self.input_path+self.path_os_separator+self.deploy_folder)
        if not os.path.exists(self.output_path+self.path_os_separator+self.deploy_folder):
            os.makedirs(self.output_path+self.path_os_separator+self.deploy_folder)
        if not os.path.exists(self.input_path+ self.path_os_separator+ self.arcgisinput_folder):
            os.makedirs(self.input_path+ self.path_os_separator+ self.arcgisinput_folder)

        self.user_role_out_file = self.output_path + '\\' + self.user_role_folder + '\\' + self.user_role_csv_filename
        self.portal_contents_out_file = self.output_path + '\\' + self.content_folder + '\\' + self.portal_content_csv_filename
        self.server_contents_out_file = self.output_path + '\\' + self.content_folder + '\\' + self.server_content_csv_filename
        self.deploy_sd_folder = self.output_path+ '\\' + self.deploy_sd_folder + '\\'
        self.arcgisinput_folder_path = self.input_path+ self.path_os_separator+ self.arcgisinput_folder + self.path_os_separator
        self.deploy_folder_input_path = self.input_path+self.path_os_separator+self.deploy_folder
        self.deploy_folder_output_path = self.output_path+self.path_os_separator+self.deploy_folder
        self.deploy_report_service_file = self.deploy_folder_output_path+self.path_os_separator+self.deploy_service_report_filename
        self.template_aprx_path = self.input_path+self.path_os_separator+"/template/template.aprx"
        self.template_deploy_path = self.output_path+self.path_os_separator+"temp.aprx"
        self.list_svc_portal_csv = self.input_path + self.path_os_separator + "l_portal.csv"
        self.list_svc_server_csv = self.input_path + self.path_os_separator + "l_server.csv"
        self.arcgis_source_portal_username = os.environ['ARCGIS_SOURCE_PORTAL_USERNAME']
        self.arcgis_source_portal_password = os.environ['ARCGIS_SOURCE_PORTAL_PASSWORD']
        self.arcgis_enterprise_source_url = os.environ['ARCGIS_ENTERPRISE_SOURCE_URL']

