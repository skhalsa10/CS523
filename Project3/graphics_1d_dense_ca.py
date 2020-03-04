from p5 import *
from dense_1d_ca import CaOneDDense
import ca_inputs

def setup():
    size(CaOneDDense._input_len*4,CaOneDDense._iter_size*4)
    no_stroke()



def draw():
    # print(CaOneDDense._init_cond_len)
    for i in range(0,CaOneDDense._input_len):
        if ca.input[i]=='0':
            fill(0)
        else:
            fill(255)
        square((i*4,ca.current_iter*4),4)

    ca.iterate_once()
    if ca.current_iter >= ca._iter_size:
        no_loop()



ca = CaOneDDense(rules= ca_inputs.testrule, input=ca_inputs.dense_0)
# ca.iterate_all()
run()