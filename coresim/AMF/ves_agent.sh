#!/bin/bash
echo "Started executing the ves-agent bash file"

cd /root/

echo -e "$(pwd)"

ls -lrt

echo -e "git clone https://github.com/onap/vnfsdk-ves-agent"

git clone https://github.com/onap/vnfsdk-ves-agent

mv vnfsdk-ves-agent/veslibrary/ves_javalibrary .

rm -rf vnfsdk-ves-agent

rm -rf /root/ves_javalibrary/evel_javalib2/src_test/evel_javalibrary/att/com/maindir/Main.java /root/ves_javalibrary/evel_javalib2/pom.xml

mv Main.java /root/ves_javalibrary/evel_javalib2/src_test/evel_javalibrary/att/com/maindir/

mv pom.xml /root/ves_javalibrary/evel_javalib2

cd /root/ves_javalibrary/evel_javalib2

mvn clean install -DskipTests

cd ~

echo "ves-agent script executed"

