version:=$(shell ./getversioncode)
versionshort:=$(shell ./getversionshort)
recent_beta_name=-debug-${versionshort}-${version}
bugly_app_key=你的app注册bugly-key
bugly_app_id=你的app注册bugly-id
desTxt=./build/fastlane_sources/des.txt
description=`cat $(desTxt)`

define readDescription
	@echo "\033[32m Note: Have a description if you like:\033[0m"; \
	read des; \
	if [ ! -d './build/fastlane_sources' ]; then \
	mkdir './build/fastlane_sources'; \
	fi; \
	echo $$des > ${desTxt}; 
endef

bugly_beta:
	curl --insecure -F "file=@build/fastlane_sources/regular/debug/${recent_beta_name}.ipa" -F "app_id=${bugly_app_id}" -F "pid=2" -F "title=${recent_beta_name}" -F "description=${description}" https://api.bugly.qq.com/beta/apiv1/exp?app_key=${bugly_app_key} > bugly_response_tmp.json

### fastlane + bugly
fastlane_bugly_debug:
	${call readDescription}
	fastlane build
	make bugly_beta

### fastlane + itunce
fastlane_transXlsx:
	@if [ -d "./fastlane/configSources" ]; then \
	cd ./fastlane/configSources; \
	xlsx2csv itunesExcel.xlsx itunesCSV.csv -e;\
	fi

xlsx2json_parse:
	@if [ -d "./fastlane" ]; then \
	cd ./fastlane; \
	python csvToJson.py; \
	fi

fastlane_config:
	cd fastlane; \
	python fastconfig.py

fastlane_prepare:
	make fastlane_transXlsx
	make xlsx2json_parse
	make fastlane_config
	
fastlane_itunes:fastlane_prepare
	fastlane upload_itc_doall

### creat APP
fastlane_creatApp:
	fastlane creatApplication