package evel_javalibrary.att.com.maindir;

/**************************************************************************//**
 * @file
 * Sample Agent for EVEL library
 *
 * This file implements the Sample Agent which is intended to provide a
 * simple wrapper around the complexity of AT&T's Vendor Event Listener API so
 * that VNFs can use it without worrying about details of the API transport.
 * It also shows how events can be formatted with data for POST
 *
 * License
 * -------
 * Unless otherwise specified, all software contained herein is
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *****************************************************************************/


import org.apache.log4j.Logger;

import evel_javalibrary.att.com.*;
import evel_javalibrary.att.com.AgentMain.EVEL_ERR_CODES;
import evel_javalibrary.att.com.EvelFault.EVEL_SEVERITIES;
import evel_javalibrary.att.com.EvelFault.EVEL_SOURCE_TYPES;
import evel_javalibrary.att.com.EvelFault.EVEL_VF_STATUSES;
import evel_javalibrary.att.com.EvelHeader.PRIORITIES;
import evel_javalibrary.att.com.EvelMobileFlow.MOBILE_GTP_PER_FLOW_METRICS;
import evel_javalibrary.att.com.EvelScalingMeasurement.MACHINE_CHECK_EXCEPTION;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_CODEC_USE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_CPU_USE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_DISK_USE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_FEATURE_USE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_FSYS_USE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_HUGE_PAGE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_IPMI;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_LATENCY_BUCKET;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_LOAD;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_MEM_USE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_NIC_PERFORMANCE;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_PROCESS_STATS;
import evel_javalibrary.att.com.EvelScalingMeasurement.MEASUREMENT_IPMI.MEASUREMENT_IPMI_PROCESSOR;
import evel_javalibrary.att.com.EvelStateChange.EVEL_ENTITY_STATE;
import evel_javalibrary.att.com.EvelSyslog.EVEL_SYSLOG_FACILITIES;
import evel_javalibrary.att.com.EvelThresholdCross.EVEL_ALERT_TYPE;
import evel_javalibrary.att.com.EvelThresholdCross.EVEL_EVENT_ACTION;

import org.apache.log4j.Level;

import java.io.*;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Date;

public class Main
{

    public static void main(String[] args)
	{
		String collector_ip = null;
		String file_name = null;
		String location = null;
		
		collector_ip = args[0];
		int collector_port = Integer.parseInt(args[1]);
		String url = "http://"+collector_ip;
		file_name = args[2];
		location = args[3];
		
		try{
			AgentMain.evel_initialize(url,collector_port,null,null,"will","pill",null,null,null,url,collector_port,"will","pill",Level.TRACE);
		}
		catch (Exception e)
		{
			 e.printStackTrace();
		}

	try {
                Thread.sleep(5);
            } 
	catch( Exception e )
            {
                e.printStackTrace();
            }
		
        EvelNotification notification = new EvelNotification("notifyFileReady", "FileReady_1797490e-10ae-4d48-9ea7-3d7d790b25e1","PM_MEAS_FILES", "fileReady");
          //EvelNotification notification = new EvelNotification("Notification_vVNF", "vmname_ip","PM_MEAS_FILES", "fileReady");

          notification.evel_notification_add_namedarray(file_name, "location", location);
          notification.evel_notification_add_namedarray(file_name, "compression", "gzip");
          notification.evel_notification_add_namedarray(file_name, "fileFormatType", "org.3GPP.32.435#measCollec");
          notification.evel_notification_add_namedarray(file_name, "fileFormatVersion", "V10");
          //"PM_FILE_3GPP_TS_28.550", "location", "ftpes://135.3.1.44:21/pmfiles/A20180531.1030+0600-1045+0600_5gBts213.bin.gz","compression","gzip","fileFormatType","org.3GPP.32.435#measCollec","fileFormatVersion","V10"
          notification.evel_notification_add_stateInterface_set("StateChange"); 
        System.out.println("A NEW NOTIFICATION IS PREPARED & EVEL POST CALLED");
	AgentMain.evel_post_event(notification);
        System.out.println("EVEL SHUTDOWN CALLED");			
	AgentMain.evel_shutdown();
	}
}          



