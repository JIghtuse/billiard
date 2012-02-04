.PHONY: all clean

CC=gcc
CFLAGS=-Wall -pedantic -Werror -ansi -g -lm
APP=run

all: $(APP)

clean:
	rm *.o *.d $(APP)

$(APP): $(patsubst %.c, %.o, $(wildcard *.c))
	$(CC) $(CFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c -MD $<

include $(wildcard *.d)

test:
	(./$(APP))
