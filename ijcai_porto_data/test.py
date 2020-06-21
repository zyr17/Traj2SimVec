import numpy as np
import pickle
import h5py
import sys
import torch

def similarity(a,b, sim_type):
    if sim_type == 'diff_exp':
        return float(-np.sqrt((np.sum(np.square(a - b)))))
    elif sim_type == 'cos':
        return (a*b).sum()

def validate_for_test(traj_list, traj_embeddings, distance,  mail_pre_degree, sim_type):

    print_batch = 100
    r10in50 = False

    top_10_count, l_top_10_count = 0, 0
    top_50_count, l_top_50_count = 0, 0
    top10_in_top50_count = 0
    test_traj_num = 0
    all_true_distance, all_test_distance = [], []
    error_true, error_test, errorr1050 = 0., 0., 0.

    for i in range(len(traj_list)):

        # This is for the exp similarity
        test_distance = [(j, similarity(traj_embeddings[i], e, sim_type))
                         for j, e in enumerate(traj_embeddings)]
        t_similarity = np.exp(-distance[i][:len(traj_embeddings)] * mail_pre_degree)
        true_distance = list(enumerate(t_similarity))
        learned_distance = list(enumerate(distance[i]))

        s_test_distance = sorted(test_distance, key=lambda a: a[1], reverse=True)
        s_true_distance = sorted(true_distance, key=lambda a: a[1], reverse=True)
        '''
        print(similarity(traj_embeddings[0], traj_embeddings[1], 'diff_exp'))
        print(test_distance[:100])
        print(s_test_distance[:100])
        print(s_true_distance[:100])
        input()
        '''
        s_learned_distance = sorted(learned_distance, key=lambda a: a[1])

        top10_recall = [l[0] for l in s_test_distance[:11] if l[0] in [j[0] for j in s_true_distance[:11]]]
        top50_recall = [l[0] for l in s_test_distance[:51] if l[0] in [j[0] for j in s_true_distance[:51]]]
        top10_in_top50 = [l[0] for l in s_test_distance[:11] if l[0] in [j[0] for j in s_true_distance[:51]]]

        top_10_count += len(top10_recall) - 1
        top_50_count += len(top50_recall) - 1
        top10_in_top50_count += len(top10_in_top50) - 1

        l_top10_recall = [l[0] for l in s_learned_distance[:11] if l[0] in [j[0] for j in s_true_distance[:11]]]
        l_top50_recall = [l[0] for l in s_learned_distance[:51] if l[0] in [j[0] for j in s_true_distance[:51]]]

        l_top_10_count += len(l_top10_recall) - 1
        l_top_50_count += len(l_top50_recall) - 1

        all_true_distance.append(s_true_distance[:50])
        all_test_distance.append(s_test_distance[:50])


        #print (s_true_distance[:11])

        true_top_10_distance = 0.
        for ij in s_true_distance[:11]:
            true_top_10_distance += distance[i][ij[0]]
        test_top_10_distance = 0.
        for ij in s_test_distance[:11]:
            # print (i, ij)
            test_top_10_distance += distance[i][ij[0]]
        test_top_10_distance_r10in50 = 0.
        temp_distance_in_test50 = []
        for ij in s_test_distance[:51]:
            temp_distance_in_test50.append([ij, distance[i][ij[0]]])
        sort_dis_10in50 = sorted(temp_distance_in_test50, key=lambda x: x[1])
        test_top_10_distance_r10in50 = sum([iaj[1] for iaj in sort_dis_10in50[:11]])

        error_true += true_top_10_distance
        error_test += test_top_10_distance
        errorr1050 += test_top_10_distance_r10in50

        test_traj_num += 1
        if False and (i % print_batch) == 0:
            # print test_distance
            print('**----------------------------------**')
            print('s_test_distance: ', s_test_distance[:20])
            print('s_true_distance: ', s_true_distance[:20])
            print(top10_recall)
            print(top50_recall)
            print('Search Top 10 recall {}'.format(float(top_10_count) / (test_traj_num * 10)))
            print('Search Top 50 recall {}'.format(float(top_50_count) / (test_traj_num * 50)))
          #  if len(top10_recall) - 1 <= 5:
          #      pdb.set_trace()

    if r10in50:
        error_test = errorr1050

    print('Test on {} trajs'.format(test_traj_num))
    print('Search Top 50 recall {}'.format(float(top_50_count) / (test_traj_num * 50)))
    print('Search Top 10 recall {}'.format(float(top_10_count) / (test_traj_num * 10)))
    print('Search Top 10 in Top 50 recall {}'.format(float(top10_in_top50_count) / (test_traj_num * 10)))
    print('Error true:{}'.format((float(error_true) / (test_traj_num * 10)) * 84000))
    print('Error test:{}'.format((float(error_test) / (test_traj_num * 10)) * 84000))
    print('Error div :{}'.format((float(abs(error_test - error_true)) / (test_traj_num * 10)) * 84000))
    print(float(top_10_count) / (test_traj_num * 10), \
            float(top_50_count) / (test_traj_num * 50), \
            float(top10_in_top50_count) / (test_traj_num * 10), \
            (float(error_true) / (test_traj_num * 10)) * 84000, \
            (float(error_test) / (test_traj_num * 10)) * 84000, \
            (float(abs(error_test - error_true)) / (test_traj_num * 10)) * 84000)

    return float(top_10_count) / (test_traj_num * 10)

def get_embedding(filename = '../t2vec/data/trj.h5'):
    if filename[-4:] == '.pkl':
        return pickle.load(open(filename, 'rb'))
    if filename[-3:] == '.pt':
        a = torch.load(filename)
        return a['test_result'].numpy()
    h5data = h5py.File(filename, 'r')
    res = np.array(h5data['layer3'], dtype='float')
    assert(res.shape[0] == 10000 and res.shape[1] == 128)
    return res

if __name__ == '__main__':
    data_path = './'
    dis_type = 'dtw'
    split = 'test'
    input_norm = True


    #with open(data_path + 'traj_embed_%s_%s.pkl'%(dis_type, split),'rb') as f:
        #traj_embeddings = pickle.load(f)
    if len(sys.argv) > 1:
        traj_embeddings = get_embedding(sys.argv[1])
    else:
        traj_embeddings = get_embedding()

    mat_path = data_path + "/dis_%s_%s.pkl" % (dis_type, split)
    if len(sys.argv) > 2:
        mat_path = sys.argv[2]

    magic_num = 17295.77609804242
    if len(sys.argv) > 3:
        magic_num = float(sys.argv[3])

    with open(mat_path, "rb") as f:
        dis_matrix = pickle.load(f) / magic_num

    validate_for_test(traj_embeddings=traj_embeddings, traj_list=dis_matrix, distance= dis_matrix, sim_type='diff_exp', mail_pre_degree=8)
