all:
	gcc -fPIC -c devaarg.c
	ld -shared -soname devaarg.so.1 -o devaarg.so.1.0 -lc devaarg.o

