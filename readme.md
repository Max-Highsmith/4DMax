4DMax is a tool for prediction of the 4dgenome conformation from a time-series Hi-C dataset

![alt text](https://github.com/Max-Highsmith/4DMax/blob/master/4DMax_Logo.png)


# Use 4DMax.
##1.  Format your time series Hi-C data

##2.  Build dataset and hyper parameters configuration files
	examples shown in:
		Config/Datasets/example.json
		Config/Hyper_Params/example.json
	
##3    Run 4DMax
	'python 4dmax.py {input.dataset} {input.param}'
	
##4    View Strucutes
	'python Python_Scripts/create_gif.py {output.outfig} {input.npfile}

#Reproduce white paper experiments.
1.  download the needed files using getDatasetScripts.py #TODO #TODO

#To run on your own data
