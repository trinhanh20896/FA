9#FireFly Algorithm
import random
import init_ind_module
import result_ind_module
import eval_module
import move_module
import time

random.seed(10) #乱数のシードを8に設定

POP_SIZE = 30 #個体群サイズ
R_POP_SIZE = 15 #掛け合わせをする個体の数
R_POP_SEL = 0 #掛け合わせをする個体の選出方法 0: 良いものからR_POP_SIZE個 1: ランダムにR_POP_SIZE個 2: 良いものからR_P_S個, ランダムにP_POP_SIZE-R_PS個
R_P_S = 0 # R_POP_SEL =2 の時のみ使用 関数評価値の良いものからR_P_S個選択
NUM_OF_VARI = 90 #変数の数
NUM_CONS = 5 #制約式の数 (23年9月追加)
NUM_OF_OFJ = 3 #目的関数の数 (23年12月追加)
Lower_Bound = -10 #変数の下限値
Upper_Bound = 10 #変数の上限値
ITE_COUNT = 1000 #打ち切り世代数
gene = 0 #更新時の距離の正規化を行うかどうかを表すフラグ 0:実施しない(距離2乗使用)，1:実施しない(距離1乗使用), 2:実施
Alpha_sel = 0 #単一軸の方向に移動させるか, 複数の軸に移動させるかを決める確率：設定値は複数軸に移動させる場合の確率
Gamma = 0.6 #光の吸収係数
Beta_zero = 1 #発光地点における誘引度を表す定数
Alpha = 0.6 #ランダム性パラメータ
Theta = 0.999 #ランダム性の減少要素 (アルファ)


best_obj_v = [0] #最良の目的関数値
best_ite = [0] #最良の目的関数値を得た世代を記憶するための変数

f=open('result.txt','a')
bs=open('best_solution.txt','a') #'a'の方が良いか検討する．
bg=open('get_best_solution.txt','a') #'a'の方が良いか検討する．
tm = open('processing_time.txt','a')
bao = open('value_of_x.txt','a')

start = time.process_time() #計測開始

# 初期個体群の形成
ind = [['' for i in range(NUM_OF_VARI)] for j in range(POP_SIZE)]

init_ind_module.initial_individual(POP_SIZE,NUM_OF_VARI,ind,Lower_Bound,Upper_Bound)

#print('初期個体群発生後の個体',end = '\n',file = f)
#result_ind_module.result_individual(POP_SIZE,NUM_OF_VARI,ind)

# 各ホタルの評価値の算出
fun_eval = [" " for j in range(POP_SIZE)]

# 最も良いホタルの位置の値
best_ind = [" " for j in range(NUM_OF_VARI)]

# 最も良い実行可能解 (x) の値
best_Real_x = [" " for j in range(NUM_OF_VARI)]


#制約式の係数の入力 (23年9月追加 Cons_A貼り付け)
Cons_A = [
[10,60,27,82,62,53,41,90,84,77,25,87,73,56,37,11,18,42,23,24,98,50,20,10,10,44,57,61,64,64,24,69,50,41,15,64,80,82,56,37,88,75,96,93,58,22,51,31,87,28,80,85,99,99,65,45,33,36,85,12,43,18,70,15,10,92,34,34,62,72,85,75,53,28,76,52,51,95,76,19,63,44,76,64,61,42,23,30,48,82],
[56,99,77,41,25,69,54,15,72,55,23,95,22,91,72,37,48,16,96,71,23,88,83,62,27,26,83,52,23,55,75,46,35,61,71,78,74,52,21,43,85,13,56,69,48,19,95,92,59,41,52,43,86,38,51,34,98,36,76,61,27,78,85,45,55,90,12,99,61,14,57,27,85,66,69,27,85,21,19,76,38,94,35,40,22,75,85,73,64,77],
[32,23,10,15,82,86,28,20,59,11,20,50,77,71,58,16,49,28,72,36,49,30,62,57,66,24,55,96,72,93,27,40,26,99,51,99,18,66,18,49,93,14,90,36,30,79,46,28,66,64,50,51,63,67,86,84,66,74,60,43,26,76,59,91,31,27,64,72,62,41,54,17,76,65,65,72,82,23,61,88,92,65,75,13,70,97,38,61,37,25],
[19,88,86,76,23,39,17,16,67,83,59,50,46,36,51,55,23,39,76,38,84,96,88,75,37,94,21,15,80,57,64,96,16,88,68,38,19,55,30,36,92,59,69,20,54,44,54,81,55,44,71,57,64,45,10,73,19,66,87,54,77,54,44,80,59,42,96,66,25,43,21,76,95,65,12,39,15,67,21,86,87,63,74,86,11,21,73,65,29,15],
[25,66,40,38,43,69,82,82,57,64,81,91,23,66,46,32,22,86,15,48,61,37,59,30,38,19,82,22,35,80,90,81,76,65,42,87,30,87,30,32,58,98,14,17,57,48,18,33,90,30,23,21,93,17,14,15,40,92,45,48,95,85,58,85,72,45,33,10,57,95,45,31,62,32,71,95,49,90,10,94,64,80,61,22,30,44,10,47,17,69]
]
#制約式の右辺値の入力  (23年9月追加 Cons_b貼り付け)
Cons_b = [2591,2312,2578,2513,2433]
#目的関数の係数の入力  (23年9月追加+12月追加 Obj貼り付け)
Obj = [
[82,57,71,22,72,75,79,12,88,68,73,17,59,95,15,34,23,98,65,36,93,43,72,29,24,31,56,91,19,91,49,17,80,25,97,79,88,28,51,10,77,20,46,38,99,13,32,27,32,23,65,89,94,27,80,68,69,91,50,92,69,23,67,61,47,94,58,62,58,32,45,41,13,81,27,16,45,63,16,27,24,67,50,64,72,49,71,45,85,63],
[-22,58,-89,-55,-76,47,-67,-16,71,-68,-48,-77,57,35,82,-76,39,-99,23,-19,-66,-63,77,-93,77,-46,-24,72,44,59,-36,17,-99,-56,-52,21,-82,-89,22,-61,-74,-56,24,98,96,-76,89,-74,42,-73,-34,-87,42,-36,64,-83,-81,49,15,21,-16,47,-10,-13,-20,57,-60,-95,96,-61,-23,-23,10,11,83,-98,31,-91,62,-43,-41,-33,57,-32,67,-45,-75,20,91,92],
[-49,-43,-29,-69,-12,-57,-52,-94,-57,-62,-73,-42,-47,-87,-37,-13,-69,-73,-97,-87,-60,-17,-12,-75,-46,-37,-32,-61,-81,-75,-76,-91,-12,-77,-72,-75,-86,-87,-90,-25,-95,-44,-40,-49,-39,-27,-80,-29,-79,-29,-82,-62,-86,-70,-95,-12,-21,-89,-23,-69,-13,-58,-29,-57,-89,-17,-93,-15,-93,-40,-40,-34,-96,-80,-10,-46,-99,-43,-57,-51,-82,-80,-66,-86,-69,-38,-31,-97,-91,-96]
]
#ファジィ目標の入力  (23年12月追加 Obj貼り付け)
fuz_obj_max = [3388, 2044, 0]
fuz_obj_min = [0, -2932, -5252]
#print('制約左辺値の出力',end = '\n',file = f)
#for i in range(NUM_CONS):
#   for j in range(NUM_OF_VARI):
#      print(Cons_A[i][j],end = '\t',file = f)
#   print(end = '\n',file = f)

#print('目的関数の係数値の出力',end = '\n',file = f)
#for i in range(NUM_OF_OFJ):
#   for j in range(NUM_OF_VARI):
#      print(Obj[i][j],end = '\t',file = f)
#   print(end = '\n',file = f)

#print('ファジィ目標の出力 z_1',end = '\n',file = f)
#for i in range(NUM_OF_OFJ):
#   print(fuz_obj_max[i],end = '\t',file = f)
#print(end = '\n',file = f)

#print('ファジィ目標の出力 z_0',end = '\n',file = f)
#for i in range(NUM_OF_OFJ):
#   print(fuz_obj_min[i],end = '\t',file = f)
#print(end = '\n',file = f)

eval_module.eval_individual(POP_SIZE,NUM_OF_VARI,ind,fun_eval,best_obj_v,best_ite,best_ind, gene, NUM_CONS, Cons_A, Cons_b, best_Real_x,Obj,fuz_obj_max,fuz_obj_min,NUM_OF_OFJ)

for l in range(ITE_COUNT): #Fireflyの世代開始

   Alpha *= Theta #追加220824

   move_module.move_individual(POP_SIZE,NUM_OF_VARI,ind,fun_eval,Alpha,Beta_zero,Gamma,best_obj_v,best_ite,l,best_ind,Upper_Bound,Lower_Bound, gene, R_POP_SIZE,R_POP_SEL,R_P_S,Alpha_sel,NUM_CONS,Cons_A,Cons_b,Obj,fuz_obj_max,fuz_obj_min,NUM_OF_OFJ)

end = time.process_time() #計測終了

print('最良値の値',best_obj_v[0],end = '\n',file = bs)
print('最良値の得られた世代',best_ite[0],end = '\n',file = bg)
print('近似最良解を与える個体',end = '\n',file = bao)
for j in range (NUM_OF_VARI):
   print(best_ind[j],end = '\t',file = bao)
print('\n',file=bao)
print('近似最良解',end = '\n',file = bao)
for j in range (NUM_OF_VARI):
   print(best_Real_x[j],end = '\t',file = bao)
print('\n',file=bao)

print('近似最適解',best_obj_v[0],file = f)
print('近似最適解が得られた世代　',best_ite[0],file = f)
print('処理時間', end-start, file = tm)

f.close()
bs.close()
bg.close()
tm.close()
bao.close()
