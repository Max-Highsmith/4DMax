4DMax is a tool for prediction of the 4dgenome conformation from a time-series Hi-C dataset

![alt text](https://github.com/Max-Highsmith/4DMax/blob/master/4DMax_Logo.png)


# 4DMax 

**1. Format your time series Hi-C data**\
*Each Hi-C experiment should be represented as a 3 column tab seperated text file where (pos1, pos2, val)*\
**2. Build dataset and hyper parameters configuration files**\
examples shown in:
1. Config/Datasets/example.json
2. Config/Hyper_Params/example.json

	*Hyper Params*	
	- eta: weight of movement loss
	- alpha: contact map to distance constraint conversion ratio IF=d^alpha
	- lr: learning rate
	- epoch: number of epochs to train


	*Data Set*
	- name: genomic Process name
	- step: granularity of 4D Model
	- chro: chromosome number
	- rep: biological replicate number
	- taos: indx of hi-c experiments in time process
	- datasets: hi-c experiment text files

**3. Run 4DMax**
	'python 4dmax.py {input.dataset} {input.param}'
	
**4    View Strucutes**
	'python Python_Scripts/create_gif.py {output.outfig} {input.npfile}

# Reproduce white paper experiments.
1.  Download needed Hi-C files Cardiomyocyte GSE106690 iPSC GSE96611
2.  Generate modes
	'snakemake'
3. Generate TADS
	'cd TADS;
	snakemake --use-conda
	'
4. Generate AB Compartments:
	'cd AB;
	snakemake'
	
#To run on your own data
