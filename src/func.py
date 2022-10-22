import math, re

special_chars_remover = re.compile("[\W]_")

def remove_special_characters(sentence):
  return special_chars_remover.sub(' ', sentence)

def make_BOW(sentence):
  bow = {}
  
  words=remove_special_characters(sentence.lower()).split()
  
  for word in words:
    if len(word)>=1:
      bow.setdefault(word, 0)
      bow[word]+=1
  
  return bow

def calculate_doc_prob(train_data, test_data, alpha):
  Prob = 0
  
  TrainM = make_BOW(train_data)
  testM = make_BOW(test_data)
  
  tot = 0
  
  for word in TrainM:
    tot+=TrainM[word]

  for word in testM:
    test_cnt=testM[word]
    
    if word in TrainM:
      Train_cnt = TrainM
      Prob += test_cnt*(math.log(Train_cnt)-math.log(tot))
    else:
      Prob += test_cnt*(math.log(alpha)-math.log(tot))
  return Prob

def normalize_log_prob(prob1, prob2):
  maxprob = max(prob1, prob2)
  
  prob1 -= maxprob
  prob2 -= maxprob
  
  prob1 = math.exp(prob1)
  prob2 = math.exp(prob2)
  
  normalize_constant = 1.0 / float(prob1 + prob2)
  prob1 *= normalize_constant
  prob2 *= normalize_constant

  return (prob1, prob2)

def naive_bayes(train_data, test_data):
  log_prob_positive=calculate_doc_prob(train_data[1], test_data, 0.1) + math.log(0.5)
  log_prob_negative=calculate_doc_prob(train_data[0], test_data, 0.1) + math.log(0.5)
  prob_pos_neg=normalize_log_prob(log_prob_positive, log_prob_negative)
  
  return prob_pos_neg