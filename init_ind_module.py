import codecs #ファイル出力時に追加
import random

def initial_individual(POP_SIZE,NUM_OF_VARI,init_ind,Lower_Bound,Upper_Bound):
# 初期個体群の形成

    f_init=open('init_result.txt','a') #'a'の方が良いか検討する．
    for i in range(POP_SIZE):

        for j in range(NUM_OF_VARI):
            rand = random.uniform(Lower_Bound,Upper_Bound)
            #print(rand, end = '\t',file = f_init) # 半角スペースをTabに変更する
            init_ind[i][j] = rand
            #init_ind[i][j] = (Upper_Bound-Lower_Bound)*rand-Lower_Bound
            
        #print('\n',file = f_init)

    f_init.close()
