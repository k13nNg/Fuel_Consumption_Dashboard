# Fuel_Consumption_Dashboard

This dashboard aims to offer more insights on the fuel consumption of Plug-in Hybrid Vehicles in Canada, with model year ranging from 2012 to 2024.

The dataset was obtained from the Open Canadian Government Portal (https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64)

The .csv file of the dataset (named "dataset") is attached in this repository.

# Viewing the dashboard

There are two options to view the dashboard:\
    <ol>
        <li>Online via [this link](https://fuel-consumption-dashboard-phd0.onrender.com/) (Please give the website up to 1 minute to load)</li>
        <li>Locally</li>
    </ol>

To view the dashboard locally, please following the following steps:
    <ol>
        <li>Clone this project</li>
        <li>Install all the required dependencies in the requirements.txt file using pip</li>
        <li>Go to the project folder and run the app.py file</li>
        <li>Follow the link in the terminal (usually http:127.0.0.1:8050) to access the dashboard</li>
        <li>Enjoy the beautiful plots and graphs!</li>
    </ol>

# Conclusions and Analysis

Below are a few conclusions I was able to draw when creating and analyzing this dataset:
<ul>
    <li>In general, a Mid-size and Small SUV cars are the two most popular vehicle classes in this dataset. The dataset includes 67 Mid-size and 63 Small SUV car models</li>
    <li>Minicompact class was the least popular class in this dataset. Only 1 model from the manufacturer Polestar was included in this dataset</li>
    <li>Volvo has the most variety of vehicle classes being tested in this dataset. Car models from across 5 classes were included in this dataset</li>
    <li>There appears to be a positive correlation between the year model and the number of models included in the dataset</li>
</ul>

# Notes

This dashboard is using plotly - a Python library for data visualization and dashboard creation. Thus, it is interactive!\
Here are a few tips to best use the interactiveness of the dashboard:
    <ol>
        <li>Double-click on an item in legend would help isolate the graph for that only item!</li>
        ![2024-02-23 23 29 14](https://github.com/k13nNg/Fuel_Consumption_Dashboard/assets/75595156/0a1eefb3-af01-48a5-8fe6-c358aad706e8)
        <li>Once you have isolated an item for view on a graph, you can add other items for comparison by single-click each item\
        ![2024-02-23 23 30 53](https://github.com/k13nNg/Fuel_Consumption_Dashboard/assets/75595156/46011c91-6828-4908-aa16-7aac4ac0e631)</li>
        <li>Hovering over the individual vehicle class in the "Vehicle Classes in the dataset" graph would give you detailed information about the models and manufacturers for that class in the graph "Unique Models from Each Manufacturers"\
        ![2024-02-23 23 34 12](https://github.com/k13nNg/Fuel_Consumption_Dashboard/assets/75595156/b37c1abd-a586-4c41-8a6c-4806d375c29b)

 </li>
    </ol>
