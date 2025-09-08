# DreamcastPVMTool

Quick unpack/repack Python script for PVM files, I'm aware that the Sonic Adventure DLC Tool can do this (https://github.com/X-Hax/sa_tools/wiki/DLC-Editor) but I just wanted something dedicated to this feature. 

python pvm_tool.py extract FILENAME.PVM out_dir -> dumps PVRs in order in directory of your choosing

python pvm_tool.py repack FILENAME.PVM out_dir FILENAME_new.PVM -> packs them back in order

This doesn't really allow you to put more or less files back but file size changes are no problem since PVM just concatenates PVRs together, so this script uses the original header, and just builds a new file with the new PVRs from your directory you chose for extraction. 
