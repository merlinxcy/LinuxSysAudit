obj-m := hook_detection.o
all:
	$(MAKE) -C /lib/modules/4.9.0-kali3-amd64/build M=$(PWD) modules
.PHONY:clean
clean:
	$(MAKE) -C /lib/modules/4.9.0-kali3-amd64/build M=$(pwd) clean
