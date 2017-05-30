#include<linux/kernel.h>
#include<linux/module.h>
#include<linux/init.h>
static int hello_init(void)
{
	printk(KERN_WARNING "Hello Kernel\n");
	return 0;
}
static void hello_exit(void)
{
	printk("Bye Kernel\n");
}
/*main module function*/
module_init(hello_init);
module_exit(hello_exit);