from train_model import MATES_train 
from make_prediction import make_prediction

def train(data_mode, file_name, bin_size = 5, proportion = 80, BATCH_SIZE= 4096, 
          AE_LR = 1e-4, MLP_LR = 1e-6, AE_EPOCHS = 200, MLP_EPOCHS = 200, USE_GPU= True):
    if data_mode != "10X" and data_mode != "Smart_seq":
        print('Invalid data format.')
        exit(1)
    
    if data_mode == "10X":
        sample_name = open(file_name).read().strip()
        for idx, sample in enumerate(sample_name):
            MATES_train(data_mode, sample, bin_size, proportion, BATCH_SIZE= 4096, 
                        AE_EPOCHS = 200, MLP_EPOCHS = 200, MLP_LR = 1e-6, EPOCHS = 200, USE_GPU= True)
    elif data_mode == 'Smart_seq':
        MATES_train(data_mode, file_name, bin_size, proportion, BATCH_SIZE= 4096, 
                    AE_EPOCHS = 200, MLP_EPOCHS = 200, MLP_LR = 1e-6, EPOCHS = 200, USE_GPU= True)

def prediction(TE_mode, data_mode, file_name, bin_size, proportion, AE_trained_epochs, MLP_trained_epochs, USE_GPU= True):
    if TE_mode == "exclusiv":
        TE_ref_path = './TE_nooverlap.csv'
    else: 
        TE_ref_path = './TE_Full.csv'
    if data_mode != "10X" and data_mode != "Smart_seq":
        print('Invalid data format.')
        exit(1)
    
    if data_mode == "10X":
        sample_name = open(file_name).read().strip()
        for idx, sample in enumerate(sample_name):
            make_prediction(data_mode, bin_size, proportion, TE_ref_path, AE_trained_epochs, MLP_trained_epochs, sample, USE_GPU)
    elif data_mode == 'Smart_seq':
        make_prediction(data_mode, bin_size, proportion, TE_ref_path, AE_trained_epochs, MLP_trained_epochs, None, USE_GPU)
    
    