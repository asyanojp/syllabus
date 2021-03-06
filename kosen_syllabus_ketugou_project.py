# -*- coding: utf-8 -*-
"""kosen_syllabus_KETUGOU_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i8aWgaGtZTBLYLfWCA1cGr0x8R1HVNs3
"""

#ライブラリの導入ここから
!pip install PyPDF2
import os
import sys
import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import time
import PyPDF2
import glob
import shutil
#ライブラリの導入ここまで



#情報の登録(年度で入力してください)
#school_id とdepartment_idの入力はこちらのHPを参照してください。
###################ここにURLを忘れない###################
#start_yearとend_yearで入力した年度の間のシラバスが取得されます。
#my_yearは、自分が入学した年度(若しくは、欲しいシラバスの学年が入学した年度)を入力してください。
school_id = "22"
department_id = "14"
start_year = "2020"
end_year = "2020"
my_year = "2018"
#情報の登録ココまで




#基礎情報ここから(いじらないでね)
urlBase = "https://syllabus.kosen-k.go.jp"
start_year = int(start_year)
end_year = int(end_year) + 1
my_year = int(my_year)
urlList = []
rangenum = end_year - start_year
if start_year > end_year:
  print("適切な開始年度と終了年度が設定されていません")
  sys.exit(1)
number = 1
#基礎情報ここまで(いじらないでね)

print("""



システムのご利用ありがとうございます。
処理が開始されます。
処理はおおよそ5分程度で終了します。
--------------------
シラバスが取得される、開始年度は{}年度で終了年度は{}年度です。
シラバスが取得される、入学年度は{}年度です。
シラバスが取得される、学校コードは{}で学科コードは{}です。
--------------------
2018年度以前のシラバスは、今のように全ての科目を網羅していない場合があります。
--------------------
このシステムは、留年や休学などを考慮していません。
入学年度からストレートで進級した場合のシラバスが取得されます。
--------------------""".format(str(start_year),str(end_year - 1),str(my_year),str(school_id),str(department_id)))


#アクセスURLの生成ここから

accessurlBase = urlBase + "/Pages/PublicSubjects?"
for i in range(rangenum):
  year = start_year + i
  if year == end_year:
    break
  year = str(year)
  url = accessurlBase + "school_id="+school_id+"&department_id="+department_id+"&year="+year+"&lang=ja"
  urlList.append(url)
  #ここまでで標準5個のURLの作成
#アクセスURLの生成ここまで

print("ベースURLの取得が完了しました。(5%)")
print("もし、暇なら、僕のブログを見ててもいいんじゃね？Googleで「asyano」と検索")

#スクレイピングを実施及びPDFのDLここから
#年度ごとのfor
for i in urlList:
  #保存用フォルダの作成
  os.mkdir("/content/{}".format(number))
  syllabusUrl = []
  url = requests.get(i)
  time.sleep(2)
  soup = BeautifulSoup(url.content, "html.parser")
  elems = soup.find_all("a")
  #1年度のシラバスURLのfor
  for elem in elems: 
    try:
      string = elem.get("class").pop(0)
      if string in "mcc-show":
        r = elem.find_previous('a')
        if "PublicSyllabus" in r.get('href'):
          urlData = urlBase + r.get('href')
          #取得されたURLデータが、取得すべきデータかの検証(入学年度)
          data = urlData.split("&")
          if int(data[3][-4:]) == my_year:
            syllabusUrl.append(urlData)
  
    except:
      pass
  #取得されたURLにアクセスし、PDFのURLを取得する
  #1年度のシラバスのPDFのfor
  suuji = 0
  for j in syllabusUrl:
    url = requests.get(j)
    time.sleep(2)
    soup = BeautifulSoup(url.content, "html.parser")

    elems = soup.find_all("a")
    for elem in elems:
      try:
        string = elem.get("href")
        if "attachment=false" in string:
          url = urlBase + string
      except:
        pass
    #PDFをDL
    savepath = "/content/{}/{}.pdf".format(number,suuji)
    urllib.request.urlretrieve(url, savepath)
    time.sleep(2)
    suuji = suuji + 1
  number = number + 1

#スクレイピングを実施及びPDFのDLここまで
print("全てのPDFの取得が完了しました。(70%)")
#ファイルの結合の実施ここから
urlListNum = len(urlList)
os.mkdir("/content/all_syllabus")
for i in range(urlListNum):
  inow = i + 1
  inow_year = str(start_year + i)
  inow_admition_year = str(my_year)
  files = glob.glob("/content/{}/*".format(inow))
  merger = PyPDF2.PdfFileMerger()
  for file in files:
    merger.append(file)
  merger.write('/content/all_syllabus/school_id={}_department_id={}_my_admission_year={}_this_file_year={}.pdf'.format(str(school_id),str(department_id),inow_admition_year,inow_year))
  merger.close()
  shutil.rmtree("/content/{}/".format(inow))

print("全ての処理が完了しました。(100%)")
print("--------------------")
print("左のファイルアイコン内の、[all_syllabus]内に、各年度ごとのシラバスがあります。(google colab利用時)")
print("印刷などをしてご利用ください。")
print("システムをご利用いただきありがとうございました。")
print("--------------------")
print("Program Wrote By asyano.jp")
print("--------------------")
#ファイルの結合の実施ここまで


#Thank you for USING