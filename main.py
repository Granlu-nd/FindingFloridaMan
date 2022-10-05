from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import re

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

time.sleep(3)

url = "https://news.google.com/search?q=Florida Man"
driver.get(url)

scroll_pause_time = .5
screen_height = driver.execute_script("return window.screen.height;")

i = 1
while True:
  driver.execute_script("window.scrollTo(0, {screen_height} * {i});".format(
    screen_height=screen_height, i=i))

  i += 1
  time.sleep(scroll_pause_time)

  scroll_height = driver.execute_script("return document.body.scrollHeight;")
  if screen_height * i > scroll_height:
    break

#out of loop
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html5lib')

driver.quit()

#-------------------------------------- algorithmic section

titles = []

frequency = dict()
whichTitle = dict()

titleNum = 0

matches = []

for heading in soup.findAll('h3', class_='ipQwMb ekueJc RD0gLb'):
  title = heading.find('a', class_="DY5T1d RZIKme").text
  safeTitle = True
  words = title.split()

  for i in range(len(words)):
    words[i] = re.sub("[^a-zA-Z]+", '', words[i]).lower()
    for match in matches:
      if match.lower() == words[i]:
        safeTitle = False
        break

  if safeTitle:
    for word in words:
      if word in frequency:
        frequency[word] += 1
        whichTitle[word].append(titleNum)
      else:
        frequency[word] = 1
        whichTitle[word] = [titleNum]
    titles.append(title)
    titleNum += 1

titleU = [0] * len(titles)
for word, freq in frequency.items():
  if freq == 1:
    for titleNum in whichTitle[word]:
      titleU[titleNum] += 1

for i in range(len(titleU)):
  print(titles[i] + ": " + str(titleU[i]) + "\n")

mostUScore = max(titleU)

print("Best Title" + str(mostUScore) + "unique words: ")

for i in range(len(titles)):
  if titleU[i] == mostUScore:
    print(titles[i])
