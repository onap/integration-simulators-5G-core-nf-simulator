import os
import json


class ConfigParser:
    def __init__(self, logger, application_config):
        self.application_config = application_config
        self.active_sNssai = dict()
        self.logger = logger

    def read_temp_config(self):
        '''
        :return: loads the last iterated s-nssai config data from the temporary config file.
        '''
        self.logger.info("Reading temperory Config_Data")
        data = self.application_config.load_data(
            self.application_config.temp_config_file)
        self.logger.info(json.dumps(data, indent=4, sort_keys=True))
        return data

    def read_config(self):
        '''
        :return: loads the lastest s-nssai config data from s-nssai config file.
        '''
        self.logger.info("Reading Latest Config_Data")
        data = self.application_config.load_data(
            self.application_config.config_file)
        self.logger.info(json.dumps(data, indent=4, sort_keys=True))
        self.application_config.save_data(
            data, self.application_config.temp_config_file)

        return data

    def parser(self, data):
        '''
        :param data: nssai_config file data
        :return: if no active nssai then it returns 0 else returns the dict
                of active_nssai(ex: {"sNssai ": ["001-100002","003-100003"]} )
        '''
        self.logger.info("Parser Method instantiated")
        for k1, v1 in dict(data).items():
            ls = []  # list of s-nssai id which are active
            for i in range(len(v1)):
                if dict(v1[i])['status'] == "activated":
                    ls.append(dict(v1[i])['s-nssai'])
            self.active_sNssai[k1] = ls
        length = len(self.active_sNssai['sNssai'])
        self.logger.debug(self.active_sNssai['sNssai'])
        if length == 0:
            return 0
        else:
            return self.active_sNssai

    def compare_snssai_config(self):
        '''
        :return: it compares the latest and existing config(if present)files,
            if both have same active nssai then it returns SAME as the flag,
            active_nssai dict and config_data as None else MODIFIED as the
            flag, active_nssai dict and config_data with new data
        '''
        self.logger.info("Entered into json compare")
        temp_data = {}
        # check for whether already previous data exists
        if os.path.exists(self.application_config.temp_config_file):
            temp_data = self.read_temp_config()
        # read the latest configuration data from the config file
        data = self.read_config()
        active_list = self.parser(data)
        if data == temp_data:
            return "SAME", active_list, None
        else:
            return "MODIFIED", active_list, data
