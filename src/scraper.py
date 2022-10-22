# -*- coding: utf-8 -*-

from requests import get
from bs4 import BeautifulSoup
import re, random

def get_code(url):
  return url[len("https://movie.naver.com/movie/bi/mi/basic.naver?code="):]

def save_file(datas):
  file = open('ratings_train.txt', 'w')
  for data in datas:
    file.write("%s\t%s\t%d\n" % (data["별점"], data["리뷰"], data["라벨"]))
  file.close()

def scrap(target):
  code = get_code(target)
  result = []
  for i in range(1, 11):
    response = get(f"https://movie.naver.com//movie/bi/mi/pointWriteFormList.naver?code={code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={i}")
    if response.status_code!=200:
      print("Can't request this website")
    else:
      soup = BeautifulSoup(response.text, "html.parser")
      table = soup.find('div', class_="score_result")
      reviews = table.find_all('li')
      index = 0
      for review in reviews:
        scoreReple = review.find('span', id=f"_filtered_ment_{index}")
        reple = ""
        if scoreReple.string==None:
          scoreReple = scoreReple.find('a')
          reple = re.sub("&#39;", "", scoreReple["data-src"])
        else:
          reple = re.sub("\r|\t|\n", "", scoreReple.text)
        review_data = {
          "별점" : review.find('em').string,
          "리뷰" : reple,
          "라벨" : random.randint(0, 1)
        }
        index += 1
        result.append(review_data)
  save_file(result)