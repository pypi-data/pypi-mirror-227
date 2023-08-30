SITE={{cookiecutter.cmk_dev_site}}
SITE_PATH=/omd/sites/${SITE}

AGENT_PATH=/usr/lib/check_mk_agent/plugins/
PLUGIN_PATH=${SITE_PATH}/local/lib/check_mk/base/plugins/agent_based
WATO_PATH=${SITE_PATH}/local/share/check_mk/web/plugins/wato
AGENT_SPECIAL_PATH=${SITE_PATH}/local/share/check_mk/agents/special
CHECKS_PATH=${SITE_PATH}/local/share/check_mk/checks


CMK_RUN_HOST={{cookiecutter.cmk_dev_hostname}}


PROJECT_DIR={{cookiecutter.project_slug}}
AGENT_ID={{cookiecutter.agent_id}}
dev-deploy-plugin:
#	agent
	sudo cp ./agent_special/agent_${AGENT_ID} ${AGENT_SPECIAL_PATH}/agent_${AGENT_ID}
	chmod +x ${AGENT_SPECIAL_PATH}/agent_${AGENT_ID}
#	agent invoker
	sudo cp ./agent_invoker/agent_${AGENT_ID} ${CHECKS_PATH}/agent_${AGENT_ID}
	chmod +x ${CHECKS_PATH}/agent_${AGENT_ID}
#	wato
	sudo cp ./wato/${AGENT_ID}_register.py ${WATO_PATH}/${AGENT_ID}_register.py
#	service check
	sudo cp ./plugin/service_${AGENT_ID}.py ${PLUGIN_PATH}/service_${AGENT_ID}.py

	omd restart ${SITE}


dev-undeploy-plugin:
	rm -rf ${AGENT_SPECIAL_PATH}/agent_${AGENT_ID}
	rm -rf ${CHECKS_PATH}/agent_${AGENT_ID}
	rm -rf ${WATO_PATH}/${AGENT_ID}_register.py
	rm -rf ${PLUGIN_PATH}/service_${AGENT_ID}.py

	omd restart ${SITE}

# create MKP
# mkp config file should be at var/check_mk/packages (in OMD[site])
dev-create-mkp:
	cp ./mkp/config ${SITE_PATH}/var/check_mk/packages/{{cookiecutter.agent_id}}


# pack MKP, run in OMD[site]
# mkp config file should be at var/check_mk/packages (in OMD[site])
dev-pack-kmp: 
	mkp pack {{cookiecutter.agent_id}}
	ll | grep {{cookiecutter.agent_id}}


dev-copy-makefile-to-site:
	mkdir -p ${SITE_PATH}/dev/{{cookiecutter.agent_id}}
	cp Makefile ${SITE_PATH}/dev/{{cookiecutter.agent_id}}/Makefile

# run in OMD[site]
dev-check-agent:
	cmk -d ${CMK_RUN_HOST}

# run in OMD[site]
dev-debug-agent:
	cmk --debug --checks={{cookiecutter.agent_id}} -vvn ${CMK_RUN_HOST}

# run in OMD[site]
dev-detect-plugins:
	cmk --detect-plugins={{cookiecutter.agent_id}} -vI ${CMK_RUN_HOST}