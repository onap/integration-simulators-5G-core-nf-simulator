#!/bin/bash
echo "Started executing the sftp bash file"

echo "Creating the sftp user & group with a directory"

mkdir -p /data

chmod 701 /data

groupadd sftp_users

useradd -g sftp_users -d /pm_directory -s /sbin/nologin admin

echo "admin:admin" | chpasswd

mkdir -p /data/admin/pm_directory

chown -R root:sftp_users /data/admin

chown -R admin:sftp_users /data/admin/pm_directory

echo "Now copying the sshd config"

cp sshd_config /etc/ssh/sshd_config

echo "After copying sshd,Restarting the service ssh"

service ssh restart

#mkdir /etc/config

#mkdir /etc/config/smf-conf

#mv ./config/smf-conf/supportedNssai.json /etc/config/

#mv ./config/smf-conf/dcae_collector_ip.txt /etc/config/smf-conf/

#mv ./config/smf-conf/dcae_collector_port.txt /etc/config/smf-conf/

#mv ./config/smf-conf/granularity_period.txt /etc/config/smf-conf/

