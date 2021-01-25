#!/usr/bin/env python

import os
import sys
from time import sleep
from application_config import *
from config_parser import ConfigParser
from create_pm_file import CreatePMFile
import socket
import logging
from logging.handlers import TimedRotatingFileHandler

global granularity_period


def ves_agent_call(filename, application_config):
    '''
    :param filename: Generated pm_file name
    :param application_config: object of ApplicationConfig to get the
                            values of the variables defined in that class
    :return:
    '''
    logger.info("Here we will trigger the ves agent application")
    cwd = os.getcwd()
    os.chdir(application_config.ves_agent_directory_path)

    collector_port = application_config.dcae_collector_port
    collector_ip = application_config.dcae_collector_ip
    simulator_ip = get_sim_ip()
    sftp_username = application_config.sftp_username
    sftp_password = application_config.sftp_password
    sftp_port = application_config.sftp_port
    file_location = 'sftp://'+sftp_username+':'+sftp_password+'@'+simulator_ip+':'+sftp_port+ '/pm_directory/'  +filename
    # COMPILE
    os.system(application_config.ves_agent_compile_cmd)
    # Now RUN the VES-AGENT
    run_cmd = (application_config.ves_agent_run_cmd + " " + collector_ip + " "
               + collector_port + " " + filename + " " + file_location)
    os.system(run_cmd)
    os.chdir(cwd)


def simulate_amf(application_config, param):
    '''
    :param application_config:
    :param param: AMF
    :return: it returns None if there are no active nssai else
            it will generate a pm_file and calls ves_agent_call function
    '''
    logger.info('Parameter flag is '+param)
    config_parser = ConfigParser(logger, application_config)
    config_flag, active_nssai, config_data = \
        config_parser.compare_snssai_config()
    # Data after config_parser
    logger.info(config_flag)
    logger.info(active_nssai)
    logger.info(config_data)
    if active_nssai == 0:
        logger.info("None of the S-NSSAI is activated")
        return None
    else:
        logger.info("Now Compute PM File for the Active NSSAI's")
        application_config.save_data(active_nssai,
                                     application_config.temp_SNSSAI_data)
        create_pm = CreatePMFile(logger, application_config)
        if config_data == None:
            temp_config_data = config_parser.read_temp_config()
            filename = create_pm.prepare_xml_file(active_nssai, temp_config_data)
        else:
            filename = create_pm.prepare_xml_file(active_nssai, config_data)
        logger.info("Received filename " + filename
                    + " Now a VES-agent need to be called")
        ves_agent_call(filename, application_config)

def get_sim_ip():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        logger.info(host_name)
        logger.info(host_ip)
        return host_ip
    except:
        logger.info("Unable to get Hostname and IP")
        return "0.0.0.0"


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.system("mkdir logs")
    if not os.path.exists('__tmp'):
        os.system("mkdir __tmp")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s.%(funcName)s(): %(message)s")
    handler = TimedRotatingFileHandler('./logs/simulator.log', when="midnight", interval=1, encoding='utf8')
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info('AMF Application started')
    if sys.argv[1] == 'AMF':
        while 1:
            with open('/etc/config/amf-conf/granularity_period.txt') as mytxt:
                for line in mytxt:
                    # granularity_period = math.ceil(
                    # float(line.rstrip("\n")) * 60)
                    granularity_period = int((line.rstrip("\n")))
            application_config = ApplicationConfig(logger, granularity_period)
            simulate_amf(application_config, sys.argv[1])
            logger.info("APPLICATION IS GOING TO SLEEP FOR "
                        + str(granularity_period) + " seconds at time ")
            sleep(granularity_period)
