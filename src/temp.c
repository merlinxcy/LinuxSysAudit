#include <linux/module.h>
#include <linux/kernel.h>
#include <asm/unistd.h>
#include <linux/types.h>
#include <linux/dirent.h>
#include <linux/string.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/moduleparam.h>
#include <asm/uaccess.h>
#include <linux/sched.h>
//#include <asm/semaphore.h>


//#include <linux/malloc.h>
//#include <sys/syscall.h>
//#include <sys/types.h>
extern void *sys_call_table[];
int modified_mkdir(const char * path,mode_t mode);
int modified_mkdir(const char * path,mode_t mode)
{
return orig_mkdir(path,mode);
}
int init_module(void)
{
orig_mkdir=sys_call_table[SYS_mkdir];
sys_call_table[SYS_mkdir]=modified_mkdir;
return 0;
}
void cleanup_module(void)
{
sys_call_table[SYS_mkdir]=orig_mkdir;
return;
}