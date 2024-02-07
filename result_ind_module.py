import codecs #ファイル出力時に追加
import random

def result_individual(POP_SIZE,NUM_OF_VARI,init_ind):
# 現在の個体の出力

    r_ind=open('result.txt','a') #'a'の方が良いか検討する．

    for i in range(POP_SIZE):
        print('individual',i,file = r_ind)
        for j in range(NUM_OF_VARI):
            print(init_ind[i][j], end = "\t",file = r_ind)
        print('',file = r_ind)

# 2進数として出力
#   for i in range(POP_SIZE):
#       print('individual',i,file = r_ind)
#       for j in range(NUM_OF_VARI):
#           print(init_ind[i][j], end = '', file = r_ind)
#       print('',file = r_ind)

    r_ind.close()
