import subprocess
import os
import pandas as pd

##### Quant Unique TE #####
def unique_TE_MTX(TE_mode, data_mode, file_name, threads_num, barcodes_file_path_list=None):
    if TE_mode == "exclusiv":
        TE_ref_path = './TE_nooverlap.csv'
    else: 
        TE_ref_path = './TE_Full.csv'

    os.makedirs("Unique_TE", exist_ok=True)

    if data_mode == "Smart_seq":
        sample_count = sum(1 for line in open(file_name)) + 1
        file_batch = threads_num

        result = sample_count / file_batch
        sample_per_batch = int(result + 0.5)
        processes = []
        for i in range(threads_num):
            command = f"python scripts/quant_unique_TE.py {file_name} {i} {sample_per_batch} {TE_ref_path} {data_mode} {None}"
            process = subprocess.Popen(command, shell=True)
            processes.append(process)

        for process in processes:
            process.wait()

        unique_file_list = os.listdir('Unique_TE')
        Unique_TE = pd.read_csv('Unique_TE/' + unique_file_list[0], index_col = 0)

        i = 1
        while len(unique_file_list[1:]) > 0:
            Unique_TE_tmp = pd.read_csv('Unique_TE/' + unique_file_list[i], index_col = 0)
            Unique_TE = pd.concat([Unique_TE, Unique_TE_tmp], axis=0, ignore_index=False)
            i += 1

        Unique_TE = Unique_TE.fillna(0)
        Unique_TE = Unique_TE.groupby(Unique_TE.index).sum()
        Unique_TE = Unique_TE.drop_duplicates()
        Unique_TE.to_csv('Unique_TE/Unique_All_MTX.csv')

    elif data_mode == "10X":
        sample_name = open(file_name).read().strip()
        barcodes_paths = open(barcodes_file_path_list).read().strip()
        for idx, sample in enumerate(sample_name):
            sample_count = sum(1 for line in open(barcodes_paths[idx])) + 1
            file_batch = threads_num

            result = sample_count / file_batch
            sample_per_batch = int(result + 0.5)
            processes = []
            for i in range(threads_num):
                command = f"python scripts/quant_unique_TE.py {sample} {i} {sample_per_batch} {TE_ref_path} {data_mode} {barcodes_paths[idx]}"
                process = subprocess.Popen(command, shell=True)
                processes.append(process)

            for process in processes:
                process.wait()

            Unique_TE = pd.read_csv('Unique_TE/'+sample+'/' + unique_file_list[0], index_col = 0)
            i = 1
            while len(unique_file_list[1:]) > 0:
                Unique_TE_tmp = pd.read_csv('Unique_TE/' +sample+'/' + unique_file_list[i], index_col = 0)
                Unique_TE = pd.concat([Unique_TE, Unique_TE_tmp], axis=0, ignore_index=False)
                i += 1

            Unique_TE = Unique_TE.fillna(0)
            Unique_TE = Unique_TE.groupby(Unique_TE.index).sum()
            Unique_TE = Unique_TE.drop_duplicates()
            Unique_TE.to_csv('Unique_TE/'+sample+'/Unique_All_MTX.csv')
    else:
        print('Invalid data format.')

##### Quant All TE #####
def finalize_TE_MTX(data_mode, file_name=None):
    if data_mode == "Smart_seq":
        os.makedirs("result_MTX", exist_ok=True)
        os.rename("Combination/TE_MTX.csv", "result_MTX/TE_MTX.csv")
        os.rename("Unique_TE/Unique_All_MTX.csv", "result_MTX/Unique_TE_MTX.csv")
        os.rename("prediction/Multi_MTX.csv", "result_MTX/Multi_TE_MTX.csv")
        os.rmdir("Combination")
        os.rmdir("Unique_TE")
        os.rmdir("prediction")
    elif data_mode == "10X":
        os.makedirs("result_MTX", exist_ok=True)
        if file_name == None:
            print('Please provide sample list for 10X data.')
            exit(1)
        with open(file_name, "r") as f:
            for line in f:
                line = line.strip()
                os.makedirs(f"result_MTX/{line}", exist_ok=True)
                os.rename(f"Combination/{line}/TE_MTX.csv", f"result_MTX/{line}/TE_MTX.csv")
                os.rename(f"Unique_TE/{line}/Unique_All_MTX.csv", f"result_MTX/{line}/Unique_TE_MTX.csv")
                os.rename(f"prediction/{line}/Multi_MTX.csv", f"result_MTX/{line}/Multi_TE_MTX.csv")
                os.rmdir(f"Combination/{line}")
                os.rmdir(f"Unique_TE/{line}")
                os.rmdir(f"prediction/{line}")

        os.rmdir("Combination")
        os.rmdir("Unique_TE")
        os.rmdir("prediction")