#include <stdio.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdlib.h>

int kfd;

 struct
 {
      unsigned short limit;
      unsigned int base;
 } __attribute__ ((packed)) idtr;

 struct
 {
      unsigned short off1;
      unsigned short sel;
      unsigned char none, flags;
       unsigned short off2;
 } __attribute__ ((packed)) idt;


 int readkmem (unsigned char *mem, 
              unsigned off, 
              int bytes)
 {
      if (lseek64 (kfd, (unsigned long long) off, 
                                    SEEK_SET) != off)
      {
                 return -1;
      }

      if (read (kfd, mem, bytes) != bytes) 
     {
             return -1;
     }

 }
 
 int main (void)
 {
      unsigned long sct_off;
      unsigned long sct;
       unsigned char *p, code[255];
      int i;


/* request IDT and fill struct */



    asm ("sidt %0":"=m" (idtr));

    if ((kfd = open ("/dev/kmem", O_RDONLY)) == -1)
    {
                perror("open");
            exit(-1);
    }
    
    if (readkmem ((unsigned char *)&idt, 
               idtr.base + 8 * 0x80, sizeof (idt)) == -1)
    {
            printf("Failed to read from /dev/kmem\n");
            exit(-1);
    }
    
    sct_off = (idt.off2 << 16) | idt.off1;

    if (readkmem (code, sct_off, 0x100) == -1)
    {
            printf("Failed to read from /dev/kmem\n");
            exit(-1);
    }

/* find the code sequence that calls SCT */


 sct = 0;
    for (i = 0; i < 255; i++)
    {
            if (code[i] == 0xff && code[i+1] == 0x14 && 
                                        code[i+2] == 0x85)
                    sct = code[i+3] + (code[i+4] << 8) + 
                        (code[i+5] << 16) + (code[i+6] << 24);
    }
    if (sct)
            printf ("sys_call_table: 0x%x\n", sct);
    close (kfd);
 }