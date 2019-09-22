#include <stdio.h>
#include <string.h>

/*
 * memcmp-hijack.c, Hijack memcmp() function
 */

// https://stackoverflow.com/questions/35364772/how-to-print-memory-bits-in-c
void print_bytes(void *ptr, int size) 
{
    unsigned char *p = ptr;
    int i;
    for (i=0; i<size; i++) {
        printf("%02hhX ", p[i]);
    }
    printf("\n");
}

int memcmp ( const void * ptr1, const void * ptr2, size_t num ) {
    printf(" -> start memcmp\n");
    printf(" -> ptr1: ");
    print_bytes(ptr1, num);
    printf(" -> ptr2: ");
    print_bytes(ptr2, num);
    printf(" -> end memcmp\n");
    return 0;
}

