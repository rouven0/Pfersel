install:
	@echo Setting up the virtual environment...
	@python3 -m venv venv
	@echo Installing requirements...
	@venv/bin/pip install -r requirements.txt
	@echo Done.
	@echo Setting up the systemd service...
	@sed -i 's|WORKINGDIRECTORY|'$(PWD)'|g' ManasoupBumpReminder.service
	@sed -i 's|USER|'$(USER)'|g' ManasoupBumpReminder.service
	@sudo cp ./ManasoupBumpReminder.service /etc/systemd/system
	@sudo systemctl daemon-reload
	@echo Done. The service is ready to be started

uninstall:
	@echo Removing systemd service...
	@sed -i 's|'$(PWD)'|WORKINGDIRECTORY|g' ManasoupBumpReminder.service
	@sed -i 's|'$(USER)'|USER|g' ManasoupBumpReminder.service
	@sudo rm /etc/systemd/system/ManasoupBumpReminder.service
	@sudo systemctl daemon-reload
	@echo Done.

start:
	@sudo systemctl start ManasoupBumpReminder.service
	@echo Service started

stop:
	@sudo systemctl stop ManasoupBumpReminder.service
	@echo Service stopped
