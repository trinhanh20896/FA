from cmath import sqrt
import codecs #ファイル出力時に追加
import math
import statistics
import numpy

def eval_individual(POP_SIZE,NUM_OF_VARI,init_ind,fun_eval,best_obj_v,best_ite,best_ind, gene, NUM_CONS, Cons_A, Cons_b, best_Real_x, Obj,fuz_obj_max,fuz_obj_min,NUM_OF_OFJ):

    e_ind=open('result.txt','a') #'a'の方が良いか検討する．
    ite_obj=open('iteration_result.txt','a') #'a'の方が良いか検討する．

    # 各ホタルの評価値の算出

    r_cons = [" " for j in range(NUM_CONS)] #制約右辺値の確認用配列

    # 実行可能解を格納するための配列
    Real_x = [['' for i in range(NUM_OF_VARI)] for j in range(POP_SIZE)]

    # ファジィ目標導入後の目的関数値保存用
    fuz_Obj = [['' for j in range(NUM_OF_OFJ)] for i in range(POP_SIZE)]

    #実行可能解と目的関数値の導出

    A = numpy.argsort(init_ind)
    for i in range(POP_SIZE):
        fun_eval[i] = 0
        for k in range(NUM_OF_OFJ):
            fuz_Obj[i][k] = 0

        for j in range(NUM_CONS):
            r_cons[j] = 0

        for j in range(NUM_OF_VARI):
            cons_flag = 0
            for k in range(NUM_CONS):
                r_cons[k] += Cons_A[k][A[i][j]]
                if r_cons[k] > Cons_b[k]:
                    cons_flag = 1

            if cons_flag == 1:
                Real_x[i][A[i][j]] = 0
                for k in range(NUM_CONS):
                    r_cons[k] -= Cons_A[k][A[i][j]]
            else:
                Real_x[i][A[i][j]] = 1

        #Real_xの出力
        #print('Real_x',"\n",file = e_ind)
        #print('individual',i,"\n",file = e_ind)
        #for j in range(NUM_OF_VARI):
        #    print(Real_x[i][j], end = "\t",file = e_ind)
        #print('\n',file = e_ind)
        
        
        for j in range(NUM_OF_VARI):
            if Real_x[i][j] == 1:
               for k in range(NUM_OF_OFJ):
                   fuz_Obj[i][k] += Obj[k][j] #ここを改良 Obj[]を2次元配列化

        #目的関数値の出力
        #print('Objの値',"\n",file = e_ind)
        #for k in range(NUM_OF_OFJ):
        #    print(fuz_Obj[i][k], end = "\t",file = e_ind)
        #print('\n',file = e_ind)

        #ファジイ目標を入れて正規化
        for k in range(NUM_OF_OFJ):
            fuz_Obj[i][k] = (fuz_Obj[i][k]-fuz_obj_min[k])/(fuz_obj_max[k]-fuz_obj_min[k]) 

        #ファジィ目標導入後の目的関数値の出力
        #print('fuz_objの値',"\n",file = e_ind)
        #for k in range(NUM_OF_OFJ):
        #    print(fuz_Obj[i][k], end = "\t",file = e_ind)
        #print('\n',file = e_ind)

        #正規化された値の中の最小値を導出し，fun_evalに値を渡す．
        for k in range(NUM_OF_OFJ):
            if k == 0:
               fun_eval[i] = fuz_Obj[i][k]
            else:
               if fun_eval[i] > fuz_Obj[i][k]:
                  fun_eval[i] = fuz_Obj[i][k]

        #ファジィ目標導入後の目的関数値の出力
        #print('最大化決定後のfuz_obj(fun_eval)の値',"\n",file = e_ind)
        #print(fun_eval[i], end = "\n",file = e_ind)


#結果の出力
#    for i in range(POP_SIZE):
#       print('individual',i,"\t",fun_eval[i], end = "\n",file = e_ind)
#       print('',file = e_ind)

#   print('Real_x',"\n",file = e_ind)
#   for i in range(POP_SIZE):
#      print('individual',i,"\n",file = e_ind)
#      for j in range(NUM_OF_VARI):
#           print(Real_x[i][j], end = "\t",file = e_ind)
#      print('\n',file = e_ind)

#   print('A',"\n",file = e_ind)
#   for i in range(POP_SIZE):
#      print('individual',i,"\n",file = e_ind)
#      for j in range(NUM_OF_VARI):
#           print(A[i][j], end = "\t",file = e_ind)
#      print('\n',file = e_ind)

# 初期世代の目的関数の最良値・最悪値・平均値の算出
    ite_max = max(fun_eval)
    ite_min = min(fun_eval)
    ite_ave = statistics.mean(fun_eval)

    # 出力は別ファイルに行う
    print('世代','\t', '目的関数値(最小値)', '\t', '目的関数値(最大値)' ,'\t', '目的関数値(平均値)', end = '\n',file = ite_obj)    

    print('世代',0, '\t', ite_min, '\t', ite_max,'\t', ite_ave, end = '\n',file = ite_obj)    

    max_index = fun_eval.index(ite_max)
    best_obj_v[0] = ite_max
    best_ite[0] = 0
    for j in range (NUM_OF_VARI):
        best_ind[j] = init_ind[max_index][j]
        best_Real_x[j] = Real_x[max_index][j]

    ite_obj.close()    
    e_ind.close()
