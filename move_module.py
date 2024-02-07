from math import exp, sqrt
import random
import statistics
import math
import numpy

def move_individual(POP_SIZE,NUM_OF_VARI,ind,fun_eval,Alpha,Beta_zero,Gamma,best_obj_v,best_ite,sedai,best_ind,Upper_Bound,Lower_Bound, gene, R_POP_SIZE, R_POP_SEL,R_P_S,Alpha_sel,NUM_CONS,Cons_A,Cons_b,Obj,fuz_obj_max,fuz_obj_min,NUM_OF_OFJ):

    move=open('result.txt','a') #'a'の方が良いか検討する．

    ite_obj=open('iteration_result.txt','a') #'a'の方が良いか検討する．

    a_m_ind = [['' for i in range(NUM_OF_VARI)] for j in range(POP_SIZE)] # move後の個体群

    kari_fun_eval = ['' for i in range(POP_SIZE)] # move後の目的関数値

    r_fun_eval = ['' for i in range(POP_SIZE)] # 掛け合わせをする個体選定用の目的関数値の配列

    random_pop_num = ['' for i in range(POP_SIZE)] # 個体番号選定用の配列 (計算に使用するのみ)

    r_pop_num = ['' for i in range(R_POP_SIZE)] # 掛け合わせる個体の番号を保存するための配列

    # ファジィ目標導入後の目的関数値保存用
    fuz_Obj = ['' for j in range(NUM_OF_OFJ)]


    for i in range(POP_SIZE):
        random_pop_num[i] = i
        r_fun_eval[i] = fun_eval[i]

    if R_POP_SEL == 1: #ランダムに掛け合わせをする個体を選択する場合  
        for i in range(0,R_POP_SIZE):
            rand = random.uniform(0,POP_SIZE-i) # 範囲を与えるときはunifrom
            #print(i, '番目の個体の乱数', "\t", rand, end = '\n',file=move) # 乱数の値
            individual_num = int(rand)
            #print(i, '番目の個体', "\t",individual_num, '番目の個体',"\t", end = '\n',file=move) # 個体のiと個体jの距離

            r_pop_num[i] = random_pop_num[individual_num]
            for j in range(individual_num,POP_SIZE-i-1):
                random_pop_num[j] = random_pop_num[j+1]

# 結果の出力
#        print('最終結果', end = '\n',file=move)
#        for i in range(0,R_POP_SIZE):
#            print(i, '番目の個体', "\t",r_pop_num[i], '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号

    elif R_POP_SEL == 0: #目的関数値の良いものから順に掛け合わせをする個体を選択する場合
        A = numpy.argsort(r_fun_eval)
# 結果の出力
#        print('ソート後の個体番号の結果', end = '\n',file=move)
#        for i in range(0,POP_SIZE):
#            print(i, '番目の個体', "\t",A[i], '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号

        for i in range(0,R_POP_SIZE):
            individual_num = A[R_POP_SIZE - 1 - i] #23年9月27日書き換え．大きいものから順に選択
#           print(i, '番目の個体', "\t",individual_num, '番目の個体',"\t", end = '\n',file=move) # 個体のiと個体jの距離

            r_pop_num[i] = individual_num

# 結果の出力
#        print('最終結果', end = '\n',file=move)
#        for i in range(0,R_POP_SIZE):
#            print(i, '番目の個体', "\t",r_pop_num[i], '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号

    elif R_POP_SEL == 2: #目的関数値の良いものからR_P_S個，残りをランダムに選択する場合
        A = numpy.argsort(r_fun_eval)
# 結果の出力
#        print('ソート後の個体番号の結果', end = '\n',file=move)
#        for i in range(0,POP_SIZE):
#            print(i, '番目の個体', "\t",A[i], '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号

        for i in range(0,R_P_S): #良いものからR_P_S個
            individual_num = A[R_POP_SIZE - 1 - i] #23年9月27日書き換え．大きいものから順に選択
#            print(i, '番目の個体', "\t",individual_num, '番目の個体',"\t", end = '\n',file=move) # 個体のiと個体jの距離

            r_pop_num[i] = individual_num

            for j in range(0,POP_SIZE): #選出された個体番号の摘出
                if random_pop_num[j] == individual_num:
                    iteration = j
                    j=POP_SIZE

            for j in range(iteration,POP_SIZE-i-1): #random_pop_numの修正
                random_pop_num[j] = random_pop_num[j+1]

#        print('修正後のrandom_pop_numの結果', end = '\n',file=move)
#        for i in range(0,POP_SIZE-R_P_S): #修正後のrandom_pop_numの出力
#            print(i, '番目の個体', "\t",random_pop_num[i], '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号


        for i in range(R_P_S,R_POP_SIZE): # ランダムにR_POP_SIZE - R_P_S個選択
            rand = random.uniform(0,POP_SIZE - R_P_S - i) # 範囲を与えるときはunifrom
#            print(i, '番目の個体の乱数', "\t", rand, end = '\n',file=move) # 乱数の値
            individual_num = int(rand)
#            print(i, '番目の個体', "\t",individual_num, '番目の個体',"\t", end = '\n',file=move) # 個体のiと個体jの距離

            r_pop_num[i] = random_pop_num[individual_num]
            for j in range(individual_num,POP_SIZE - R_P_S - i - 1):
                random_pop_num[j] = random_pop_num[j+1]

# 結果の出力
#        print('最終結果', end = '\n',file=move)
#        for i in range(0,R_POP_SIZE):
#            print(i, '番目の個体', "\t",r_pop_num[i], '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号

    #ホタルの掛け合わせに関するコード
    for i in range(0,POP_SIZE): # ホタルの掛け合わせ

        best_next_ind = 0 #個体が進化したかどうか
        first_next_ind = 0 #個体を進化するプロセスを経たかどうか (進化させても目的関数値が良くならない場合の検出用)
        new_f_eval = 0.0

        for z in range(0,R_POP_SIZE): # iのホタルと掛け合わせるホタルの番号を選定

            j = r_pop_num[z]

#            print(z, '回目の個体', "\t",j, '番目の個体',"\t", end = '\n',file=move) # ランダムに選定された個体番号


            kari_a_m_ind = ['' for l in range(NUM_OF_VARI)] # move後の個体群 (jの値ごとに計算)

            if i != j:
                if fun_eval[i] <= fun_eval[j]: #目的関数値が j の方が大きければ (良ければ) 掛け合わせ 23年9月27日書き換え
                    attract = 0.0 # 魅力の値
                    dist = 0.0 # 個体間の距離
                    
                    if gene == 0: #距離の正規化をしない．距離の2乗を魅力に用いる．
                        for l in range(0,NUM_OF_VARI):
                            dist += (ind[i][l] - ind[j][l])*(ind[i][l] - ind[j][l])

                        dist = math.sqrt(dist)
#                       print(i, '番目の個体', "\t",j, '番目の個体',"\t",'距離の値',dist,end = '\n',file=move) # 個体のiと個体jの距離

                        attract = Beta_zero*exp(-1*Gamma*dist*dist)
                    elif gene == 1: #距離の正規化をしない．距離をそのまま魅力に用いる．
                        for l in range(0,NUM_OF_VARI):
                            dist += (ind[i][l] - ind[j][l])*(ind[i][l] - ind[j][l])

                        dist = math.sqrt(dist)
#                       print(i, '番目の個体', "\t",j, '番目の個体',"\t",'距離の値',dist,end = '\n',file=move) # 個体のiと個体jの距離
                        attract = Beta_zero*exp(-1*Gamma*dist) #distをルートrに設定
                    elif gene == 2: #距離の正規化をする．距離の2乗を魅力に用いる．
                        for l in range(0,NUM_OF_VARI):
                            dist1 = (ind[i][l]-Lower_Bound)/(Upper_Bound-Lower_Bound)
                            dist2 = (ind[j][l]-Lower_Bound)/(Upper_Bound-Lower_Bound)
                            dist += (dist1 - dist2)**2
#                           print(dist1, 'dist1の値', "\t",dist2, 'dist2の値',"\t",end = '\n',file=move) # 正規化した値の出力


                        dist = math.sqrt(dist)
#                       print(i, '番目の個体', "\t",j, '番目の個体',"\t",'距離の値',dist,end = '\n',file=move) # 個体のiと個体jの距離

                        attract = Beta_zero*exp(-1*Gamma*dist*dist)
                        #attract = Beta_zero*exp(-1*Gamma*dist) #distをルートrに設定


#                   print('魅力の値', "\t",attract,end = '\n',file=move) # 個体のiと個体jに関する魅力の値
                    rand = random.random()
#                   print('ランダムに移動させる方向を決めるの値', "\t",rand,end = '\n',file=move) 

                    if rand >= Alpha_sel:
#                       print('多軸での移動', end = '\n',file=move) 

                        for l in range(0,NUM_OF_VARI):
                            rand = random.uniform(-0.5,0.5)*(Upper_Bound - Lower_Bound) 
#                           print('近傍へのランダム移動の乱数',rand,'第3項',Alpha*rand,end = '\n',file=move) # 第3項の値

                            kari_a_m_ind[l] = ind[i][l] + attract * (ind[j][l] - ind[i][l]) + Alpha*rand
                            if kari_a_m_ind[l] < Lower_Bound:
                                kari_a_m_ind[l] = Lower_Bound
                            elif kari_a_m_ind[l] > Upper_Bound:
                                kari_a_m_ind[l] = Upper_Bound
                    else:
#                       print('一軸での移動', end = '\n',file=move) 
                        rand=random.uniform(0,NUM_OF_VARI)
#                       print('軸の決定用乱数', "\t",rand,end = '\n',file=move) 
                        individual_num = int(rand)
#                       print('決定した軸番号', "\t",individual_num,end = '\n',file=move) 
                        for l in range(0,NUM_OF_VARI):
                            if l == individual_num:
                                rand = random.uniform(-0.5,0.5)*(Upper_Bound - Lower_Bound) 
#                               print('近傍へのランダム移動の乱数',rand,'第3項',Alpha*rand,end = '\n',file=move) # 第3項の値
                            else:
                                rand=0
#                               print('移動対象以外の軸の乱数',rand,'第3項',Alpha*rand,end = '\n',file=move) # 第3項の値

                            kari_a_m_ind[l] = ind[i][l] + attract * (ind[j][l] - ind[i][l]) + Alpha*rand
                            if kari_a_m_ind[l] < Lower_Bound:
                                kari_a_m_ind[l] = Lower_Bound
                            elif kari_a_m_ind[l] > Upper_Bound:
                                kari_a_m_ind[l] = Upper_Bound

                    # 更新されたiの位置
#                   print('更新された個体iの位置', end = '\n',file = move)    
#                   for l in range(0,NUM_OF_VARI):
#                       print(kari_a_m_ind[l],end = '\t',file = move)
#                   print('\n',file=move)    

                    # 目的関数値の確認 (関数ごとにここを変更する) 23年9月27日書き換え
                    kari_f_eval=0
                    for k in range(NUM_OF_OFJ):
                        fuz_Obj[k] = 0

                    r_cons = [" " for l in range(NUM_CONS)] #制約右辺値の確認用配列
                    # 実行可能解を格納するための配列
                    Real_x = ['' for l in range(NUM_OF_VARI)]

            	    #実行可能解の導出
                    A = numpy.argsort(kari_a_m_ind)

                    for k in range(NUM_CONS):
                        r_cons[k] = 0

                    for k in range(NUM_OF_VARI):
                        cons_flag = 0
                        for m in range(NUM_CONS):
                            r_cons[m] += Cons_A[m][A[k]]
                            if r_cons[m] > Cons_b[m]:
                                cons_flag = 1
                        if cons_flag == 1:
                            Real_x[A[k]] = 0
                            for m in range(NUM_CONS):
                                r_cons[m] -= Cons_A[m][A[k]]
                        else:
                            Real_x[A[k]] = 1

                    #Real_xの出力
                    #print('Real_x(move)',"\n",file = move)
                    #print('individual',i,"\n",file = move)
                    #for k in range(NUM_OF_VARI):
                    #    print(Real_x[k], end = "\t",file = move)
                    #print('\n',file = move)

                    #目的関数値の算出
                    for k in range(NUM_OF_VARI):
                        if  Real_x[k] == 1:
                            for l in range(NUM_OF_OFJ):
                                fuz_Obj[l] += Obj[l][k] #ここを改良 Obj[]を2次元配列化

                    #目的関数値の出力
                    #print('Objの値',"\n",file = move)
                    #for k in range(NUM_OF_OFJ):
                    #    print(fuz_Obj[k], end = "\t",file = move)
                    #print('\n',file = move)
                    
                    #ファジイ目標を入れて正規化
                    for k in range(NUM_OF_OFJ):
                        fuz_Obj[k] = (fuz_Obj[k]-fuz_obj_min[k])/(fuz_obj_max[k]-fuz_obj_min[k]) 

                    #ファジイ目標導入後の目的関数値の出力
                    #print('fuz_objの値',"\n",file = move)
                    #for k in range(NUM_OF_OFJ):
                    #    print(fuz_Obj[k], end = "\t",file = move)
                    #print('\n',file = move)

                    #正規化された値の中の最小値を導出し，fun_evalに値を渡す．
                    for k in range(NUM_OF_OFJ):
                        if k == 0:
                           kari_f_eval = fuz_Obj[k]
                        else:
                           if kari_f_eval > fuz_Obj[k]:
                              kari_f_eval = fuz_Obj[k]

                    #ファジィ目標導入後の目的関数値の出力
                    #print('最大化決定後のkari_f_evalの値',"\n",file = move)
                    #print(kari_f_eval, end = "\n",file = move)


                    # 更新された目的関数値
#                   print('flag-1', end = '\n',file = move)
#                   print('自分自身を更新した個体iの目的関数値', end = '\n',file = move)    
#                   print(kari_f_eval,end = '\n',file = move)
#                   print('更新された個体iの位置', end = '\n',file = move)    
#                   for l in range(0,NUM_OF_VARI):
#                       print(kari_a_m_ind[l],end = '\t',file = move)
#                   print('\n',file=move)
#                   for k in range(NUM_OF_VARI):
#                       print(Real_x[k], end = "\t",file = move)
#                   print('\n',file = move)    #23年9月27日書き換え おわり

                    if best_next_ind == 0:
                        first_next_ind = 1
                        if kari_f_eval > fun_eval[i]: #23年9月27日書き換え
                            best_next_ind = 1
                            new_f_eval = kari_f_eval
                        
                            for l in range(0,NUM_OF_VARI):
                                a_m_ind[i][l] = kari_a_m_ind[l]
#                           print('更新\n',file=move)
#                           print('更新された個体iの目的関数値', end = '\n',file = move)    
#                           print(kari_f_eval,end = '\n',file = move)
                        # 更新されたiの位置
#                           print('更新された個体iの位置', end = '\n',file = move)    
#                           for l in range(0,NUM_OF_VARI):
#                               print(a_m_ind[i][l],end = '\t',file = move)
#                           print('\n',file=move)
                    else:
                        if kari_f_eval > new_f_eval: #23年9月27日書き換え
                            new_f_eval = kari_f_eval

                            for l in range(0,NUM_OF_VARI):
                                a_m_ind[i][l] = kari_a_m_ind[l]
#                           print('更新\n',file=move)
#                           print('更新された個体iの目的関数値', end = '\n',file = move)    
#                           print(kari_f_eval,end = '\n',file = move)
                            # 更新されたiの位置
#                           print('更新された個体iの位置', end = '\n',file = move)    
#                           for l in range(0,NUM_OF_VARI):
#                               print(a_m_ind[i][l],end = '\t',file = move)
#                           print('\n',file=move)

        if best_next_ind == 0:
            if first_next_ind == 0:
#               print('掛け合わせが行われなかった個体', i, end = '\n',file = move)    

                rand = random.random()
#               print('ランダムに移動させる方向を決めるの値', "\t",rand,end = '\n',file=move) 

                if rand >= Alpha_sel:
#                   print('多軸での移動', end = '\n',file=move) 
                    for l in range(0,NUM_OF_VARI):
                        rand = random.uniform(-0.5,0.5)*(Upper_Bound - Lower_Bound)
#                       print('近傍へのランダム移動の乱数',rand,'第3項',Alpha*rand,end = '\n',file=move) # 第3項の値
                        kari_a_m_ind[l] = ind[i][l] + Alpha*rand
                        if kari_a_m_ind[l] < Lower_Bound:
                            kari_a_m_ind[l] = Lower_Bound
                        elif kari_a_m_ind[l] > Upper_Bound:
                            kari_a_m_ind[l] = Upper_Bound
                else:
#                   print('一軸での移動', end = '\n',file=move) 
                    rand=random.uniform(0,NUM_OF_VARI)
#                   print('軸の決定用乱数', "\t",rand,end = '\n',file=move) 
                    individual_num = int(rand)
#                   print('決定した軸番号', "\t",individual_num,end = '\n',file=move) 
                    for l in range(0,NUM_OF_VARI):
                        if l == individual_num:
                            rand = random.uniform(-0.5,0.5)*(Upper_Bound - Lower_Bound) 
#                           print('近傍へのランダム移動の乱数',rand,'第3項',Alpha*rand,end = '\n',file=move) # 第3項の値
                        else:
                            rand=0
#                           print('移動対象以外の軸の乱数',rand,'第3項',Alpha*rand,end = '\n',file=move) # 第3項の値

                        kari_a_m_ind[l] = ind[i][l] + Alpha*rand
                        if kari_a_m_ind[l] < Lower_Bound:
                            kari_a_m_ind[l] = Lower_Bound
                        elif kari_a_m_ind[l] > Upper_Bound:
                            kari_a_m_ind[l] = Upper_Bound

                # 更新されたiの位置
#               print('更新された個体iの位置', end = '\n',file = move)    
#               for l in range(0,NUM_OF_VARI):
#                   print(kari_a_m_ind[l],end = '\t',file = move)
#               print('\n',file=move)    

                # 目的関数値の確認 (関数ごとにここを変更する) 23年9月27日書き換え
                kari_f_eval=0
                for k in range(NUM_OF_OFJ):
                    fuz_Obj[k] = 0

                r_cons = [" " for l in range(NUM_CONS)] #制約右辺値の確認用配列
                # 実行可能解を格納するための配列
                Real_x = ['' for l in range(NUM_OF_VARI)]

            	#実行可能解の導出
                A = numpy.argsort(kari_a_m_ind)

                for k in range(NUM_CONS):
                    r_cons[k] = 0

                for k in range(NUM_OF_VARI):
                    cons_flag = 0
                    for m in range(NUM_CONS):
                        r_cons[m] += Cons_A[m][A[k]]
                        if r_cons[m] > Cons_b[m]:
                           cons_flag = 1
                    if cons_flag == 1:
                        Real_x[A[k]] = 0
                        for m in range(NUM_CONS):
                            r_cons[m] -= Cons_A[m][A[k]]
                    else:
                        Real_x[A[k]] = 1

                #Real_xの出力
                #print('Real_x-type2',"\n",file = move)
                #print('individual',i,"\n",file = move)
                #for k in range(NUM_OF_VARI):
                #    print(Real_x[k], end = "\t",file = move)
                #print('\n',file = move)

                #目的関数値の算出
                for k in range(NUM_OF_VARI):
                    if  Real_x[k] == 1:
                        for l in range(NUM_OF_OFJ):
                            fuz_Obj[l] += Obj[l][k] #ここを改良 Obj[]を2次元配列化

                #目的関数値の出力
                #print('目的関数値の出力',"\n",file = move)
                #for k in range(NUM_OF_OFJ):
                #    print(fuz_Obj[k], end = "\t",file = move)
                #print('\n',file = move)

                #ファジイ目標を入れて正規化
                for k in range(NUM_OF_OFJ):
                    fuz_Obj[k] = (fuz_Obj[k]-fuz_obj_min[k])/(fuz_obj_max[k]-fuz_obj_min[k]) 

                #ファジイ目標導入後の目的関数値の出力
                #print('fuz_objの値',"\n",file = move)
                #for k in range(NUM_OF_OFJ):
                #    print(fuz_Obj[k], end = "\t",file = move)
                #print('\n',file = move)


                #正規化された値の中の最小値を導出し，fun_evalに値を渡す．
                for k in range(NUM_OF_OFJ):
                    if k == 0:
                       kari_f_eval = fuz_Obj[k]
                    else:
                       if kari_f_eval > fuz_Obj[k]:
                          kari_f_eval = fuz_Obj[k]
                
                #ファジィ目標導入後の目的関数値の出力
                #print('最大化決定後のkari_f_evalの値',"\n",file = move)
                #print(kari_f_eval, end = "\n",file = move)

                # 更新された目的関数値
#               print('flag-2', end = '\n',file = move)
#               print('自分自身を更新した個体iの目的関数値', end = '\n',file = move)    
#               print(kari_f_eval,end = '\n',file = move)
#               print('更新された個体iの位置', end = '\n',file = move)    
#               for l in range(0,NUM_OF_VARI):
#                   print(kari_a_m_ind[l],end = '\t',file = move)
#               print('\n',file=move)
#               for k in range(NUM_OF_VARI):
#                   print(Real_x[k], end = "\t",file = move)
#               print('\n',file = move)    #23年9月27日書き換え おわり

                if kari_f_eval > fun_eval[i]: #23年9月27日書き換え
                    kari_fun_eval[i] = kari_f_eval
                    for l in range(0,NUM_OF_VARI):
                        a_m_ind[i][l] = kari_a_m_ind[l]
                else:
                    kari_fun_eval[i] = fun_eval[i]
                    for l in range(0,NUM_OF_VARI):
                        a_m_ind[i][l] = ind[i][l]
            else:
#               print('掛け合わたけれど更新されなかった個体', i, end = '\n',file = move)    
                kari_fun_eval[i] = fun_eval[i]
                for l in range(0,NUM_OF_VARI):
                    a_m_ind[i][l] = ind[i][l]
        else:
            kari_fun_eval[i] = new_f_eval

    # moveした後の個体と評価値をindとfun_evalにコピー
    for i in range(0,POP_SIZE):
        fun_eval[i] = kari_fun_eval[i]
        for j in range (NUM_OF_VARI):
            ind[i][j] = a_m_ind[i][j]

#   print('move終了後の個体', end = '\n',file = move)    
#   for i in range(0,POP_SIZE):
#       for j in range(0,NUM_OF_VARI):
#           print(ind[i][j],end = '\t',file = move)
#       print('\n',file=move)

#    print('move終了後の個体評価値', end = '\n',file = move)    
#    for i in range(0,POP_SIZE):
#        print('individual',i,"\t",fun_eval[i],end = '\n',file = move)
#    print('\n',file=move)


    # 反復ごとの目的関数の最良値・最悪値・平均値の算出
    ite_max = max(fun_eval)
    ite_min = min(fun_eval)
    ite_ave = statistics.mean(fun_eval)

    # 出力は別ファイルに行う
    print('世代',sedai, '\t', ite_min, '\t', ite_max,'\t', ite_ave, end = '\n',file = ite_obj)    

    # 最良値が更新された場合は値を更新
    if ite_max > best_obj_v[0]: #23年9月27日書き換え
        max_index = fun_eval.index(ite_max) #23年9月27日書き換え
        best_obj_v[0] = ite_max #23年9月27日書き換え
        best_ite[0] = sedai
        for j in range (NUM_OF_VARI):
            best_ind[j] = ind[max_index][j] #23年9月27日書き換え


    move.close()
    ite_obj.close()


