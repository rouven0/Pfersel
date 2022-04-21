install:
	@echo Setting up the virtual environment...
	@python3 -m venv venv
	@echo Installing requirements...
	@venv/bin/pip install -r requirements.txt
	@echo Done.
	@echo Setting up the systemd service...
	@sed -i 's|WORKINGDIRECTORY|'$(PWD)'|g' Pfersel.service
	@sudo cp ./Pfersel.service /etc/systemd/system
	@sudo systemctl daemon-reload
	@sudo systemctl enable Pfersel.service
	@echo Done. The service is ready to be started

uninstall:
	@echo Removing systemd service...
	@sudo systemctl disable Pfersel.service
	@sed -i 's|'$(PWD)'|WORKINGDIRECTORY|g' Pfersel.service
	@sudo rm /etc/systemd/system/Pfersel.service
	@sudo systemctl daemon-reload
	@echo Done.

start:
	@sudo systemctl start Pfersel.service
	@echo Service started

stop:
	@sudo systemctl stop Pfersel.service
	@echo Service stopped
