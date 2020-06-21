class HistogramsEmbedding:
    #(longitude, latitude)
    coordinate_min_lon = 180
    coordinate_max_lon = -180
    coordinate_min_lat = 90
    coordinate_max_lat = -90
    # divide number
    div_num_bin = 1
    div_num_lon = 1
    div_num_lat = 1
    div_delta_lon = 1
    div_delta_lat = 1
    # flag
    coordinate_set_flag = False
    div_num_set_flag = False

    def __init__(self):
        print('Histograms Init succeed, should run set_coordinate() and set_div_num() first')

    def __set_div_gap(self):
        if self.coordinate_set_flag and self.div_num_set_flag:
            self.div_delta_lon = (self.coordinate_max_lon + 0.000001 - self.coordinate_min_lon) / self.div_num_lon
            self.div_delta_lat = (self.coordinate_max_lat + 0.000001 - self.coordinate_min_lat) / self.div_num_lat
            self.div_num_bin = self.div_num_lon * self.div_num_lat

    def set_coordinate(self, coo_min_lon, coo_max_lon, coo_min_lat, coo_max_lat):
        self.coordinate_min_lon, self.coordinate_max_lon = coo_min_lon, coo_max_lon
        self.coordinate_min_lat, self.coordinate_max_lat = coo_min_lat, coo_max_lat
        self.coordinate_set_flag = True
        print('Trajectory lon gap is {:6f} and lat gap is {:6f}'.format(coo_max_lon - coo_min_lon, coo_max_lat - coo_min_lat))
        self.__set_div_gap()

    def set_div_num(self, div_num_lon = 1, div_num_lat = 1):
        self.div_num_lon = div_num_lon
        self.div_num_lat = div_num_lat
        self.div_num_set_flag = True
        print('Histograms bin number is {}'.format(div_num_lon * div_num_lat))
        self.__set_div_gap()

    def __get_bin_2d_index(self, lon: float, lat: float) -> (int, int):
        if not self.coordinate_min_lon <= lon <= self.coordinate_max_lon:
            return 0, -1
        if not self.coordinate_min_lat <= lat <= self.coordinate_max_lat:
            return 0, -1
        lon_bin_num = int((lon - self.coordinate_min_lon) / self.div_delta_lon)
        lat_bin_num = int((lat - self.coordinate_min_lat) / self.div_delta_lat)
        return lon_bin_num, lat_bin_num

    def __get_bin_1d_index(self, lon_bin_num: int, lat_bin_num: int, method='normal') -> int:
        # todo: different methods
        bin_1d_index = 0
        if method == 'normal':
            # 123
            # 456 like
            bin_1d_index = lon_bin_num * self.div_num_lat + lat_bin_num
        return bin_1d_index

    def encoder(self, trajectory):
        # must set coordinate and divide number first
        assert self.div_num_set_flag and self.coordinate_set_flag
        # create an empty embedding
        embedding = list()
        for i in range(self.div_num_bin):
            embedding.append(0)
        # count points of trajectory in bins
        for point in trajectory:
            lon_bin_num, lat_bin_num = self.__get_bin_2d_index(point[0], point[1])
            bin_1d_index = self.__get_bin_1d_index(lon_bin_num, lat_bin_num, method='normal')
            # print(point[0], point[1])
            # print(self.coordinate_min_lon, self.coordinate_min_lat)
            # print(self.div_delta_lon, self.div_delta_lat)
            # print(lon_bin_num, lat_bin_num)
            if bin_1d_index != -1:
                embedding[bin_1d_index] += 1
        # return the bin embedding
        return embedding

if __name__ == '__main__':
    print('Trajectory Histograms Embedding')
    embedding_method = HistogramsEmbedding()
    embedding_method.set_coordinate(0, 90, 0, 90)
    embedding_method.set_div_num(2, 2)
    print(embedding_method.encoder([(20, 20), (60, 60), (30, 0), (60, 30)]))
    # print(embedding_method.encoder([(100, 0)]))
