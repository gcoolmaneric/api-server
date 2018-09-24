# Get Started  

First step you need to set up database settings for mysql in folder /settings/env.yaml
Please modify it as below

```
dev:
    database-ip: 127.0.0.1
    database-port: 8889
    database-user: root
    database-password: root
    database-name: shop-db
```

Modify config.py

Set up your env name to match env.yaml accordingly such as dev, sandbox, qa or production

You can adjust this parameters when you deploy apiserver to your cloud's environment.

For example, if you use Google Cloud, ENV_NAME can be setup by your projectId. 

Project Id can be dynamically determinated by your deployment commands.

For local testing, please set it as "dev" below

```
ENV_NAME = 'dev'
```

## Install libs

```
./script/install.sh
```

## Import Table into MYSQL

```
./script/import_model.sh
```

# Run Pytest Unit-Test

```
./script/test.sh
or
source env/bin/activate
pytest tests
```

## Run

If you want to run apiserver at local, execute the following scripts.

```
source env/bin/activate
python main.py

```

Once you start the apiserver, it would open port at 8080.

You can test REST APIs as below

### Create list

http://127.0.0.1:8080/shop/api/v1/create_list

### Update list

http://127.0.0.1:8080/shop/api/v1/update_list

### Delete list

http://127.0.0.1:8080/shop/api/v1/delete_list

### Add Items to list

http://127.0.0.1:8080/shop/api/v1/add_items

### Get all Shopping lists

http://127.0.0.1:8080/shop/api/v1/get_all_lists

### Get the Shopping lists by itemId, multiple titles or item names

http://127.0.0.1:8080/shop/api/v1/get_lists


### Test 

To save your time to test REST APIs, you can insatll Chrome's plugin postman bewlow.

Insatll postman for Chrome 

https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en


Download the following config file and import it into postman to test APIs. 

https://drive.google.com/file/d/1J94AeGgkzsbhDkM_4y_ycN5soMPnb5VV/view?usp=sharing


# Design  

ShoppingList APIs send to ShoppingService which would process requests and use
three different data models services to meet business needs.

```
API --> ShoppingService <--> ShoppingListService      <-->  ShoppingList      <--> DatabaseManager <--> ORM  <-->  MYSQL
                        <--> ShoppingListItemService  <-->  ShoppingListItem
                        <--> ItemService              <-->  Item
```
ShoppingService: Act as an interface to process all ShoppingList business logic

ShoppingListService, ShoppingListItemService, ItemService: define any operations on data models  

ShoppingList, ShoppingListItem, Item: data model class

DatabaseManager: act as an interface to ORM because all the database's operations will be executed by this class.
This would help us reuse database connection and cache data improve performance in the future if needed.


# Database Table Design

ShoppingListItem table records the relationship between ShoppingList and Item table.
So as we can query ShoppingList's itemId or item name by joining the following three tables.

### Table: ShoppingList

Column | Type  | Description
--------- | ----- | -----------
id    |  integer | Primary key
title |  string    | title
shop_name |  string    | store name
date |  datetime    | created date time

### Table: Item

Column | Type  | Description
--------- | ----- | -----------
id    |  integer | Primary key
name |  string    | item name
quantity |  integer   | item's quantity

### Table: ShoppingListItem

Column | Type  | Description
--------- | ----- | -----------
id    |  integer | Primary key
shop_list_id |  integer    | ShoppingList's id
item_id |  integer    | Item's id

### Table Index:

To improve the performance, we set up the following indexes to query.

Table | Column  |  Type
--------- | ----- | -----------
Item    |  name |  string
ShoppingListItem |  shop_list_id | integer
ShoppingListItem |  item_id | integer
ShoppingList |  title | string


# Code Structure

- /apiserver/api/shop.py : api endpoints

- /apiserver/model/load_model.py : define 3 data models including ShoppingListItem, ShoppingList, and Item

- /apiserver/service/item_service.py: define operations for Item data model

- /apiserver/service/shopping_list_item_service.py: define operations for ShoppingListItem data model

- /apiserver/service/shopping_list_service.py: define operations for ShoppingList data model

- /apiserver/service/shopping_service.py: act as an interface to process all Shopping API's business logic

- /apiserver/utils/database_manager.py: an interface to communicate with ORM and database.
     - By using this class, you can easily cache read data in memacahe to improve performance cos all the data models would use this class
     - Use singleton to reuse the database's connection to improve performance

- /apiserver/utils/render.py: define REST API's error and response code

- /script/install.sh: a script to install necessary libs

- /script/import_model.sh: a script to import table into your database

- /script/test.sh: a script to run pytest

- /settings/config.py: load env.yaml into app; remember ENV_NAME is dependent on your envs, you can set it up by your cloud's Project Id if you use Google to identify different envs

- /settings/env.yaml:  define database settings
  - This file can be saved on your CDN; download this when doing deployment

- /tests/conftest.py: define what functions, model or class can be shared and tested by pytest

- /tests/test_item_service.py:  unit-test cases for Item service class

- /tests/test_shop_api.py: unit-test cases for all the shopping list apis and ShoppingListItem service class

- /tests/test_shopping_list_service.py: unit-test cases for ShoppingList service class


# REST API

### API: /shop/api/v1/create_list

### Request Parameters:

| Parameter | Type | description |
| --- | ----------- |----------- |
| name | string | store name |
| title | string | title |

### Example:

```
{
  "title":"Shopping Store1",
  "name":"Shopping Name1"
}

```

### Response Parameters

Parameter | Type  | Description
--------- | ----- | -----------
status    |  integer | 200 means success otherwise not 200 means an error such as 4XX, 5XX.
data      |  json    | Successful JSON payload

### Successful JSON Payload

Parameter | Type  | Description
--------- | ----- | -----------
id    |  integer | Shopping List's id


### Example:

```
{
    "status": 200,
    "data": {
        "id": 23
    }
}
```

### Error Response Parameters

Returns an error in JSON data structured like this:

```
[
 {  
  "status": 400,
  "reason": "title is null"
 }
]
```

Parameter | Type | Description
--------- | -----| -----------
status    |  integer | 4XX, 5XX.
reason    |  string / json  | a string of error reason / error's reasons in JSON while invalid request


Error Status | Error Reason | Description
--------- | -----| -----------
400    |  invalid_request | function name is null or function parameters are null
500    |  Internal server error | Internal server error


### API: /shop/api/v1/update_list

### Request Parameters:

| Parameter | Type | description |
| --- | ----------- |----------- |
| listId | integer | ShoppingList's id|
| title | string | title |
| name | string | store name |

### Example:

```
{
  "listId": 23,
	"title": "ShoppingList title2",
  "name": "ShoppingList name2"
}

```

### Response Parameters

Parameter | Type  | Description
--------- | ----- | -----------
status    |  integer | 200 means success otherwise not 200 means an error such as 4XX, 5XX.
data      |  json    | Successful JSON payload

### Successful JSON Payload

Parameter | Type  | Description
--------- | ----- | -----------
id  | integer | ShoppingList's id
shop_name  | string | store name
title  | string | title
date  | string | date

### Example:

```
{
    "status": 200,
    "data": {
        "shop_name": "ShoppingList name2",
        "id": 23,
        "date": null,
        "title": "ShoppingList title2"
    }
}

```

### Error Response Parameters

Returns an error in JSON data structured like this:

```
[
 {  
  "status": 400,
  "reason": "title is null"
 }
]
```


Parameter | Type | Description
--------- | -----| -----------
status    |  integer | 4XX, 5XX.
reason    |  string / json  | a string of error reason / error's reasons in JSON while invalid request


Error Status | Error Reason | Description
--------- | -----| -----------
400    |  invalid_request | request parameters are null
404    |  data_does_not_exist | shopping list is null
500    |  Internal server error | Internal server error


### API: /shop/api/v1/delete_list

### Request Parameters:

| Parameter | Type | description |
| --- | ----------- |----------- |
| listId | integer | ShoppingList's id|

### Example:

```
{
  "listId": 23
}

```

### Response Parameters

Parameter | Type  | Description
--------- | ----- | -----------
status    |  integer | 200 means success otherwise not 200 means an error such as 4XX, 5XX.
data      |  json    | Successful JSON payload

### Successful JSON Payload

Parameter | Type  | Description
--------- | ----- | -----------
id  | integer | ShoppingList's id
shop_name  | string | store name
title  | string | title
date  | string | date

### Example:

```
{
    "status": 200,
    "data": "ok"
}

```

### Error Response Parameters

Returns an error in JSON data structured like this:

```
[
 {  
  "status": 400,
  "reason": "list_id is null"
 }
]
```


Parameter | Type | Description
--------- | -----| -----------
status    |  integer | 4XX, 5XX.
reason    |  string / json  | a string of error reason / error's reasons in JSON while invalid request


Error Status | Error Reason | Description
--------- | -----| -----------
400    |  invalid_request | request parameters are null
404    |  data_does_not_exist | shopping list is null
500    |  Internal server error | Internal server error


### API: /shop/api/v1/add_items

### Request Parameters:

| Parameter | Type | description |
| --- | ----------- |----------- |
| listId | string | ShoppingList's id |
| items | object | items objects |

### Example:

```
{
	"listId": 23,
    "items": [
       {"name": "banana", "quantity": 1},
       {"name": "apple", "quantity": 1}]
}

```

### Response Parameters

Parameter | Type  | Description
--------- | ----- | -----------
status    |  integer | 200 means success otherwise not 200 means an error such as 4XX, 5XX.
data      |  json    | Successful JSON payload

### Successful JSON Payload

Parameter | Type  | Description
--------- | ----- | -----------
items    |  list | a list of item objects
shopping_list    |  list | a list of ShoppingList objects

### Example:

```
{
    "status": 200,
    "data": {
        "items": [
            {
                "name": "banana",
                "quantity": "1",
                "id": 4
            },
            {
                "name": "apple",
                "quantity": "1",
                "id": 5
            }
        ],
        "shopping_list": [
            {
                "shop_name": "Shopping Name1",
                "id": 23,
                "date": 1537789806000,
                "title": "Shopping Store1"
            }
        ]
    }
}

```


### Error Response Parameters

Returns an error in JSON data structured like this:

```
[
 {  
  "status": 400,
  "reason": "title is null"
 }
]
```


Parameter | Type | Description
--------- | -----| -----------
status    |  integer | 4XX, 5XX.
reason    |  string / json  | a string of error reason / error's reasons in JSON while invalid request


Error Status | Error Reason | Description
--------- | -----| -----------
400    |  invalid_request | request parameters are null
404    |  data_does_not_exist | shopping list is null
500    |  Internal server error | Internal server error


### API: /shop/api/v1/get_all_lists

### Request Parameters:

| Parameter | Type | description |
| --- | ----------- |----------- |
| limit | integer | maximum number of ShoppingList objects to be returned |
| cursor | integer | the index of beginning position to query|

### Example:

```
{
  "limit": 10,
  "cursor": 5
}

```

### Response Parameters

Parameter | Type  | Description
--------- | ----- | -----------
status    |  integer | 200 means success otherwise not 200 means an error such as 4XX, 5XX.
data      |  json    | Successful JSON payload

### Successful JSON Payload

Parameter | Type  | Description
--------- | ----- | -----------
items    |  list | a list of item objects
shopping_list  |  list | a list of ShoppingList objects
next_page  |  integer | current position; if cursor+limit > maximum row, then None

### Example:

```
{
    "status": 200,
    "data": {
        "shopping_list": [
            {
                "shop_name": "test-name2",
                "id": 40,
                "date": null,
                "title": "test-title2"
            },
            {
                "shop_name": "test-name1",
                "id": 39,
                "date": null,
                "title": "test-title1"
            },
            {
                "shop_name": "test-name22",
                "id": 38,
                "date": null,
                "title": "test-title22"
            }
        ],
        "next_page": 8
    }
}

```


### Error Response Parameters

Parameter | Type | Description
--------- | -----| -----------
status    |  integer | 4XX, 5XX.
reason    |  string / json  | a string of error reason / error's reasons in JSON while invalid request


Error Status | Error Reason | Description
--------- | -----| -----------
400    |  invalid_request | request parameters are null
500    |  Internal server error | Internal server error


### API: /shop/api/v1/get_lists

Get a shopping list by searching one or multiple titles or itemId or itemName

### Request Parameters:

| Parameter | Type | description |
| --- | ----------- |----------- |
| findType | string | Choose which method to search by title, itemId, or itemName|
| title | string | search by title |
| itemId | integer | search by itemId |
| itemName | string | search by itemName |


### Response Parameters

Parameter | Type  | Description
--------- | ----- | -----------
status    |  integer | 200 means success otherwise not 200 means an error such as 4XX, 5XX.
data      |  json    | Successful JSON payload

### Successful JSON Payload

Parameter | Type  | Description
--------- | ----- | -----------
items    |  list | a list of item objects
shopping_list  |  list | a list of ShoppingList objects
items  |  list | a list of Item objects

### Example:

#### Search ShoppingList by multiple titles

```
Request:
{
  "findType": "title",
  "title": "Shopping Title4, Shopping Title5",
  "itemId": 0,
  "itemName": ""
}

Response:
{
    "status": 200,
    "data": {
        "items": [
            {
                "name": "banana",
                "id": 4,
                "quantity": "1"
            },
            {
                "name": "apple",
                "id": 5,
                "quantity": "1"
            }
        ],
        "shopping_list": [
            {
                "date": 1537786363000,
                "title": "Shopping Title4",
                "id": 10,
                "shop_name": "Shopping Name4"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title5",
                "id": 11,
                "shop_name": "Shopping Name5"
            }
        ]
    }
}

```

#### Search ShoppingList by ItemId

```
Request:
{
  "findType": "itemId",
  "title": "",
  "itemId": 4,
  "itemName": ""
}

Response:

{
    "status": 200,
    "data": {
        "items": [
            {
                "name": "banana",
                "id": 4,
                "quantity": "1"
            }
        ],
        "shopping_list": [
            {
                "date": 1537786362000,
                "title": "Shopping Title",
                "id": 6,
                "shop_name": "Shopping Name"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title",
                "id": 8,
                "shop_name": "Shopping Name"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title",
                "id": 9,
                "shop_name": "Shopping Name"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title4",
                "id": 10,
                "shop_name": "Shopping Name4"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title5",
                "id": 11,
                "shop_name": "Shopping Name5"
            }
        ]
    }
}

```


#### Search ShoppingList by multiple Item Names

```
Request:
{
  "findType": "itemName",
  "title": "",
  "itemId": 0,
  "itemName": "banana, tuna"
}

Response:

{
    "status": 200,
    "data": {
        "items": [
            {
                "name": "banana",
                "id": 4,
                "quantity": "1"
            },
            {
                "name": "tuna",
                "id": 6,
                "quantity": "6"
            }
        ],
        "shopping_list": [
            {
                "date": 1537786362000,
                "title": "Shopping Title",
                "id": 6,
                "shop_name": "Shopping Name"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title",
                "id": 8,
                "shop_name": "Shopping Name"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title",
                "id": 9,
                "shop_name": "Shopping Name"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title4",
                "id": 10,
                "shop_name": "Shopping Name4"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title5",
                "id": 11,
                "shop_name": "Shopping Name5"
            },
            {
                "date": 1537786363000,
                "title": "Shopping Title",
                "id": 7,
                "shop_name": "Shopping Name"
            }
        ]
    }
}

```

If there is not data found, this api would return an empty list below.

```
{
    "status": 200,
    "data": []
}
```

### Error Response Parameters

Parameter | Type | Description
--------- | -----| -----------
status    |  integer | 4XX, 5XX.
reason    |  string / json  | a string of error reason / error's reasons in JSON while invalid request

### Example:

```
{
    "status": 400,
    "reason": "find_type is null"
}
```

Error Status | Error Reason | Description
--------- | -----| -----------
400    |  invalid_request | request parameters are null
500    |  Internal server error | Internal server error
