
install:
	sudo cp sever/v4l2grab /mnt/root
	sudo cp servers/led_server.py /mnt/root

client:  
	python client/client.py
