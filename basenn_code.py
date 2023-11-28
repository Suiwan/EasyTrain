# coding:utf-8
from BaseNN import nn

def generated_train():
	model = nn()
	model.load_tab_data(r'D:\workspace\XEdu\datasets\basenn\iris\iris_training.csv',y_type='long',batch_size=32)
	model.save_fold = r'D:\workspace\XEdu\my_checkpoints\basenn_20231128_101553'
	model.set_seed(42)
	model.add(optimizer='SGD')
	model.add(layer='linear',size=(4, 10),activation='relu')
	model.add(layer='linear',size=(10, 20),activation='relu')
	model.add(layer='linear',size=(20, 3),activation='softmax')
	model.train(epochs=10,lr=0.01,loss='CrossEntropyLoss',metrics=['acc'])

if __name__ == '__main__':
	generated_train()
