#!/usr/bin/env python

from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'dwarf2', """
# DURATION     TID     FUNCTION
            [ 23714] | main() {
 482.922 us [ 23714] |   A::A(0x7ffecd0fe6e0, FOO, 4, "debug info test");
  16.629 us [ 23714] |   std::sort(0x7ffecd0fe700, 0x7ffecd0fe714, &myless);
   5.713 us [ 23714] |   std::sort(0x7ffecd0fe700, 0x7ffecd0fe714, 0x7ffecd0fe700);
   5.853 us [ 23714] |   std::sort(0x7ffecd0fe700, 0x7ffecd0fe714, 0x7ffecd0fe700);
 515.511 us [ 23714] | } = 0; /* main */
""", lang='C++', cflags='-g')

    def build(self, name, cflags='', ldflags=''):
        if cflags.find('-finstrument-functions') >= 0:
            return TestBase.TEST_SKIP

        return TestBase.build(self, name, cflags, ldflags)

    def runcmd(self):
        return '%s %s %s' % (TestBase.uftrace_cmd,
                             '-A . -R . -D2 -F main',
                             't-' + self.name)

    def sort(self, output):
        import re

        result = []
        for ln in output.split('\n'):
            # ignore blank lines and comments
            if ln.strip() == '' or ln.startswith('#'):
                continue
            line = ln.split('|', 1)[-1]
            func = re.sub(r'0x[0-9a-f]+', '0xADDR', line)
            result.append(func)

        return '\n'.join(result)

    def fixup(self, cflags, result):
        # -O2 makes specialization of std::sort() (without 3rd arg)
        return result.replace(', 0x7ffecd0fe700)', ')')
