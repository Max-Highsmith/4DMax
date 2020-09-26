import pdb
import numpy as np
import matplotlib.pyplot as plt

time_nms = ['Ba', 'D2', 'D4', 'D6', 'D8', 'PSC']
times    = [0,2,4,6,8,10]
def show_pcc(pcc_log, **args):
	num_hic = len(list(pcc_log[0].keys()))
	fig, ax = plt.subplots(1)
	for i in range(0, num_hic):
		pcc = list(map(lambda x:x[times[i]][0], pcc_log))
		ax.plot(pcc, label=time_nms[i])
	
	title_ar = []
	for i in dict(args).keys():
		if i=="name":
			continue
		else:
			title_ar.append(i+"_"+str(args[i])+"_")
	title_text = ''.join(title_ar)
	ax.set_title("PCC Log \n("+title_text+")")
	ax.set_xlabel("Pearson Correlation")
	ax.set_ylabel("Epochs")
	ax.legend()
	plt.show()

def show_mov(mov_log, **args):
	fig, ax = plt.subplots()
	ax.set_title("mov_log")
	ax.plot(mov_log)
	plt.show()

def train_graphs(**args):
	x = np.load("Generated_Struc_Logs/"+args['name']+""\
	"_rep_"+str(args['rep'])+"_eta_"+str(args['eta'])+""\
	"_alpha_"+str(args['alpha'])+"_lr_"+str(args['lr'])+""\
	"_epoch_"+str(args['epoch'])+"_res_"+str(args['res'])+""\
	"_step_"+str(args['step'])+"_chro_"+str(args['chro'])+".npy", allow_pickle=True)
	pcc_log = x.item()['pcc_log']
	mov_log = x.item()['mov_log']
	show_pcc(pcc_log, **args)
	show_mov(mov_log, **args)


if __name__ == "__main__":
	args = {
		"name":"ipsc_full",
		"rep":2,
		"eta":1000,
		"alpha":0.6,
		"lr":0.00001,
		"epoch":1000,
		"res":50000,
		"step":21,
		"chro":3,
		}

	for chro in [1,2,3]:
		train_graphs(**args)
