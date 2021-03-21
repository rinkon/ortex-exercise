# well, lets code..
import csv
from collections import defaultdict
import json


def process_monthly_transactions(monthly_transactions, total_transactions):
    grand_total = 0.0
    for item in monthly_transactions.items():
        monthly_transactions[item[0]] = 100 * (item[1] / total_transactions)
        grand_total += monthly_transactions[item[0]]

    return monthly_transactions


def get_max_excahnge_and_august_max_value_company(reader):
    exchanges = defaultdict(lambda: 0)
    august_value = defaultdict(lambda: 0.0)
    total_transactions = 0
    monthly_transactions = defaultdict(lambda: 0)
    month_dictionary = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                        '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov',
                        '12': 'Dec'}

    for row in reader:
        exchanges[row['exchange'].strip()] += 1

        trade_date = row['tradedate']
        if trade_date.startswith('201708'):
            august_value[row['companyName']] += float(row['valueEUR'])

        if trade_date.startswith('2017'):
            if row['tradeSignificance'] == '3':
                total_transactions += 1
                monthly_transactions[month_dictionary[trade_date[4] + trade_date[5]]] += 1

    monthly_transactions = process_monthly_transactions(monthly_transactions, total_transactions)

    return sorted(exchanges.items(), key=lambda kv: kv[1], reverse=True)[0][0], sorted(august_value.items(), key=lambda kv: kv[1], reverse=True)[0][0], monthly_transactions


def main():
    with open('2017.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        max_exchange, august_max_valueer_company, monthly_transactions = \
            get_max_excahnge_and_august_max_value_company(reader)

        print("What Exchange has had the most transactions in the file? \n" + max_exchange + "\n")
        print("In August 2017, which companyName had the highest combined valueEUR?\n" + august_max_valueer_company + "\n")
        print("For 2017, only considering transactions with tradeSignificance 3, what is the percentage of transactions per month?")
        for item in monthly_transactions.items():
            print("{0}, {1}%".format(item[0], item[1]))


if __name__ == '__main__':
    main()




