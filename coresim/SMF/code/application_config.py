import json
from builtins import staticmethod
from datetime import datetime, timedelta



class ApplicationConfig:
    @staticmethod
    def save_object(obj, filepath, operator=None):
        if operator is None:
            operator = 'w'
        with open(filepath, operator) as fout:
            json.dump(obj, fout)
        # with open(filepathname, 'wb') as fout:
        #     pickle.dump(obj, fout)

    @staticmethod
    def load_object(filepath):
        with open(filepath) as fout:
            data = json.load(fout)
            return data

    def save_data(self, data, filepath, operator=None):
        self.save_object(data, filepath, operator)

    def load_data(self, filepath):
        return self.load_object(filepath)

    def __init__(self, logger, granularity_period):
        self.logger = logger
        logger.info("Application Config Instantiation Started")

        self.sftp_username = 'admin'
        self.sftp_password = 'admin'
        self.sftp_port = '22'

        self.date_dict = self.get_date_dict(granularity_period)
        self.temp_config_file = '__tmp/nssai_config'
        self.config_file = '/etc/config/smf-conf/supportedNssai.json'
        self.temp_SNSSAI_data = '__tmp/S-NSSAI_list'
        self.dcae_collector_ip_file_path = '/etc/config/smf-conf/dcae_collector_ip.txt'
        self.dcae_collector_port_file_path = '/etc/config/smf-conf/dcae_collector_port.txt'
        self.granularity_period_file_path = '/etc/config/smf-conf/granularity_period.txt'
        self.target_pm_directory = '/data/'+ self.sftp_username +'/pm_directory/'

        self.measCollecFile_xmlns = \
            'http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec'
        self.fileHeader_dnPrefix = 'www.google.com'
        self.fileHeader_vendorName = 'LTTS'
        self.fileHeader_fileFormatVersion = '32.435 V10.0'
        self.fileSender_senderName = 'some sender name'
        self.fileSender_senderType = "some send Type"
        self.measData_beginTime = self.date_dict['beginTime']
        self.MeasData_endTime = self.date_dict['endTime']

        self.managedElement_swVersion = 'r0.1'
        self.managedElement_localDn = 'SMFMeasurement'
        self.measInfo_measInfoId = 'SMFFunction'
        self.measInfo_jobId = 'SMFJob8'
        self.measInfo_granPeriod_duration = 'PT'+str(granularity_period)\
                                            + 'S'
        self.measInfo_granPeriod_endTime = self.date_dict['endTime']
        self.measInfo_repPeriod_duration = 'PT'+str(granularity_period)\
                                           + 'S'
        self.measInfo_measType_name = 'p'
        self.measInfo_measType_value = '1'
        self.measInfo_measType_text = 'SM.SessionNbrMean.'
        self.measInfo_measValue_measObjLdn = 'some measObjLdn'
        self.measInfo_measValue_r_name = 'p'
        self.measInfo_measValue_r_value = '1'
        self.measInfo_measValue_r_text = '10'
        self.measInfo_measValue_suspect = 'false'

        self.dcae_collector_ip = self.read_data(
            self.dcae_collector_ip_file_path)
        self.dcae_collector_port = self.read_data(
            self.dcae_collector_port_file_path)
        self.ves_agent_directory_path = \
            '/root/ves_javalibrary/evel_javalib2/src_test'
        self.ves_agent_compile_cmd = \
            'javac -cp .:../target/evel_javalib2-1.1.1-SNAPSHOT.jar:' \
            './log4j.jar:slf4j-api.jar:slf4j-log4j12-1.6.0.jar:' \
            './javax.json-1.0.jar ./evel_javalibrary/att/com/maindir/Main.java'
        self.ves_agent_run_cmd = \
            'java -cp .:../target/evel_javalib2-1.1.1-SNAPSHOT.jar:' \
            './log4j.jar:slf4j-api.jar:slf4j-log4j12-1.6.0.jar:' \
            './javax.json-1.0.jar evel_javalibrary.att.com.maindir.Main'

        self.logger.info("Application Config Instantiation Completed")

    @staticmethod
    def get_date_dict(granularity_period):
        '''
        :return: returns date dictionary( date_dict = {"beginTime":start_time,
         "endTime":end_time, "UTC_diff":utc_diff, "initial_filename":filename})
        '''
        date_dict = {}
        granularity_period_mints = granularity_period/60
        timestamp = datetime.now()
        
        start_time = timestamp.replace(microsecond=0).isoformat() + 'Z'
        date_dict['beginTime'] = start_time
        timestamp_delta = timestamp + timedelta(minutes=granularity_period_mints)
        end_time = timestamp_delta.replace(microsecond=0).isoformat() + 'Z'
        date_dict['endTime'] = end_time
        utc_diff = (datetime.now().astimezone().
                    replace(microsecond=0, second=0).isoformat())[19:]
        date_dict['UTC_diff'] = utc_diff
        filename = 'B'+str(timestamp.strftime("%Y%d%m.%H%M"))\
                   + utc_diff + '-' + str((timestamp_delta.
                                           strftime("%Y%d%m.%H%M"))[9:13]) \
                   + utc_diff
        date_dict['initial_filename'] = filename
        return date_dict

    @staticmethod
    def read_data(file_path):
        temp = None
        with open(file_path) as fout:
            for line in fout:
                temp = line.rstrip("\n")
        return temp
