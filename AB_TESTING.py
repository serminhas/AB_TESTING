#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
pd.set_option('display.width', 500)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df_=pd.read_excel(r"C:\Users\sermi\PycharmProjects\pythonProject4\ab_testing.xlsx")
df=df_.copy()
df.head()

control_df_=pd.read_excel(r"C:\Users\sermi\PycharmProjects\pythonProject4\ab_testing.xlsx", sheet_name="Control Group")
control_df=control_df_.copy()

test_df_=pd.read_excel(r"C:\Users\sermi\PycharmProjects\pythonProject4\ab_testing.xlsx", sheet_name="Test Group")
test_df=test_df_.copy()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_df.describe().T

test_df.describe().T

#mean ve median değerleri birbirine yakın olduğundan aykırı değerlerin varlığından söz edemeyiz.

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_total=pd.concat([control_df, test_df], ignore_index=True)

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

#H0: M1==M2 => Test ve Control gruplarının kazanç ortalamaları arasında önemli farklılık yoktur.
#H1: M1!=M2 => ...vardır.

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

control_df["Purchase"].mean()
test_df["Purchase"].mean()

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

#H0: Normal dağılım varsayımı sağlanmaktadır.
#H1: ... sağlanmamaktadır.

test_stat, pvalue= shapiro(control_df["Purchase"])
print("Test Stat = %.4f, pvalue= %.4f"%(test_stat, pvalue))

test_stat, pvalue= shapiro(test_df["Purchase"])
print("Test Stat = %.4f, pvalue= %.4f"%(test_stat, pvalue))

#Her ikisi için de p_value>0.05 => H0 REDDEDİLEMEZ => Normal dağılım varsayımı sağlanmaktadır.

#H0: Varyanslar homojendir.
#H1: ... homojen değildir.

test_stat, pvalue= levene(control_df["Purchase"], test_df["Purchase"])
print("Test Stat = %.4f, pvalue= %.4f"%(test_stat, pvalue))

#p_value>0.05 => H0 REDDEDİLEMEZ => Varyanslar homojendir.

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

test_stat, pvalue= ttest_ind(control_df["Purchase"], test_df["Purchase"], equal_var=True)
print("Test Stat = %.4f, pvalue= %.4f"%(test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

#pvalue>0.05 => H0 REDDEDİLEMEZ =>  Test ve Control gruplarının kazanç ortalamaları arasında önemli farklılık yoktur.

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#Normallik ve Varyans homojenliği varsayımları doğrulandığından parametrik test olan t testi kullanılmıştır.

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

#Average Bidding ve Maximum Bidding arasında önemli farklılık bulunmadığından her 2 teklif verme türü de kullanılabilir.
