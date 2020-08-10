#Dataset
chros       = [15]
steps       = [21]
reps        = [1,2]
missings    = [2,4,6,8]

#Training Hyper Parameters
etas=[1000]
#alphas=[0.6, 0.7]
alphas=[0.6]
#lrs=[.00001, 0.001]
lrs=[.0001]

#Other Hyper Params
struc_names=["ipsc_missing_"]
ress=[50000]
epochs=[400]
ipsc_res=[50000]

rule all:
	input:
		expand("Config/Datasets/ipsc_missing_{missing}_chro_{chro}_rep_{rep}_step_{step}.json",
			missing=missings,
			chro=chros,
			rep=reps,
			step=steps),

		expand("Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epochs}.json",
			eta=etas,
			alpha=alphas,
			lr=lrs,
			epochs=epochs),

		expand("Generated_Structures/ipsc_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy",
			missing=missings,
			eta=etas,
			alpha=alphas,
			lr=lrs,
			epoch=epochs,
			step=steps,
			chro=chros,
			rep=reps,
			res=ipsc_res),

		#Generate iPSC gifs
		expand("Gifs/ipsc_missing/missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif",
			missing=missings,
			rep=reps,
			eta=etas,
			alpha=alphas,
			lr=lrs,
			epoch=epochs,
			res=ipsc_res,
			step=steps,
			chro=chros)

rule build_missing_ipsc_configs:
	output:
		name="Config/Datasets/ipsc_missing_{missing}_chro_{chro}_rep_{rep}_step_{step}.json"
	shell:
		"python Python_Scripts/make_ipsc_missing.py {output.name} {wildcards.step} {wildcards.chro} {wildcards.rep} {wildcards.missing}" 

rule build_hyper_param_configs:
	output:
		name="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epochs}.json"
	shell:
		"python Python_Scripts/make_hyper_param_config.py {output.name} {wildcards.eta} {wildcards.alpha} {wildcards.lr} {wildcards.epochs}"

rule run4D_missing:
	input:
		dataset="Config/Datasets/ipsc_missing_{missing}_chro_{chro}_rep_{rep}_step_{step}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/ipsc_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"

rule build_psc_missing_images:
	input:
		npfile="Generated_Structures/ipsc_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	output:
		outfig="Gifs/ipsc_missing/missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "
