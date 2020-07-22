num=$1
dirr=$2
gif=$3
echo $gif
echo $dirr
tes=$(for i in $(seq 0 $num)
do
	printf "${dirr}/${i}.png "
done)
convert -delay 10 -loop 0 $tes $gif
