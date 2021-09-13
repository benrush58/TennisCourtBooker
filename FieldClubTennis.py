import time

import requests
import copy
from bs4 import BeautifulSoup
import datetime

s = requests.Session()


courtToID = {
    "1": "AMN-0ee28cd9468647b7b1accba1fead3e72",
    "2": "AMN-b32bb58931074c6890c6b8c244183c36",
    "3": "AMN-57f6aaca23c549508cb1bf6d375ee812",
    "4": "AMN-f46e138c469c4448add4e85c6cfc02dc",
    "5": "AMN-48504daf5be14584bd9cc47186644a32",
    "6": "AMN-c3c8391fb3374e52a1eacdcc8f5ca061",
    "7": "AMN-c9062125cb194f8ea909076a0604c328",
    "8": "AMN-13bb3775d19940ff9cd598987d256e4b",
    "9": "AMN-1153be273cf54bbfb7ac67c2337c7c49",
    "10": "AMN-d46bb0081176476f8abc9d991317d0b8",
    "11": "AMN-b587a16705f2494986f99aeb63a904b2",
    "12": "AMN-0d75bc81438742dfae92c3b8ae799306",
    "13": "AMN-4ad79343c76e40dea24b5f023a520e3b",
    "14": "AMN-dfd2c3bb64204557ab62316b797ad303",
}

IDToCourt = {
    "AMN-0ee28cd9468647b7b1accba1fead3e72": "1",
    "AMN-b32bb58931074c6890c6b8c244183c36": "2",
    "AMN-57f6aaca23c549508cb1bf6d375ee812": "3",
    "AMN-f46e138c469c4448add4e85c6cfc02dc": "4",
    "AMN-48504daf5be14584bd9cc47186644a32": "5",
    "AMN-c3c8391fb3374e52a1eacdcc8f5ca061": "6",
    "AMN-c9062125cb194f8ea909076a0604c328": "7",
    "AMN-13bb3775d19940ff9cd598987d256e4b": "8",
    "AMN-1153be273cf54bbfb7ac67c2337c7c49": "9",
    "AMN-d46bb0081176476f8abc9d991317d0b8": "10",
    "AMN-b587a16705f2494986f99aeb63a904b2": "11",
    "AMN-0d75bc81438742dfae92c3b8ae799306": "12",
    "AMN-4ad79343c76e40dea24b5f023a520e3b": "13",
    "AMN-dfd2c3bb64204557ab62316b797ad303": "14",
}


def login():
    # Get the username and password
    f = open("credentials.txt", "r")
    username = f.readline()
    password = f.readline()
    f.close()

    #Get cookies and CSRF Token
    tokenUrl = "https://login.reservemycourt.com/login"
    response = s.get(tokenUrl)
    soup = BeautifulSoup(response.text, "html.parser")

    token = soup.find("meta", attrs={"name": "csrf-token"})
    tokenFinal = str(token)[15:55]

    cookies = response.headers["Set-Cookie"]
    cookiesList = cookies.replace(",", ";")
    cookiesSplit = cookiesList.split(";")
    cookieTotal = cookiesSplit[0] + ";" + cookiesSplit[6] + ";" + cookiesSplit[13]
    headersLogin = {
        "authority": "login.reservemycourt.com",
        "method": "POST",
        "path": "/login",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-length": "97",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": cookieTotal,
        "origin": "https://login.reservemycourt.com",
        "referer": "https://login.reservemycourt.com/login",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }

    dataLogin = {
        "_token": tokenFinal,
        "email": username,
        "password": password
    }

    websiteLogin = "https://login.reservemycourt.com/login"

    response = s.post(websiteLogin, headers=headersLogin, data=dataLogin)
    return response


# Function gets the calender of the day requested
def calender(date):
    response = login()
    calUrl = "https://app.reservemycourt.com/clubs/CLB-299e4786f534461ea8b2dce22bbe1b46/fullCalendarReservations/" + date
    cal = s.get(calUrl)
    for x in cal.json():
        start = x.get("start").split(" ")
        end = x.get("end").split(" ")
        print("Court " + IDToCourt[x.get("resourceId")] + ": " + start[1] + "-" + end[1])


def wait():
    timeRun = input("What time would you like the code to run? For example, 0:00 is midnight and 17:00 is 5pm\n")
    timeSplit = timeRun.split(":")
    timeRunFinal = datetime.time(int(timeSplit[0]), int(timeSplit[1]), 0, 0)
    print(timeRunFinal)
    now = datetime.datetime.now()
    while now.minute != timeRunFinal.minute or now.hour != timeRunFinal.hour:
        now = datetime.datetime.now()
        print("Waiting to run code at " + str(timeRunFinal))
        time.sleep(10)



def main():
    date = input("What date do you want to play? Type in the form of YYYY-MM-DD\n")
    datePicker = input("Enter date of play in the form of Tuesday, Aug 31st, 2021\n")
    reservations = input("Would you like to see what court times have already been booked on that day? yes or no\n")
    if reservations == "yes":
        calender(date)
    timeFinal = input("What time would you like to play? Enter in the form X:XX A/PM. For example, 7:30 PM\n")
    start = date + " " + timeFinal
    duration = input("How many minutes you want to book the court for. Just type the digits. For example, 60\n")
    courtNumber = input("What court do you want to book? For example, 5 or 12\n")
    type = input("Singles or Doubles? Capitalize the word\n")
    number = input("How many people? For example, 2 or 4\n")
    yesOrNo = input("Would you like the code to run now or at a different time? yes for now, and no for later\n")
    if yesOrNo == "no":
        wait()
    login()

    cook = s.get("https://app.reservemycourt.com/reservations")
    cookies = cook.headers["Set-Cookie"]
    cookiesList = cookies.replace(",", ";")
    cookiesSplit = cookiesList.split(";")
    cookieTotal2 = cookiesSplit[0] + ";" + cookiesSplit[6] + ";" + cookiesSplit[13]


    # Getting the CSRF token
    tokenUrl = "https://app.reservemycourt.com/reservations"
    response = s.get(tokenUrl)
    soup = BeautifulSoup(response.text, "html.parser")

    token = soup.find("meta", attrs={"name":"csrf-token"})
    tokenFinal = str(token)[15:55]

    headersBook = {
        "authority": "app.reservemycourt.com",
        "method": "POST",
        "path": "/reservations",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "629",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": cookieTotal2,
        "origin": "https://app.reservemycourt.com",
        "referer": "https://app.reservemycourt.com/clubs/CLB-299e4786f534461ea8b2dce22bbe1b46/reservations",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }


    dataBook = {
        "_token": tokenFinal,
        "start": start,
        "datePicker": datePicker,
        "startPicker": timeFinal,
        "duration": duration,
        "interval": "Day",
        "repeat": "1",
        "amenityIdCheck": courtToID["1"],
        "amenities[]": courtToID[courtNumber],
        "private": "1",
        "authUser": "USR-2319a6d3c81d4827be0cae5cdca33852",
        "use_type": type,
        "owner_user_id": "USR-2319a6d3c81d4827be0cae5cdca33852",
        "attendee_id": "USR-2319a6d3c81d4827be0cae5cdca33852",
        "event_type_id": "",
        "participant_count": number,
        "notes": "",
        "pro_id": "USR-2319a6d3c81d4827be0cae5cdca33852",
        "description": "",
        "min_participants": "1",
        "max_participants": "2",
        "clinic_fee_id": "",
        "private": "0",
        "join_all_required": "0",
    }

    websiteBook = "https://app.reservemycourt.com/reservations"

    response = s.post(websiteBook, headers=headersBook, data=dataBook)

    print(response.text)

main()

