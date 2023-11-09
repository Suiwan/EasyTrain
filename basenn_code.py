# coding:utf-8
from BaseNN import nn

def generated_train():
	model = nn()
	model.load_tab_data(r'D:\workspace\XEdu\datasets\basenn\workflow\workflow_pose_train.csv',batch_size=128)
	model.save_fold = r'D:\workspace\XEdu\my_checkpoints\basenn_20231109_105344'
	model.set_seed(42)
	model.add(optimizer='Adam')
	model.add(layer='linear',size=(52, 120),activation='relu')
	model.add(layer='linear',size=(120, 84),activation='relu')
	model.add(layer='linear',size=(84, 8),activation='softmax')
	model.train(epochs=10,lr=0.01,loss='CrossEntropyLoss',metrics=['acc'])

if __name__ == '__main__':
	generated_train()
