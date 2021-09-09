for eta in 1 1000 1000000
do
	for lr in 0.1 0.001 0.0001 0.00001
	do
		for alpha in 0.6 0.8 1
		do
			echo "{\"eta\": \"${eta}\", \"alpha\": \"${alpha}\", \"lr\": \"${lr}\", \"epoch\": \"100\"}" > temp_hyper.json
			python 4dmax.py tuning_dataset.json temp_hyper.json
		done
	done
done

