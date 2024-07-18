# Educational-Big-Data-Projects
Educational Big Data Projects

* 姓名：徐嫚謙
* 系級：科技114級
* 授課老師：Pecu


# A blockchain transaction visualization tool ( 暫定 )
> A method for visual analysis of token transaction data on the blockchain to easily identify suspicious transactions.
## Installation Guide
Please follow the steps below to install and configure this project :

**STEP 1 :** 
```
git clone https://github.com/Manchien/Educational_Big_Data_Projects.git
```

**STEP 2 :** Setup virtual environment and install dependencies using `pip install -r requirements.txt`

**STEP 3 :** Replace the credentials in .env file with your own API_KEYS

## User Guide

[🎞️Video demonstration part1](https://www.youtube.com/watch?v=dn8486sFMFc)
、[part2](https://www.youtube.com/watch?v=zS_y-KyNy0o)

Here are instructions on how to use this project.

### Data Collection： 

**Obtaining Multi-layer Historical Transaction Data for a Wallet :**
1. Copy the wallet address(es) you want to track and paste them into the INITIAL_ADDRESSES in the main function on line 84 of the file `data_collection.py`.

2. Modify the `MAX_DEPTH` parameter in .env file according to the maximum number of layers you want to track.

3. Adjust the `TX_COUNT_THRESHOLD` in .env to set the number of transactions per layer you want to track ( Note : If no limit is set, the process may take several hours).

4. Run the script:
```
py data_collection.py
```
5. Obtain the CSV file.

**Obtaining Single-layer Historical Transaction Data for a Wallet :**
1. Directly download the transaction data from [Etherscan](https://etherscan.io/).

### Data Visualization：
### Examples of how to use the tool
> [What Addresses are Potential Fraud Accounts?](https://github.com/Manchien/Educational_Big_Data_Projects/blob/bb88f7e49d3e4d47b09c05a2c13fa7d15cdcbbe1/docs/example.pdf)
> 
