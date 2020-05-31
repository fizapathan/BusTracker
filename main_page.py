#importing the request libraries
import requests
#importing the libraries required for web making
from flask import Flask, render_template, request
import os
import psycopg2
import numpy as np
app = Flask(__name__)

@app.route('/')
@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    return render_template('main_page.html')
    
#@app.route('/make_wallet_bal')
#def make_wallet_bal():
#    query="""
"""mutation update_user($stations: Int!, $money: Int!) {
  update_user_details(where: {user_id: {_eq: 123}}, _set: {no_of_stations_passed: $stations, wallet_bal: $money}) {
    affected_rows
    returning {
      no_of_stations_passed
      wallet_bal
    }
  }
}
"""
#    make_hasura_req(query, variables)
#    return


def make_hasura_req(query, variables):
    r=requests.post(url="https://wnm-hackathon.herokuapp.com/v1/graphql", json={"query":query, "variables":variables})
    response=r.json()
    print(response)
    return response['data']

#def make_hasura_req1():
#    r1=requests.get(url="https://wnm-hackathon.herokuapp.com/v1/graphql")
#    response1=r1.json()
#    print(response1)
#    return response1['data']


@app.route('/bus_availability')
def bus_availability():
    #api-endpoint
    URL="https://transit.api.here.com/v3/stations/by_name.json"
    #defining a PARAMS dict for the parameters to be sent to the API
    PARAMS= {
    'center': '40.7510,-73.9916',
    'name': 'union',
    'app_id': 'wweb8wBbFVGuEezx93lQ',
    'app_code': 'Ik0Ljhr6y0t0n5EOpaXOXw',
    'max': '10',
    'method': 'fuzzy',
    'radius': '5000'
    }
    # sending get request and saving the response as response object
    r = requests.get(url = URL,params = PARAMS) 
    #extracting data in json format
    data = r.json()


    #To sort the stations based on duration which is the length of 
    #that leg of the travel
    Stn = data["Res"]["Stations"]["Stn"]
    flag=0
    ans=dict()
    for i in range(len(Stn)):
        s=""
        flag=0
        for j in range(len(Stn[i]["duration"])):
            mult=60*60
            if(ord(Stn[i]["duration"][j])<=90 and ord(Stn[i]["duration"][j])>=65):
                if(flag==1):
                    if(s!=""):
                        ans[i+1]=(int(s))*mult
                        mult/=60
                    s=""
                flag=1
                continue
            else:
                s+=Stn[i]["duration"][j]
    bus_list = sorted(ans,key=ans.__getitem__)
    return render_template('bus_availability.html', bus_sorted_list=bus_list)

@app.route('/loginpage')
def loginpage():
    return render_template('login_page.html')

@app.route('/wallet_bal')
def wallet_bal():
  balance = 10
  query="""{
  user_details {
    user_id
    user_firstname
    wallet_bal
  }
}
"""
  data = make_hasura_req(query, {})
  balance = data['user_details'][0]['wallet_bal']
  return render_template('wallet_bal.html', balance=balance)

if __name__ == "__main__":
    app.run(debug=True,port=3000)

