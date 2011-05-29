typedef void *(*charp)(char *, ...);

#define charp__(name, type)  void *name(charp func, char *a, type b) { return func(a, b); }
charp__(charp__charp, char *)
charp__(charp__int, int)
charp__(charp__ulint, unsigned long int)
charp__(charp__voidp, void *)

