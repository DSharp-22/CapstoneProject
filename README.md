# CapstoneProject Repository

## Overview
This repository contains all the relative files I have created for my senior capstone project at Eastern University. The project itself was a cloud based data pipeline involving certain cryptocurrency and stock information. I used CoinGecko's API to obtain the cryptocurrency information and Finnhub's API to obtain the stock information. Based on the call rate limits for the API's I had to choose 10 coins to examine in this project, as well as 7 stocks. I had chosed certain stocks to examine potential relationships between certain coins and stocks. After the database was built and being populated on a schedule, a Grafana dashboard was built to visualize the data allowing for the user to draw insights.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python, SQL |
| Database | PostgreSQL, pgAdmin, AWS RDS |
| Visualization | Grafana |
| AWS | RDS, Lambda, EventBridge |
| OS & Tools | Linux, Git, pgAdmin |
| APIs | CoinGecko API, Finnhub API |

## Process
I created a database on pgAdmin which was hosted originally on my local machine. Then I connected my pgAdmin database to Amazon RDS to utilize it's cloud hosting capabilities. Once the instances were connected, I then used AWS Lambda to automate the 4 python scripts that ingest the data from CoinGecko and Finnhub's API's into my database. I put them all in their own unique lambda function and then used Amazon EventBridge to set up a schedule for each of the scripts to run and pull that information on a calculated interval to ensure I stayed within API call rate limits for both sources. Once that part of the pipeline was running smoothly, I then connected my postgreSQL database to Grafana, which I had used to construct a dashboard of visualizations for the data that would allow for useful insights to be made by the user. The Grafana dashboard is linked here: https://bb22davidsharp.grafana.net/public-dashboards/e8509e98d88f4abca8c83eb074968c23 

