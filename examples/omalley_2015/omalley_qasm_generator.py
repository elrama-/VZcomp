
def omalley(basename='omalley',theta=0):
    tomo_list = ['I', 'X', 'Y90', 'Y-90', 'X90', 'X-90']
    for i in range(36):
        id_0 = int(i % 6)
        id_1 = int(((i - id_0)//6) % 6)
        omalley_base = ['X q0\n', 'X-90 q0\n', 'Y90 q1\n', 'H q0\n',
                        'CZ q0,q1\n', 'H q0\n', 'Z%d\n' % theta,
                        'H q0\n', 'CZ q0,q1\n', 'H q0\n', 'X90 q0\n',
                        'Y-90 q0\n']
        omalley_base.append(tomo_list[id_0]+' q0\n')
        omalley_base.append(tomo_list[id_1]+' q1\n')
        f = open(basename+'_%d.qasm'%i,mode='w+')
        f.writelines(omalley_base)
        f.close()
