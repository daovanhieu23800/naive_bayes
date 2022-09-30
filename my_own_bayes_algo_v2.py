#some helpful ib
import math

N_WORDS = 2500
P_NONE_SPAM = 0.5
P_SPAM = 0.5
N_EMAILS = 50

#in
DATA_FOLDER = 'ex6DataPrepared'
FILE_PATHS = f'train-features-{N_EMAILS}.txt'

def read_data_set(file_path=FILE_PATHS):
    with open(DATA_FOLDER+'/'+file_path) as f:
        datas = f.readlines() 
    #remove end_line_in data
    clean_data =  [data.strip() for data in datas ]
    train_data = [x.split(' ') for x in clean_data]
    
    return train_data

def create_spare_matrix(train_data,size):
    row = [int(x[0]) for x in train_data]
    col = [int(x[1]) for x in train_data]
    value = [int(x[2]) for x in train_data]

   
    total_email = list(set(row)) #cacalute total email in data set
    sparse_matrix = [ [0 for i in range((N_WORDS)) ] for j in range(len(total_email))]
    total_spam_words, total_not_spam_words = 0, 0
    for k in range(len(row)):
        sparse_matrix[row[k]-1][col[k]-1]=value[k]
        if row[k] <= (int(size)/2):
            total_not_spam_words += value[k]
        else:
            total_spam_words +=value[k]
    return sparse_matrix, total_spam_words, total_not_spam_words

def posibility_vector(train_matrix_data,total_spam_words,total_not_spam_words):
    spam_posibility_vector = [0 for i in range((2500))]
    not_spam_posibility_vector = [0 for i in range((2500))]

   
    for i in range(0,int(len(train_matrix_data)/2)):
        for j in range(N_WORDS):
            if train_matrix_data[i][j] != 0 :
                not_spam_posibility_vector[j] += train_matrix_data[i][j]

    for i in range(int(len(train_matrix_data)/2), int(len(train_matrix_data))):
        for j in range(N_WORDS):
            if train_matrix_data[i][j] != 0 :
                spam_posibility_vector[j] += train_matrix_data[i][j]

    for i in range(2500):
        not_spam_posibility_vector[i] = (not_spam_posibility_vector[i]+1) / (total_not_spam_words+2500)
        spam_posibility_vector[i] = (spam_posibility_vector[i]+1) / (total_spam_words+2500)
   
    return spam_posibility_vector, not_spam_posibility_vector

def predict_email(vector ,spam_posibility_vector, not_spam_posibility_vector):
    spam_value=0
    not_spam_value=0
    for i in range(2500):
        spam_value += vector[i] * math.log(spam_posibility_vector[i])
        not_spam_value += vector[i] * math.log(not_spam_posibility_vector[i])
    
    if not_spam_value >= spam_value:
        return 0
    else: 
        return 1

def calculate_accuracy(real_labels, predict_labels):
    count = 0
    for i in range((260)):
        if (real_labels[i] != predict_labels[i]):
            count+=1
    return 1-(count/260)

def main():
    train_data = read_data_set()
    train_matrix,total_spam_words,total_not_spam_words = create_spare_matrix(train_data,N_EMAILS)
    spam_posibility_vector, not_spam_posibility_vector = posibility_vector(train_matrix,total_spam_words,total_not_spam_words)

    test_data =  read_data_set("test-features.txt")
    test_matrix = create_spare_matrix(test_data,260)[0]

    test_labels = [0 if i<130 else 1 for i in range(260)]
    predict_label = []
    for i in test_matrix:
        predict_label.append(predict_email(i,spam_posibility_vector, not_spam_posibility_vector ))
    print(calculate_accuracy(test_labels, predict_label))
if __name__ == "__main__":
    main()