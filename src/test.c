#include <linux/init.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
//#include<linux/config.h>

#include <linux/kernel.h>/*printk()*/
#include <linux/sched.h>

MODULE_LICENSE("GPL");


static __init int test_driver_init(void)
{
    int result = 0;
    char cmd_path[] = "/usr/bin/touch";
    char* cmd_argv[] = {cmd_path,"/touchX.txt",NULL};
    char* cmd_envp[] = {"HOME=/", "PATH=/sbin:/bin:/usr/bin", NULL};

    result = call_usermodehelper(cmd_path, cmd_argv, cmd_envp, UMH_WAIT_PROC);
    printk(KERN_DEBUG "test driver init exec! there result of call_usermodehelper is %d\n", result);
    printk(KERN_DEBUG "test driver init exec! the process is \"%s\", pid is %d.\n",current->comm, current->pid);
    return result;
}


static __exit void test_driver_exit(void)
{
    int result = 0;
    char cmd_path[] = "/bin/rm";
    char* cmd_argv[] = {cmd_path,"/touchX.txt",NULL};
    char* cmd_envp[] = {"HOME=/", "PATH=/sbin:/bin:/usr/bin", NULL};

    result = call_usermodehelper(cmd_path, cmd_argv, cmd_envp, UMH_WAIT_PROC);
    printk(KERN_DEBUG "test driver exit exec! the result of call_usermodehelper is %d\n", result);
    printk(KERN_DEBUG "test driver exit exec! the process is \"%s\",pidis %d \n", current->comm, current->pid);
}

module_init(test_driver_init);
module_exit(test_driver_exit);