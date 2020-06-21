#./test dis/porto_all/hausdorff.txt data/porto/median/10000_hausdorff.txt data/porto/median/all_hausdorff.txt > porto_median_hausdorff.txt
#./test dis/porto_all/hausdorff.txt data/porto/new/10000_hausdorff.txt data/porto/new/all_hausdorff.txt > porto_new_hausdorff.txt

./calc_mat frechet data/shanghai_test.txt data/shanghai_test_all.txt
mv frechet.txt dis/shanghai_all/
./calc_mat dtw data/shanghai_test.txt data/shanghai_test_all.txt
mv dtw.txt dis/shanghai_all/
./calc_mat hausdorff data/shanghai_test.txt data/shanghai_test_all.txt
mv hausdorff.txt dis/shanghai_all/

#./test dis/shanghai_all/frechet.txt data/shanghai/median/10000_frechet.txt data/shanghai/median/all_frechet.txt > m_fre.txt
#./test dis/shanghai_all/dtw.txt data/shanghai/median/10000_dtw.txt data/shanghai/median/all_dtw.txt > m_dtw.txt
#./test dis/shanghai_all/hausdorff.txt data/shanghai/median/10000_hausdorff.txt data/shanghai/median/all_hausdorff.txt > m_haus.txt
#./test dis/shanghai_all/frechet.txt data/shanghai/new/10000_frechet.txt data/shanghai/new/all_frechet.txt > new_fre.txt
#./test dis/shanghai_all/dtw.txt data/shanghai/new/10000_dtw.txt data/shanghai/new/all_dtw.txt > new_dtw.txt
#./test dis/shanghai_all/hausdorff.txt data/shanghai/new/10000_hausdorff.txt data/shanghai/new/all_hausdorff.txt > new_haus.txt

#./test dis/shanghai_all/frechet.txt data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt > learning_all_shanghai_frechet.txt
#./test dis/shanghai_all/dtw.txt data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt > learning_all_shanghai_dtw.txt
#./test dis/shanghai_all/hausdorff.txt data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt > learning_all_shanghai_hausdorff.txt

#./test dis/shanghai_all/frechet.txt data/shanghai/t2vec_all/10000.txt data/shanghai/t2vec_all/all.txt > t2vec_all_shanghai_frechet.txt
#./test dis/shanghai_all/dtw.txt data/shanghai/t2vec_all/10000.txt data/shanghai/t2vec_all/all.txt > t2vec_all_shanghai_dtw.txt
#./test dis/shanghai_all/hausdorff.txt data/shanghai/t2vec_all/10000.txt data/shanghai/t2vec_all/all.txt > t2vec_all_shanghai_hausdorff.txt

#./test dis/porto_all/frechet.txt data/porto/hist/10000.txt data/porto/hist/all.txt \
#data/porto/onlypos/10000_frechet.txt data/porto/onlypos/all_frechet.txt \
#> hist_porto_frechet.txt
#./test dis/porto_all/dtw.txt data/porto/hist/10000.txt data/porto/hist/all.txt \
#data/porto/onlypos/10000_dtw.txt data/porto/onlypos/all_dtw.txt \
#> hist_porto_dtw.txt
#./test dis/porto_all/hausdorff.txt data/porto/hist/10000.txt data/porto/hist/all.txt \
#data/porto/onlypos/10000_hausdorff.txt data/porto/onlypos/all_hausdorff.txt \
#> hist_porto_hausdorff.txt

./test dis/shanghai_all/frechet.txt \
data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt \
data/shanghai/t2vec_all/10000.txt data/shanghai/t2vec_all/all.txt \
data/shanghai/neutraj/10000_frechet.txt data/shanghai/neutraj/all_frechet.txt \
data/shanghai/nt_no_sam/10000_frechet.txt data/shanghai/nt_no_sam/all_frechet.txt \
data/shanghai/new/10000_frechet.txt data/shanghai/new/all_frechet.txt \
data/shanghai/median/10000_frechet.txt data/shanghai/median/all_frechet.txt \
data/shanghai/hist/10000.txt data/shanghai/hist/all.txt > shanghai_all_frechet_res.txt

./test dis/shanghai_all/dtw.txt \
data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt \
data/shanghai/t2vec_all/10000.txt data/shanghai/t2vec_all/all.txt \
data/shanghai/neutraj/10000_dtw.txt data/shanghai/neutraj/all_dtw.txt \
data/shanghai/nt_no_sam/10000_dtw.txt data/shanghai/nt_no_sam/all_dtw.txt \
data/shanghai/new/10000_dtw.txt data/shanghai/new/all_dtw.txt \
data/shanghai/median/10000_dtw.txt data/shanghai/median/all_dtw.txt \
data/shanghai/hist/10000.txt data/shanghai/hist/all.txt > shanghai_all_dtw_res.txt

./test dis/shanghai_all/hausdorff.txt \
data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt \
data/shanghai/t2vec_all/10000.txt data/shanghai/t2vec_all/all.txt \
data/shanghai/neutraj/10000_hausdorff.txt data/shanghai/neutraj/all_hausdorff.txt \
data/shanghai/nt_no_sam/10000_hausdorff.txt data/shanghai/nt_no_sam/all_hausdorff.txt \
data/shanghai/new/10000_hausdorff.txt data/shanghai/new/all_hausdorff.txt \
data/shanghai/median/10000_hausdorff.txt data/shanghai/median/all_hausdorff.txt \
data/shanghai/hist/10000.txt data/shanghai/hist/all.txt > shanghai_all_hausdorff_res.txt

#./test dis/shanghai_all/dtw.txt \
#data/shanghai/learning_all/10000.txt data/shanghai/learning_all/all.txt \
#data/shanghai/neutraj/10000_dtw.txt data/shanghai/neutraj/all_dtw.txt \
#data/shanghai/nt_no_sam/10000_dtw.txt data/shanghai/nt_no_sam/all_dtw.txt \
#data/shanghai/hist/10000.txt data/shanghai/hist/all.txt >shanghai_all_dtw_res.txt

#./test_short dis/porto_all/frechet.txt \
#data/porto/sz_16/10000_frechet.txt data/porto/sz_16/all_frechet.txt \
#data/porto/sz_32/10000_frechet.txt data/porto/sz_32/all_frechet.txt \
#data/porto/sz_64/10000_frechet.txt data/porto/sz_64/all_frechet.txt \
#data/porto/sz_256/10000_frechet.txt data/porto/sz_256/all_frechet.txt > porto_all_frechet_res.txt

#./test_short dis/porto_all/dtw.txt \
#data/porto/sz_16/10000_dtw.txt data/porto/sz_16/all_dtw.txt \
#data/porto/sz_32/10000_dtw.txt data/porto/sz_32/all_dtw.txt \
#data/porto/sz_256/10000_dtw.txt data/porto/sz_256/all_dtw.txt \
#data/porto/sz_64/10000_dtw.txt data/porto/sz_64/all_dtw.txt > porto_all_dtw_res.txt

#./test_short dis/porto_all/hausdorff.txt \
#data/porto/sz_16/10000_hausdorff.txt data/porto/sz_16/all_hausdorff.txt \
#data/porto/sz_32/10000_hausdorff.txt data/porto/sz_32/all_hausdorff.txt \
#data/porto/sz_256/10000_hausdorff.txt data/porto/sz_256/all_hausdorff.txt \
#data/porto/sz_64/10000_hausdorff.txt data/porto/sz_64/all_hausdorff.txt > porto_all_hausdorff_res.txt

#./test dis/shanghai_all/frechet.txt \
#data/shanghai/new/10000_frechet.txt data/shanghai/new/all_frechet.txt \
#data/shanghai/hist/10000.txt data/shanghai/hist/all.txt

#./test dis/shanghai_all/dtw.txt \
#data/shanghai/hist/10000.txt data/shanghai/hist/all.txt
