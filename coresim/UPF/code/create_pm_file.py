import json
import random
import math
from lxml import etree as xml


class CreatePMFile:
    def __init__(self, logger, application_config):
        self.application_config = application_config
        self.logger = logger

    def prepare_xml_file(self, active_nssai, config_data):
        '''
        :param active_nssai: dict of active nssai
                            (ex: {"sNssai" : ["001-100002", "003-100003"]} )
        :return: filename of the genarated pm_file
        '''
        self.logger.info("Creating the PM XML file for active S-NSSAIs")
        self.logger.info(json.dumps(active_nssai, indent=4, sort_keys=True))

        tree = xml.Element('measCollecFile')
        tree.set('xmlns', self.application_config.measCollecFile_xmlns)

        pm_header = xml.SubElement(tree, 'fileHeader')
        pm_header.set('dnPrefix', self.application_config.fileHeader_dnPrefix)
        pm_header.set('vendorName',
                      self.application_config.fileHeader_vendorName)
        pm_header.set('fileFormatVersion',
                      self.application_config.fileHeader_fileFormatVersion)

        pm_file_sender = xml.SubElement(pm_header, 'fileSender')
        pm_file_sender.set('senderName',
                           self.application_config.fileSender_senderName)
        pm_file_sender.set('senderType',
                           self.application_config.fileSender_senderType)

        pm_meas_collec_header = xml.SubElement(pm_header, 'measCollec')
        pm_meas_collec_header.set('beginTime',
                                  self.application_config.measData_beginTime)

        pm_meas_data = xml.SubElement(tree, 'measData')
        pm_measured_element = xml.SubElement(pm_meas_data, 'managedElement')
        pm_measured_element.set('swVersion',
                               self.application_config.
                               managedElement_swVersion)
        pm_measured_element.set('localDn',
                               self.application_config.managedElement_localDn)

        for k, v in dict(active_nssai).items():
            for i in range(len(v)):
                pm_meas_info = xml.SubElement(pm_meas_data, 'measInfo')
                pm_meas_info.set('measInfoId',
                                 self.application_config.measInfo_measInfoId
                                 + str(i))

                pm_job = xml.SubElement(pm_meas_info, 'job')
                pm_job.set('jobId', self.application_config.measInfo_jobId)

                pm_gran_period = xml.SubElement(pm_meas_info, 'granPeriod')
                pm_gran_period.set('endTime', self.application_config.
                                   measInfo_granPeriod_endTime)
                pm_gran_period.set('duration', self.application_config.
                                   measInfo_granPeriod_duration)

                pm_rep_period = xml.SubElement(pm_meas_info, 'repPeriod')
                pm_rep_period.set('duration', self.application_config.
                                  measInfo_repPeriod_duration)

                pm_meas_type = xml.SubElement(pm_meas_info, 'measType')
                pm_meas_type.set(self.application_config.
                                 measInfo_measType_name,
                                 self.application_config.
                                 measInfo_measType_value1)
                pm_meas_type.text = (self.application_config.
                                     measInfo_measType_text1 + str(v[i]))

                pm_meas_type = xml.SubElement(pm_meas_info, 'measType')
                pm_meas_type.set(self.application_config.
                                 measInfo_measType_name,
                                 self.application_config.
                                 measInfo_measType_value2)
                pm_meas_type.text = (self.application_config.
                                     measInfo_measType_text2 + str(v[i]))

                pm_meas_type = xml.SubElement(pm_meas_info, 'measType')
                pm_meas_type.set(self.application_config.
                                 measInfo_measType_name,
                                 self.application_config.
                                 measInfo_measType_value3)
                pm_meas_type.text = (self.application_config.
                                     measInfo_measType_text3 + str(v[i]))

                pm_meas_type = xml.SubElement(pm_meas_info, 'measType')
                pm_meas_type.set(self.application_config.
                                 measInfo_measType_name,
                                 self.application_config.
                                 measInfo_measType_value4)
                pm_meas_type.text = (self.application_config.
                                     measInfo_measType_text4 + str(v[i]))

                pm_meas_value = xml.SubElement(pm_meas_info, 'measValue')
                pm_meas_value.set('measObjLdn', self.application_config.
                                  measInfo_measValue_measObjLdn)

                pm_meas_value_r = xml.SubElement(pm_meas_value, 'r')
                pm_meas_value_r.set(self.application_config.
                                    measInfo_measValue_r_name,
                                    self.application_config.
                                    measInfo_measValue_r_value1)
                UL_data = self.get_InDataOctN3UPF(config_data, v[i])
                pm_meas_value_r.text = UL_data

                pm_meas_value_r = xml.SubElement(pm_meas_value, 'r')
                pm_meas_value_r.set(self.application_config.
                                    measInfo_measValue_r_name,
                                    self.application_config.
                                    measInfo_measValue_r_value2)
                DL_data = self.get_OutDataOctN3UPF(config_data, v[i])
                pm_meas_value_r.text = DL_data
                pm_meas_value_r = xml.SubElement(pm_meas_value, 'r')
                pm_meas_value_r.set(self.application_config.
                                    measInfo_measValue_r_name,
                                    self.application_config.
                                    measInfo_measValue_r_value3)
                pm_meas_value_r.text = str(math.ceil(int(UL_data)/(int(self.application_config.granularity_period)/60)))

                pm_meas_value_r = xml.SubElement(pm_meas_value, 'r')
                pm_meas_value_r.set(self.application_config.
                                    measInfo_measValue_r_name,
                                    self.application_config.
                                    measInfo_measValue_r_value4)
                pm_meas_value_r.text = str(math.ceil(int(DL_data)/(int(self.application_config.granularity_period)/60)))

                pm_meas_value_suspect = xml.SubElement(pm_meas_value,
                                                       'suspect')
                pm_meas_value_suspect.text = (self.application_config.
                                              measInfo_measValue_suspect)

        pm_footer = xml.SubElement(tree, 'fileFooter')
        pm_meas_collec_footer = xml.SubElement(pm_footer, 'measCollec')
        pm_meas_collec_footer.set('endTime',
                                  self.application_config.MeasData_endTime)

        tree = xml.ElementTree(tree)

        filename = self.get_filename()

        tree.write(self.application_config.target_pm_directory + filename,
                   encoding="utf-8", xml_declaration=True, pretty_print=True)
        self.logger.info("New PM File created : " + filename)
        return filename

    def get_InDataOctN3UPF(self, config_data, snssai_id):
        '''
        :param config_data: complete config data of all active nssai's
        :param snssai_id: id of the active snssai_id passed
        :return: return a random PM data for the RegisteredSubNbrMean KPI for snssai_id passed
        '''
        for k, v in dict(config_data).items():
            for i in range(len(v)):
                if 'expDataRateUL' in dict(v[i]):
                    if dict(v[i])['s-nssai'] == snssai_id:
                        expDataRateUL = dict(v[i])['expDataRateUL']
                        #From the maxNumberofUEs in slice profile, Just simulating a random integer in that range
                        random_int = random.randint(100, int(expDataRateUL))
                        return str(random_int)
                else:
                    print("Inside get_InDataOctN3UPF method & expDataRateUL NOT-Found in slice profile")
                    return str(random.randint(100, 1000))

    def get_OutDataOctN3UPF(self, config_data, snssai_id):
        '''
        :param config_data: complete config data of all active nssai's
        :param snssai_id: id of the active snssai_id passed
        :return: return a random PM data for the RegisteredSubNbrMean KPI for snssai_id passed
        '''
        for k, v in dict(config_data).items():
            for i in range(len(v)):
                if 'expDataRateDL' in dict(v[i]):
                    if dict(v[i])['s-nssai'] == snssai_id:
                        expDataRateDL = dict(v[i])['expDataRateDL']
                        #From the maxNumberofUEs in slice profile, Just simulating a random integer in that range
                        random_int = random.randint(100, int(expDataRateDL))
                        return str(random_int)
                else:
                    print("Inside get_OutDataOctN3UPF method & expDataRateDL NOT-Found in slice profile")
                    return str(random.randint(100, 1000))

    def get_filename(self):
        '''
        :return: returning the filename,as part of it followed the
                file_naming_convections standards
        '''
        initial_name = self.application_config.date_dict['initial_filename']
        return initial_name + '_' + self.application_config.\
            measInfo_jobId+ '_S-NSSAI.xml'
