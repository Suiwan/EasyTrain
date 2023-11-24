# coding:utf-8
from MMEdu import MMClassification as cls
def generated_train():
	model = cls(backbone='LeNet')
	model.num_classes = 3
	model.load_dataset(path=r'D:\workspace\XEdu\datasets\mmedu_cls\Oracle_Bone_Characters_dataset')
	model.save_fold = r'D:\workspace\XEdu\my_checkpoints\mmedu_20231123_153303'
	model.train(epochs=10,validate=True,device='cpu',optimizer='SGD',lr=0.01, batch_size=None,weight_decay=0.001,checkpoint=None,random_seed=42)

if __name__ == '__main__':
	generated_train()
