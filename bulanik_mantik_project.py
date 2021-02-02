
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as karar

ortamSicakligi = karar.Antecedent(np.arange(20, 50, 1), 'ortam sıcaklığı')
nemOrani = karar.Antecedent(np.arange(0, 101, 1), 'nem oranı')
ortamKisiSayisi = karar.Antecedent(np.arange(1, 21, 1), 'ortamdaki kişi sayısı')
sonuc = karar.Consequent(np.arange(0, 101, 1), 'klimanın durumu')

ortamSicakligi['düşük'] = fuzz.trimf(ortamSicakligi.universe, [20, 23, 25])
ortamSicakligi['orta'] = fuzz.trimf(ortamSicakligi.universe, [25, 30, 35])
ortamSicakligi['yüksek'] = fuzz.trimf(ortamSicakligi.universe, [40, 45, 50])

nemOrani['düşük'] = fuzz.trimf(nemOrani.universe, [0, 20, 30])
nemOrani['orta'] = fuzz.trimf(nemOrani.universe, [30, 50, 70])
nemOrani['yüksek'] = fuzz.trimf(nemOrani.universe, [70, 90, 100])

ortamKisiSayisi['az'] = fuzz.trimf(ortamKisiSayisi.universe, [1, 3, 5])
ortamKisiSayisi['orta'] = fuzz.trimf(ortamKisiSayisi.universe, [5, 7, 10])
ortamKisiSayisi['çok'] = fuzz.trimf(ortamKisiSayisi.universe, [10, 15, 20])


sonuc['sıcaklık derecesini arttır'] = fuzz.trimf(sonuc.universe, [0, 0, 50])
sonuc['soğutmayı arttır'] = fuzz.trimf(sonuc.universe, [0, 50, 100])
sonuc['şuanki dereceyi koru'] = fuzz.trimf(sonuc.universe, [50, 100, 100])

ortamSicakligi.view()
nemOrani.view()
ortamKisiSayisi.view()
sonuc.view()

kural1 = karar.Rule(ortamSicakligi['yüksek'] & nemOrani['yüksek'], sonuc['soğutmayı arttır'])
kural2 = karar.Rule(ortamSicakligi['yüksek'] & ortamKisiSayisi['çok'], sonuc['soğutmayı arttır'])
kural3 = karar.Rule(nemOrani['orta'] | ortamKisiSayisi['az'], sonuc['şuanki dereceyi koru'])
kural4 = karar.Rule(ortamKisiSayisi['orta'] & ortamSicakligi['orta'], sonuc['şuanki dereceyi koru'] )
kural5 = karar.Rule(ortamSicakligi['düşük'] | nemOrani['düşük'], sonuc['sıcaklık derecesini arttır'])
kural6 = karar.Rule(ortamKisiSayisi['az'] & ortamSicakligi['düşük'], sonuc['sıcaklık derecesini arttır'])
kural7 = karar.Rule(ortamSicakligi['orta'] & nemOrani['orta'], sonuc['şuanki dereceyi koru'])
kural8 = karar.Rule(nemOrani['düşük'] | ortamSicakligi['orta'], sonuc['şuanki dereceyi koru'])

sonuc_karar = karar.ControlSystem([kural1, kural2, kural3, kural4, kural5, kural6, kural7, kural8])
sonuc_ = karar.ControlSystemSimulation(sonuc_karar)

sonuc_.input['ortam sıcaklığı'] = 50
sonuc_.input['nem oranı'] = 90
sonuc_.input['ortamdaki kişi sayısı'] = 10

sonuc_.compute()


print(sonuc_.output['klimanın durumu'])
sonuc.view(sim=sonuc_)
