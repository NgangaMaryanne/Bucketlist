.PHONY: sonarqube smile all
sonarqube:
	@"${scannerHome}/bin/sonar-scanner"
smile:
	@echo hello world
all:
	smile sonarqube
