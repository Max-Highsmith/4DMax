#Dataset
#chros       = [10,11,12,13,14,15,16,17,18,19,20,21]
chros       = [9]
steps       = [21]
reps        = [1]
#missings    = [2,4,6,8]
#missings    = [2,4,6,8]
missings     = []


#adipose dataset
adipose_chros=[10]
adipose_reps=[1]
adipose_etas=[100]
adipose_alphas=[0.7]
adipose_lrs=[0.00001]
adipose_epochs=[4000]


#cardio dataset
cardio_chros=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
#cardio_chros=[10]
cardio_steps=[15,29,43,57,71]
#cardio_steps=[15]
cardio_reps=[1]
#cardio hyper
cardio_etas  =[1000]
#cardio_alphas=[0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
cardio_alphas=[0.6]
cardio_lrs   =[0.0001]
cardio_epochs=[400]
cardio_missing=[2]


#ipsc 10-19
#Training Hyper Parameters
#etas=[1000]
#alphas=[0.6]
#lrs=[.0001]
#comp_reps=5

etas   =[1000]
alphas =[0.6]
lrs    =[0.00001]

#Other Hyper Params
ress=[50000]
epochs=[1000]
ipsc_res=[50000]
ipsc_small_res=[500000]


######
### IPSC  dataset
#####
#ipsc_chros = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,'X']
ipsc_chros  = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
#ipsc_steps = [11,31,41,51]
ipsc_steps = [21]
ipsc_reps  = [1]

#IPSC hyper
ipsc_etas   = [1000]
ipsc_alphas = [0.6]
ipsc_lrs    = [0.0001]
ipsc_res    = [50000]
ipsc_epochs = [400]

#synthetic
synthetic_reps   = [1,2]
synthetic_etas   = [10]
synthetic_alphas = [1.0]
synthetic_lrs    = [.01]
synthetic_epochs = [1000]
synthetic_missing = [1,2,3,4]

rule all:
	input:
		expand("Gifs/cardio_chros/cardio_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_{step}_chro_{chro}.gif",
			step=cardio_steps,
			rep=cardio_reps,
			eta=cardio_etas,
			alpha=cardio_alphas,
			lr=cardio_lrs,
			epoch=cardio_epochs,
			chro=cardio_chros),

		expand("Gifs/cardio_chros/cardio_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_15_chro_{chro}.gif",
			missing=cardio_missing,
			rep=cardio_reps,
			eta=cardio_etas,
			alpha=cardio_alphas,
			lr=cardio_lrs,
			epoch=cardio_epochs,
			chro=cardio_chros),

		expand("Gifs/adipose_chros/adipose_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_50000_step_7_chro_{chro}.gif",
			rep=adipose_reps,
			eta=adipose_etas,
			alpha=adipose_alphas,
			lr=adipose_lrs,
			epoch=adipose_epochs,
			chro=adipose_chros),

		expand("Generated_Structures/cardio_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_15_chro_{chro}.npy",
			rep=cardio_reps,
			eta=cardio_etas,
			alpha=cardio_alphas,
			lr=cardio_lrs,
			epoch=cardio_epochs,
			chro=cardio_chros),

		
		expand("Generated_Structures/adipose_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_50000_step_7_chro_{chro}.npy",
			rep=adipose_reps,
			eta=adipose_etas,
			alpha=adipose_alphas,
			lr=adipose_lrs,
			epoch=adipose_epochs,
			chro=adipose_chros),

		expand("Config/Datasets/cardio_full_chro_{chro}_rep_{rep}_step_{step}.json",
			step=cardio_steps,
			chro=cardio_chros,
			rep=cardio_reps),
	
		expand("Generated_Structures/cardio_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_15_chro_{chro}.npy",
			missing=cardio_missing,
			rep=cardio_reps,
			eta=cardio_etas,
			alpha=cardio_alphas,
			lr=cardio_lrs,
			epoch=cardio_epochs,
			chro=cardio_chros),

		expand("Config/Datasets/cardio_missing_{missing}_chro_{chro}_rep_{rep}.json",
			chro=cardio_chros,
			rep=cardio_reps,
			missing=cardio_missing),

		expand("Config/Datasets/synthetic_both_missing_rep_{rep}.json",
			rep=synthetic_reps),

		expand("Config/Datasets/synthetic_missing_{missing}_rep_{rep}.json",
			missing=synthetic_missing,
			rep=synthetic_reps),
		expand("Config/Datasets/synthetic_rep_{rep}.json",
			rep=synthetic_reps),

		expand("Config/Datasets/adipose_full_chro_{chro}_rep_{rep}.json",
			chro=adipose_chros,
			rep=adipose_reps),

		expand("Config/Datasets/ipsc_missing_{missing}_chro_{chro}_rep_{rep}_step_{step}.json",
			missing=missings,
			chro=ipsc_chros,
			rep=ipsc_reps,
			step=ipsc_steps),

		expand("Config/Datasets/ipsc_full_chro_{chro}_rep_{rep}_step_{step}.json",
			chro=ipsc_chros,
			rep=ipsc_reps,
			step=ipsc_steps),

		expand("Config/Datasets/ipsc_small_chro_{chro}_rep_{rep}_step_{step}.json",
			chro=ipsc_chros,
			rep=ipsc_reps,
			step=ipsc_steps),

		expand("Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epochs}.json",
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epochs=ipsc_epochs),


		expand("Generated_Structures/synthetic_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy",
			eta=synthetic_etas,
			alpha=synthetic_alphas,
			lr=synthetic_lrs,
			epoch=synthetic_epochs,
			rep=synthetic_reps),
	
		expand("Generated_Structures/synthetic_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy",
			missing=synthetic_missing,
			eta=synthetic_etas,
			alpha=synthetic_alphas,
			lr=synthetic_lrs,
			epoch=synthetic_epochs,
			rep=synthetic_reps),

		expand("Generated_Structures/synthetic_both_missing_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy",
			eta=synthetic_etas,
			alpha=synthetic_alphas,
			lr=synthetic_lrs,
			epoch=synthetic_epochs,
			rep=synthetic_reps),

		expand("Generated_Structures/ipsc_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy",
			missing=missings,
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epoch=ipsc_epochs,
			step=ipsc_steps,
			chro=ipsc_chros,
			rep=ipsc_reps,
			res=ipsc_res),

		expand("Generated_Structures/ipsc_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy",
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epoch=ipsc_epochs,
			step=ipsc_steps,
			chro=ipsc_chros,
			rep=ipsc_reps,
			res=ipsc_res),

		expand("Generated_Structures/ipsc_small_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy",
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epoch=ipsc_epochs,
			step=ipsc_steps,
			chro=ipsc_chros,
			rep=ipsc_reps,
			res=ipsc_small_res),



		expand("Gifs/synthetic/synthetic_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.gif",
			missing=synthetic_missing,
			rep=synthetic_reps,
			eta=synthetic_etas,
			alpha=synthetic_alphas,
			lr=synthetic_lrs,
			epoch=synthetic_epochs),

		expand("Gifs/synthetic/synthetic_both_missing_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.gif",
			rep=synthetic_reps,
			eta=synthetic_etas,
			alpha=synthetic_alphas,
			lr=synthetic_lrs,
			epoch=synthetic_epochs),



		expand("Gifs/synthetic/synthetic_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.gif",
			rep=synthetic_reps,
			eta=synthetic_etas,
			alpha=synthetic_alphas,
			lr=synthetic_lrs,
			epoch=synthetic_epochs),

		#Generate iPSC gifs
		expand("Gifs/ipsc_missing/missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif",
			missing=missings,
			rep=ipsc_reps,
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epoch=ipsc_epochs,
			res=ipsc_res,
			step=ipsc_steps,
			chro=ipsc_chros),

		#Generate iPSC gifs
		expand("Gifs/ipsc_full/ipsc_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif",
			rep=ipsc_reps,
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epoch=ipsc_epochs,
			res=ipsc_res,
			step=ipsc_steps,
			chro=ipsc_chros),

		expand("Gifs/ipsc_small/ipsc_small_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif",
			rep=ipsc_reps,
			eta=ipsc_etas,
			alpha=ipsc_alphas,
			lr=ipsc_lrs,
			epoch=ipsc_epochs,
			res=ipsc_small_res,
			step=ipsc_steps,
			chro=ipsc_chros)


rule build_synthetic_both_missing_chro_configs:
	output:
		name="Config/Datasets/synthetic_both_missing_rep_{rep}.json"
	shell:
		"python Python_Scripts/make_synthetic_missing_both.py {output.name} {wildcards.rep}"



rule build_synthetic_missing_chro_configs:
	output:
		name="Config/Datasets/synthetic_missing_{missing}_rep_{rep}.json"
	shell:
		"python Python_Scripts/make_synthetic_missing.py {output.name} {wildcards.rep} {wildcards.missing}"


rule build_synthetic_chro_configs:
	output:
		name="Config/Datasets/synthetic_rep_{rep}.json"
	shell:
		"python Python_Scripts/make_synthetic_full.py {output.name} {wildcards.rep}"

rule build_cardio_chro_configs:
	output:
		name="Config/Datasets/cardio_full_chro_{chro}_rep_{rep}_step_{step}.json"
	shell:
		"python Python_Scripts/make_cardio_chro.py {output.name} {wildcards.rep} {wildcards.chro} {wildcards.step}"

rule build_cardio_missing_configs:
	output:
		name="Config/Datasets/cardio_missing_{missing}_chro_{chro}_rep_{rep}.json"
	shell:
		"python Python_Scripts/make_cardio_missing.py {output.name} {wildcards.rep} {wildcards.chro} {wildcards.missing}"



rule build_adipose_chro_configs:
	output:
		name="Config/Datasets/adipose_full_chro_{chro}_rep_{rep}.json"
	shell:
		"python Python_Scripts/make_adipose_full.py {output.name} {wildcards.rep} {wildcards.chro}"



rule build_full_ipsc_configs:
	output:
		name="Config/Datasets/ipsc_full_chro_{chro}_rep_{rep}_step_{step}.json"
	shell:
		"python Python_Scripts/make_ipsc_full.py {output.name} {wildcards.step} {wildcards.chro} {wildcards.rep}"

rule build_full_small_ipsc_configs:
	output:
		name="Config/Datasets/ipsc_small_chro_{chro}_rep_{rep}_step_{step}.json"
	shell:
		"python Python_Scripts/make_ipsc_low_res.py {output.name} {wildcards.step} {wildcards.chro} {wildcards.rep}"




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


rule run4D_synthetic_missing_both:
	input:
		dataset="Config/Datasets/synthetic_missing_{missing}_rep_{rep}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/synthetic_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"



rule run4D_synthetic_missing:
	input:
		dataset="Config/Datasets/synthetic_both_missing_rep_{rep}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/synthetic_both_missing_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"




rule run4D_synthetic:
	input:
		dataset="Config/Datasets/synthetic_rep_{rep}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/synthetic_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"


rule run4D_cardio:
	input:
		dataset="Config/Datasets/cardio_full_chro_{chro}_rep_{rep}_step_{step}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/cardio_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_{step}_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"

rule run4D_cardio_missing:
	input:
		dataset="Config/Datasets/cardio_missing_{missing}_chro_{chro}_rep_{rep}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/cardio_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_15_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"

rule run4D_adipose:
	input:
		dataset="Config/Datasets/adipose_full_chro_{chro}_rep_{rep}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/adipose_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_50000_step_7_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"



rule run4D_missing:
	input:
		dataset="Config/Datasets/ipsc_missing_{missing}_chro_{chro}_rep_{rep}_step_{step}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/ipsc_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"

rule run4D_full:
	input:
		dataset="Config/Datasets/ipsc_full_chro_{chro}_rep_{rep}_step_{step}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/ipsc_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"

rule run4D_ipsc_small:
	input:
		dataset="Config/Datasets/ipsc_small_chro_{chro}_rep_{rep}_step_{step}.json",
		param="Config/Hyper_Params/4dmax_eta_{eta}_alpha_{alpha}_lr_{lr}_epochs_{epoch}.json"
	output:
		"Generated_Structures/ipsc_small_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	shell:
		"python 4dmax.py {input.dataset} {input.param}"






rule build_psc_missing_images:
	input:
		npfile="Generated_Structures/ipsc_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	output:
		outfig="Gifs/ipsc_missing/missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "

rule build_synthetic_missing_images:
	input:
		npfile="Generated_Structures/synthetic_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy"
	output:
		outfig="Gifs/synthetic/synthetic_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "

rule build_synthetic_missing_both_images:
	input:
		npfile="Generated_Structures/synthetic_both_missing_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy"
	output:
		outfig="Gifs/synthetic/synthetic_both_missing_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "




rule build_synthetic_full_images:
	input:
		npfile="Generated_Structures/synthetic_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.npy"
	output:
		outfig="Gifs/synthetic/synthetic_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_100000_step_21_chro_all.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "

rule build_psc_small_images:
	input:
		npfile="Generated_Structures/ipsc_small_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	output:
		outfig="Gifs/ipsc_small/ipsc_small_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "



rule build_psc_full_images:
	input:
		npfile="Generated_Structures/ipsc_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.npy"
	output:
		outfig="Gifs/ipsc_full/ipsc_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_{res}_step_{step}_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile} "

rule buil_cardion_chro_images:
	input:
		npfile="Generated_Structures/cardio_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_{step}_chro_{chro}.npy"
	output:
		outfig="Gifs/cardio_chros/cardio_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_{step}_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile}"


rule buil_cardion_chro_missing_images:
	input:
		npfile="Generated_Structures/cardio_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_15_chro_{chro}.npy"
	output:
		outfig="Gifs/cardio_chros/cardio_missing_{missing}_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_1_step_15_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile}"



rule build_adipose_chro_images:
	input:
		npfile="Generated_Structures/adipose_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_50000_step_7_chro_{chro}.npy"
	output:
		outfig="Gifs/adipose_chros/adipose_full_rep_{rep}_eta_{eta}_alpha_{alpha}_lr_{lr}_epoch_{epoch}_res_50000_step_7_chro_{chro}.gif"
	shell:
		"python Python_Scripts/create_gif.py {output.outfig} {input.npfile}"

