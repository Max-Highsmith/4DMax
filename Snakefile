#Dataset
chros       = [19]
steps       = [21]
reps        = [1]

#Training Hyper Parameters
etas=[1000]
#alphas=[0.6, 0.7]
alphas=[0.6]
#lrs=[.00001, 0.001]
lrs=[.0001]

#Other Hyper Params
struc_names=["iPluripotent"]
ress=[50000]
epochs=[400]

rule all:
	input:
		expand("Generated_Structures/{struc_name}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy",
			struc_name=struc_names,
			epoch=epochs,
			eta=etas,
			alpha=alphas,
			lr=lrs,
			res=ress,
			step=steps,
			chro=chros,
			rep=reps)

rule run4D:
	output:
		"Generated_Structures/{struc_name}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epochs}_res_{res}_step_{step}_chro_{chro}.npy"
	shell:
		"python 4dmax.py {wildcards.struc_name} {wildcards.eta} {wildcards.alpha} {wildcards.lr} {wildcards.epochs} {wildcards.res} {wildcards.step} {wildcards.chro} {wildcards.rep}"

