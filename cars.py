#!/usr/bin/env python3

import json
import locale
import sys
import emails
import os
import reports


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])

def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    
    # TODO: also handle max sales
  

  max_sales = {"max_sales": 0}
  for item in data:
    item_sales = item["total_sales"]
    if item_sales > max_sales["max_sales"]:
        item["max_sales"] = item_sales
        max_sales = item
    
    # TODO: also handle most popular car_year

  pop_year = 0
  pop_yr_max = 0
  sales_yr = {}
  for item in data:
    item_yr = item["car"]["car_year"]
    total_sales = item["total_sales"]
    if item_yr not in sales_yr:
      sales_yr[item_yr] = total_sales
      
    else:
      sales_yr[item_yr] += total_sales
  for tot_yr in sales_yr.keys():
    if sales_yr[tot_yr] > pop_yr_max:
      pop_year = tot_yr
      pop_yr_max = sales_yr[tot_yr]

  pop_car_yr = { pop_year: pop_yr_max }

  summary1 = "The {} generated the most revenue: ${}".format(format_car(max_revenue["car"]), max_revenue["revenue"])
  summary2 = "The {} had the most sales: {}".format(format_car(max_sales["car"]), max_sales["max_sales"])
  summary3 = "The most popular year was {} with {}.".format(pop_year, pop_yr_max)
   
  return summary1, summary2, summary3
  
def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data

def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  print(summary)
    
  # TODO: turn this into a PDF report
  summary_pdf = "<br/>".join(summary)
  
  reports.generate("/tmp/cars.pdf", "Sales Data", summary_pdf, cars_dict_to_table(data))

  # TODO: send the PDF report as an email attachment

  sender =  "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body =  "\n".join(summary)
  
  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)

if __name__ == "__main__":
  main(sys.argv)
