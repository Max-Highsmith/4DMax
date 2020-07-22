#convert -delay 90 -loop Image_Results/struc1/struc1_.png	

for j in 1 2
do
	tes=$(for i in $(seq 0 $1)
	do
		printf "Image_Results/struc${j}/$i.png\t"
	done) 
	convert -delay 30 -loop 0 $tes struc${j}.gif
done
