import pickle
import numpy as np
import sys
from HistogramsEmbedding import HistogramsEmbedding
import time

if __name__ == '__main__':
    start_time = time.time()
    # data_path = '/home/zhanghanyuan/trajRep/data/random_test/'
    dis_type = 'frechet'
    split = 'test'
    input_norm = True

    with open(sys.argv[1], "rb") as f:
        traj_list = pickle.load(f)

    # print(len(traj_list))
    # print(len(traj_list[0]))
    # print(traj_list[0])

    embedding_method = HistogramsEmbedding()

    #shanghai
    #min_lon, max_lon = 121.08155822753906, 121.81672668457031
    #min_lat, max_lat = 30.90562629699707, 31.45410919189453
    #porto
    min_lon, max_lon = -8.699525833129883, -8.498448371887207
    min_lat, max_lat = 41.1006965639207, 41.19973373413086
    '''
    for traj in traj_list:
        for lat, lon in traj:
            if lon > max_lon:
                max_lon = lon
            if lon < min_lon:
                min_lon = lon
            if lat > max_lat:
                max_lat = lat
            if lat < min_lat:
                min_lat = lat
    '''
    embedding_method.set_coordinate(coo_min_lon=min_lon, coo_max_lon=max_lon, coo_min_lat=min_lat, coo_max_lat=max_lat)
    embedding_method.set_div_num(8, 16)

    embeddings = list()
    for traj in traj_list:
        embedding = np.array(embedding_method.encoder(map(lambda latlon: (latlon[1], latlon[0]), traj)))
        embeddings.append(embedding)

    traj_embed_file = open('result.pkl','w+b')
    pickle.dump(embeddings, traj_embed_file)

    embedding_method.set_div_num(16, 8)
    embeddings_list = list()
    for traj in traj_list:
        embedding = embedding_method.encoder(map(lambda latlon: (latlon[1], latlon[0]), traj))
        embeddings_list.append(embedding)

    traj_embed_file_txt = open('result.txt','w+')
    print(len(embeddings_list), file=traj_embed_file_txt)
    for embedding in embeddings_list:
        print(' '.join(str(num) for num in list(embedding)), file=traj_embed_file_txt)
    print(time.time() - start_time)
