# FeNOMan Server
FeNOMan is a federated learning-driven traffic flow classification framework that preserves data privacy while providing comparable performance to a hypothetical, centralized, collaborative ML-based traffic classification solution for networking scenarios. The framework consists of two parts. One is the server side, where the global models are hosted and advertised. Clients will subscribe to this given server and start training based on the pre-setted configuration. 

## Table of Contents
* [Main Features](#main-features)
* [Installation](#installation)
    * [Prerequisite](#prerequisite)
* [Usage](#usage)
* [Credits](#credits)
  * [Authors](#authors)
* [Acknowledgement](#acknowledgement)
* [License](#license)

## Main Features

The server is able to advertise different models (due to the flower, the current version of the solution can only advertise one model at a time) which clients can download via HTTP/HTTPS (and API key authentication can be set up for the solution). Once the models are downloaded from the server, clients can use them for prediction or, if the server is advertised, they can teach and modify the weights of the global model. All the model information is stored in a NoSQL database and the solution can advertise the models by feeding from it. Each model state is time-stamped in the database and the latest one is always advertised unless the user requests to revert to an older one.

## Installation
Because of network card monitoring, the user must have super-user privileges to start the server. For this reason, it is necessary to install the required libraries by logging in as a super-user. Which can be done as follows:
```
sudo su
pip3 install -r requirements.txt
```

For the entry point of the core class, the permission must be changed in the tree to run with the following command:

```
chmod u+x /core/core.py
```

### Prerequisite
* Linux based operating system that supports NFStream
* MongoDB Server
* Python 3.9

## Usage
After a successful installation, be sure to adjust the configuration files to ensure that the solution works for your needs.
The following configuration files modify the following parameters:
* **application_configuration**
  * *HOST_URI* - *The basic IP address where to listen on the web server. May be empty if the scan is properly configured for the target device in nfstream_configuration.*
  * *HOST_PORT* - *Port number of the web server running in the background.*
  * *BASE_URI* - *For the web server, the API version number defined in the URLs.*
  * *OCP_APIM_KEY* - *Key value associated with api key authentication for API endpoints.*
* **data_configuration**
  * *DATA_URI* - *In the case of an input file which may have a .csv or .pcap extension, the path.*
  * *DROP_VARIABLES* - *The field values to be discarded from the measurement data. These names are listed in this parameter.*
  * *TARGET_VARIABLE* - *Name of the target variable.*
  * *TRAIN_VALIDATION_SPLIT* - *Percentage ratio of teaching and test data to resolution.*
  * *N_FEATURES* - *The number of identifiable featurs in the data set that are used in the model training.*
  * *REDUCE_REGEX_VARIABLES* - *For fields with names specified in the list, regular expression matching is used to filter the data.*
* **evaluation_configuration**
  * *EVALUATION_BATCH_SIZE* - *The batch size of the model used in the evaluation.*
  * *EVALUATION_LOCAL_EPOCHS_MINIMUM* - *Minimum number of epochs used during evaulation.*
  * *EVALUATION_LOCAL_EPOCHS_MAXIMUM* - *Maximum number of epochs used during evaulation.*
  * *EVALUATION_VALIDATION_STEP_MINIMUM* - *Minimum number of steps used in validation.*
  * *EVALUATION_VALIDATION_STEP_MAXIMUM* - *Maximum number of steps used in validation.*
  * *EVALUATION_FIT_CONFIG_ROUND_THRESHOLD* - *Threshold value of the fit during the evaulation step.*
  * *EVALUATION_VALIDATION_STEP_ROUND_THRESHOLD* - *Threshold value of the fit during the evaulation step during validation.*
  * *CONFUSION_MATRIX_LABELS* - *For the configuration matrix output, for which field values should the solution perform the analysis.*
* **flower_configuration**
  * *FRACTION_FIT* - *Fraction of clients used during training. In case min_fit_clients is larger than fraction_fit * available_clients, min_fit_clients will still be sampled.*
  * *FRACTION_EVAL* - *Fraction of clients used during validation. In case min_evaluate_clients is larger than fraction_evaluate * available_clients, min_evaluate_clients will still be sampled.*
  * *MIN_FIT_CLIENTS* - *Minimum number of clients used during training.*
  * *MIN_EVAL_CLIENTS* - *Minimum number of clients used during validation.*
  * *MIN_AVAILABLE_CLIENTS* - *Minimum number of total clients in the system.*
  * *NUM_ROUNDS* - *Determines how many teaches should be performed on clients during the run of a flower server.*
  * *SERVER_JOB_TIMER_MINUTES* - *This allows you to set the frequency at which the flower server is started by the web server.*
  * *SECURE_MODE* - *This enables the secure SSL connection between client and server.*
  * *FLOWER_SERVER_ADDRESS* - *The IPv4 or IPv6 address of the server.*
  * *FLOWER_SERVER_PORT* - *Servers port where to listen to the Flower clients. The web server and flower server ports cannot be the same!*
* **model_configuration**
  * *MODEL_NAME* - *The fictitious name associated with the model, which is used to load the model into the database. It is very important to properly identify the different models.*
  * *MODEL_BATCH_SIZE* - *The batch size for the model.*
  * *MODE_EPOCHS* - *The number of epochs associated with teaching the model.*
* **nfstream_configuration**
  * *SOURCE* - *Network target device that can be monitored by the system in case there is no file-based input to the solution.*
  * *STATISTICAL_ANALYSIS* - *Statistical analysis applied to the sampled streams.*
  * *SPLT_ANALYSIS* - *For the analysis of early flow characteristics, for how many data sets should the system perform the analysis of early flow characteristics.*
  * *COLUMNS_TO_ANONYMIZE* - *The names of the columns to which anomalisation should be applied during the capture.*
  * *MAX_NFLOWS* - *The maximum number of flows that the procedure will sample from the target device using NFStream.*
* **nosql_database_configuration**
  * *DATABASE_HOST* - *The address associated with the database. In case the server and the database are running from a shared resource, localhost can be used in text format.*
  * *DATABASE_PORT* - *The database port number.*
  * *DATABASE* - *Textual name of the database.*
  * *COLLECTION* - *The name of the collection within the database where the models will be stored and read from.*

Once the configuration is adequately parameterised, the solution can be easily run with the following command, which also requires the super-user:
```
python3 wsgi.py
```

If you have your own model, you need to do the code-level modification in the model definition block in the model/model.py class. If there is an existing model, it can be loaded into the database, or it can be directly loaded instead of code-level implementation.
For a simple dense layer model, this should look like the following:
```python
32 ########################################
33 ### Internal model definition block. ###
34 ########################################
35 self.__model = tf.keras.Sequential()
36 self.__model.add(tf.keras.layers.Dense(13, input_dim=13, activation='relu'))
37 self.__model.add(tf.keras.layers.Dense(500, activation='softmax'))
38 self.__model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
39 ########################################
40 ### Internal model definition block. ###
41 ########################################
```

## Credits
### Authors
* Adrian Pekar
* Zied Aouini
* Laszlo Arpad Makara
* Gergely Biczok
* Balint Bicski
* Marcell Szoby
* Mate Simko

## Acknowledgement
Supported by the GÉANT Innovation Programme 2022.

## License
This project is licensed under the LGPLv3 license - see the [License](LICENSE) file for details.
