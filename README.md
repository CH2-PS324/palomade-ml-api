# PALOMADE ML API
Team CH2-PS324 | Bangkit Capstone Project 2023

```markdown
# Prerequisites
Before running the application, make sure you have the following installed on your machine:
- [Python 3](https://www.python.org/)

# Tech We Use
- Flask
- Tensorflow
```

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/CH2-PS324/palomade-ml-api.git
   ```

2. Navigate to the project directory:

   ```bash
   cd palomade-ml-api
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the Express.js server and run the database setup:

```bash 
python main.js
```

## API Endpoints

### 1.  Predict Sawit

- **Method:** `POST`
- **Path:** `/predict`
- **Description:** endpoint for predict sawit
- **Request Body (form-data):**
  ```form-data
    image = Image (*jpg/png/jpeg)
    type = "brondolan" or "bongkahan"
  ```
- **Response Body:**
  ```json
  {  
      "status": {
          "code": 200,
          "data": {
              "classType": "Bongkahan Sawit Matang",
              "precentase": 100
          },
          "message": "Success predicting"
      }
  }
  ``` 
- **Error Respone:**
  
  Error Type is Empty
  ```json
  {
       "status": {
           "code": 400,
           "message": "Invalid type of scan. Please choose bongkahan or brondolan."
       }
   }
  ```
  Error Invalid Format File
  ```json
   {
       "status": {
           "code": 400,
           "message": "Invalid file format. Please upload a JPG, JPEG, or PNG image."
       }
   }
  ```
