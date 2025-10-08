import pickle
import time

import matplotlib.pyplot as plt
from gensim.models.callbacks import CallbackAny2Vec

import pandas as pd
from gensim.models import Word2Vec
import glob

def learn_embeddings(walks,file_name,dim,window,epoch,alpha,min_alpha):
    walk_lol = [[str(i) for i in walk] for walk in walks]
    # 构建模型
    loss_list = []
    lr_list = []

    # 打印每个epoch的loss
    class callback(CallbackAny2Vec):
        def __init__(self):
            self.epoch = 0

            self.loss_to_be_subed = 0

        def on_epoch_end(self, model):
            loss = model.get_latest_training_loss()
            loss_now = loss - self.loss_to_be_subed
            self.loss_to_be_subed = loss

            loss_list.append(loss_now)
            lr_list.append(model.min_alpha_yet_reached)
            self.epoch += 1
    model = Word2Vec(walk_lol, vector_size=dim, window=window, min_count=0, sg=1, workers=32, epochs=epoch,
                     compute_loss = True,
                     callbacks = [callback()],
                     alpha = alpha,
                     min_alpha = min_alpha)


    # 保存训练结果
    model.wv.save_word2vec_format(file_name)
    return loss_list

def get_walks(file_name,dim,window,epoch,alpha,min_alpha):

    # 获取每个时间段的轨迹
    files = glob.glob(file_name + "/1*.pkl")
    files_sorted = sorted(files, key=lambda x: (int(x[len(file_name)+1:-4])))
    walks = []
    for file in files_sorted:
        with open(file,'rb') as f:
            a = pickle.load(f)
        for i, v in a.items():
            walks.append(v)

    # 将每个时间段的轨迹送到模型学习向量

    print("/home/dell/PycharmProjects/GAT_CD_traffic/data/2_trj_embedding/word2vec/"+file_name[58:]+"/word2vec_embedding_e"
                            +str(epoch)+"_m"+str(min_alpha)+".csv")
    loss = learn_embeddings(walks,"/home/dell/PycharmProjects/GAT_CD_traffic/data/2_trj_embedding/word2vec/"+file_name[58:]+"/dim_"+str(dim)+"_w_"+str(window)+"_e"
                            +str(epoch)+"_a_"+str(alpha)+"_m"+str(min_alpha)+".csv",
                            dim, window, epoch, alpha, min_alpha)
    return loss

def main():
    dim = [ 64,128,264,512,1024,2048]
    epoch = 100
    window = 10
    alpha = 0.01
    min_alpha = 0.01
    files = glob.glob("/home/dell/PycharmProjects/GAT_CD_traffic/data/1_trj_list")
    files_sorted = sorted(files)

    for file in files_sorted[:1]:


            loss_list = []
            labels = []
            for i in dim:

                p_dim = i
                p_window_size = window
                names = "dim_" + str(p_dim) + "_w_" + str(p_window_size) + "_e" + str(epoch) + "_a_" + str(
                    alpha) + "_m" + str(min_alpha)
                labels.append("dim:"+str(i))
                print(file)
                start = time.time()
                loss = get_walks(file, p_dim, p_window_size, epoch, alpha, min_alpha)
                loss_list.append(loss)
                print("耗时：" + str(time.time() - start))
            for p in range(len(loss_list)):
                plt.plot(loss_list[p],label = labels[p])
            plt.legend()  # 显示图例
            plt.savefig(
                "/home/dell/PycharmProjects/GAT_CD_traffic/data/2_trj_embedding/loss_png/word_loss_.png")
            plt.clf()

if __name__ == '__main__':
    main()