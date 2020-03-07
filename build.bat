@echo off
del /q dist\*
echo Build with pyinstaller...
pyinstaller ticker.py --onefile -n iidxseg --add-data "DSEG14Classic-Italic.ttf;."
copy iidxseg_launch.bat dist\iidxseg_launch.bat
echo Create an archive...
powershell Compress-Archive -Path dist\* -DestinationPath dist\iidxseg_release.zip