from src.scraper import scrap
from src.func import naive_bayes

movieURL = "https://movie.naver.com/movie/bi/mi/basic.naver?code=115622"

scrap(movieURL) # 100개의 영화 리뷰 스크랩 및 tsv형식으로 파일 저장

def make_data():
  training_data = [[], []]
  f = open('ratings_train.txt', 'r')
  next(f)
  
  for line in f:
    sentence, label = line.split('\t')[1:]
    training_data[int(label)].append(sentence)
  return [' '.join(training_data[0]), ' '.join(training_data[1])]

def main():
  train_data = make_data()
  test_data = input('리뷰를 입력해 보세요(긍정/부정 분류):')
  prob = naive_bayes(train_data, test_data)
  print('긍정=', prob[0], "부정=", prob[1])
  
if __name__ == "__main__":
  main()