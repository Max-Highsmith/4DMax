#eta
#alpha
eta=1000
alpha=0.6
lr=0.0001
epochs=2
res=50000
struc_name="Generated_Structures/PSC_Test"_${epochs}
python 4dmax.py $eta $alpha $lr $epochs $res ${struc_name}
