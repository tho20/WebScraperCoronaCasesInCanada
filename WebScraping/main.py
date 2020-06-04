from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def webpage_url(my_url: str):

    """
    Returns HTML content of the desired url

    :param my_url: desired url page (String)
    :return: HTML content of the page

    """

    uClient = uReq(my_url)  # Opening connection and grabbing the page
    html_page = uClient.read()  # contents of page
    uClient.close()
    return html_page


def get_data(html_page):

    """
    Gets the desired data from the HTML content. In this case, the statistics of
    Covid19 in Canada.

    :param html_page: HTML content of a URL page
    :return: tuple containing time the data was collected and dictionary
    containing the wanted data.

    """

    dic_data = {}
    page_soup = soup(html_page, "html.parser")
    all_data = page_soup.find_all("div", {"id": "covid19TableContent"})

    current_time = all_data[0].table.caption.time.text.replace(",", "")
    table_data = all_data[0].table.tbody.find_all("tr")

    for row in table_data:
        contents = row.find_all("td")

        place = contents[0].text
        nb_confirmed_cases = contents[1].text.replace(",", "")
        nb_of_deaths = contents[3].text.replace(",", "")

        dic_data[place] = (nb_confirmed_cases, nb_of_deaths)

    return current_time, dic_data


def write_into_csv(contents):

    """
    Writes the data retrieved from URL contents of the page into CSV file
    coronavirusInCanada.csv located in the same directory. Previous data might
    already have been added.

    :param contents: tuple containing time the data was collected and dictionary
    containing the wanted data
    :return: None
    """

    date, dic = contents

    with open('coronavirusInCanada.csv', mode='a') as coronaFile:

        headers = "Date:" + "," + date + "\n"
        coronaFile.write(headers)
        coronaFile.write("\n")
        coronaFile.write("Province/Territory/Other, Number of confirmed Cases,"
                         " Number of deaths \n")

        for place in dic:
            coronaFile.write(place + "," + dic[place][0] + "," +
                             dic[place][1] + "," + "\n")

        coronaFile.write("\n")
        coronaFile.write("\n")

    coronaFile.close()


if __name__ == "__main__":  # Runs Program

    page = webpage_url("https://www.canada.ca/en/public-health/services/"
                       "diseases/2019-novel-coronavirus-infection.html")
    data = get_data(page)
    print(data)
    write_into_csv(data)
