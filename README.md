# ConsoleLog_Graphgenerator
Webapp to generate graphs from Arma 3 server logs

## Installation
###  Clone this repository and run the following command to install the required packages:
```
pip install -r requirements.txt
```
### Then run the following command to start the website:
```
streamlit run ./streamlit.py
```
### Add your logs to the logs folder with the following structure:  
log_data  
├── Operation  
│   ├── server_console.log  
│   ├── arma3server.rpt  
├── Operation2  
│   ├── server_console.log  
│   ├── arma3server.rpt  

### Navigate to http://localhost:8501/ and select the log you want to generate a graph for. 