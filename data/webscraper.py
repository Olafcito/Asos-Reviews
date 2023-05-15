from bs4 import BeautifulSoup
import requests
import csv
import time
import random

pages = 6791
# Ip banned at page 4468
start_page = 6619

# Open a csv file to store the reviews
with open('reviews.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Rating", "Title", "Review"])
    for n in range(start_page,pages):
        print(f'page: {n}')
        url = f"https://trustpilot.com/review/www.asos.com?languages=en&page={n}"

        # Setting random delay between 0.5 and 8 secodns to mitigate risk of ban
        delay = random.uniform(0.5, 2)  
        time.sleep(delay)

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')    
        # Finding all reviews
        reviews = soup.find_all('div', class_= 'styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ') 
        if len(reviews) < 1:
            print(f'IP banned at page: {n}')
            break
        for i, review in enumerate(reviews):

            # language = review.find('div', class_='styles_reviewContent__0Q2Tg') # .get('lang')
            # print(language)
            try: 
                rating = review.find('div', class_= 'styles_reviewHeader__iU9Px')['data-service-review-rating']
                header = review.find('h2', class_= 'typography_heading-s__f7029 typography_appearance-default__AAY17').text
                reviews_text = review.find('p', class_='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn').text
                date = review.find('p',class_= 'typography_body-m__xgxZ_ typography_appearance-default__AAY17').text.strip('Date of experience: ').strip('xperience: ')
                
                # Write the data as a row in the CSV file
                writer.writerow([date, rating, header, reviews_text])

                # Printing every 10ths review as a form of logging, will print 2 headers per page.
                if i % 10 == 0:
                    print(header)
            except: 
                continue
            
            
    