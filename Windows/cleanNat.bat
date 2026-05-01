@echo off
set /p _confirm=Press Enter to run: net stop winnat
net stop winnat
set /p _confirm=Press Enter to run: netsh interface ipv4 show excludedportrange protocol=tcp
netsh interface ipv4 show excludedportrange protocol=tcp
set /p _confirm=Press Enter to run: net start winnat
net start winnat
set /p _confirm=Press Enter to run: netsh interface ipv4 show excludedportrange protocol=tcp
netsh interface ipv4 show excludedportrange protocol=tcp
