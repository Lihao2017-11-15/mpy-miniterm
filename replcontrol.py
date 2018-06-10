import serial
import string
import time

class ReplControl(object):

    def __init__(self, port, delay=0, debug=False):
        self.port = port
        self.buffer = b""
        self.delay = delay
        self.debug = debug
        #self.initialize()

    def response(self, end=b"\x04"):
        while True:
            bytes_to_read = self.port.inWaiting()
            self.buffer += self.port.read(bytes_to_read)
            try:
                r, self.buffer = self.buffer.split(end, 1)
                return r
            except ValueError:
                pass

    def initialize(self):
        self.port.reset_input_buffer()
        #self.hard_reset()
        # break, break, raw mode
        self.port.write(b"\x03\x03\x01")
        self.port.flush()
        
        
    def hard_reset(self):
        print("Hard reset!")
        self.port.setDTR(False) 
        time.sleep(0.1)
        self.port.setRTS(True)  # EN->LOW
        time.sleep(0.1)
        self.port.setRTS(False)
        time.sleep(1)
        
    def reset(self):
        self.hard_reset()
        self.port.write(b"\x02\x03\x03\x04")

    def command(self, cmd):
        if self.debug: print(">>> %s" % cmd)
        self.port.write(cmd.encode("ASCII") + b"\x04")
        ret = self.response()
        err = self.response(b"\x04>")

        if ret.startswith(b'OK'):
            if err:
                if self.debug: print("<<< %s" % err)
                return err
            elif len(ret) > 2:
                if self.debug: print("<<< %s" % ret[2:])
                try:
                    return eval(ret[2:], {"__builtins__": {}}, {})
                except SyntaxError as e:
                    return e
            else:
                return None

    def statement(self, func, *args):
        return self.command(func + repr(tuple(args)))

    def function(self, func, *args):
        command = "print(repr(%s))" % (func + repr(tuple(args)))
        return self.command(command)

    def variable(self, func, *args):
        return ReplControlVariable(self, func, *args)


class ReplControlVariable(object):

    names = [ '_%s%s' % (x,y) for x in string.ascii_lowercase for y in string.ascii_lowercase ]

    def __init__(self, control, func, *args):
        self.control = control
        self.name = self.__class__.names.pop(0)
        self.control.statement("%s=%s" % (self.name, func), *args)

    def get_name(self):
        return self.name

    def method(self, method, *args):
        return self.control.function("%s.%s" % (self.name, method), *args)

    def __del__(self):
        self.control.command("del %s" % self.name)
        self.__class__.names.append(self.name)