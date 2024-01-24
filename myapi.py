#Here we are importing the FastAPI feature via which we are going to create a API of our own.
from fastapi import FastAPI

#Here we are creating an API instance
app=FastAPI()

#After we have created an instance of FastAPI object, the next thing to do is creating an endpoint Of the communication channel.
#To understand an endpoint, lets see an example URL. Say the URL is "amazon.in/create-user". The "create-user" part of that URL is endpoint of that URL. What is does is it defines the task of any given URL.
#The endpoint management is done via endpoint methods. There are many of them out there though the common ones are GET, POST, PUT and DELETE. Lets have a look at what each these methods actually does.
#GET- This is used to get an information
#POST- This is used to create something new.
#PUT- This is used for updation
#DELETE- This is used to delete thing.
#Now lets see an example of implementing this endpoint methods for endpoint creation.

@app.get("/")
def index():
    return{"name":"Ashutosh Kumar Singh"}
#Above we have just used GET to create an endpoint. In the get attribute we can enter any URL though the URL "/" defines that we are opening the Home page to retrive the information. After that we need to create a function, which we created by the name index which return the data.
#Note that the default return type for data on FastAPI is JSON. We  here are returning it in dictionary format. Later we will see how to convert this dictionary to JSON format.

#Now what happens next is creation of webserver to host this API. This is done via the Uvicorn library. We implement this library in the CMD. The code to implement "myapi" file's get api parsed over app object is,
#uvicorn myapi:app --reload

#Now I would Like to elaborate a bit about uvicorn. The uvicorn provides an documentation options automatically documenting how does our api works and also provides us an environment to test our api saving us from the hastle of using tools such as postman. To access documentation, the code is,
#<Unicorn Link>\docs

#Now we are going to discuss endpoint parameters. Endpoint parameters are used to return data in respect to the input in the endpoint. This can be performed in as a path or as a query. Hence we have two types of endpoint parameters. The Path Parameter and the Query Parameter.

#Lets first try path parameter. The code below helps us understand what Path Parameters actually work/mean.
student={
    1:{
        "Name":"Ashutosh",
        "Semester":4,
        "Roll": 22052974
    }
} 

'''@app.get("/get-user/{student_id}")
def get_student(student_id: int):
    return(student[student_id])'''

#What we see in the code above is using a path parameter to manipulate the functioning of our endpoint. "/get-user/{student_id}" is the path and here student_id is the path parameter. This parameter is then getting defined in the function and is then retrieving data from the examplar dictionary.
#Note one way to access this data is using the api call, but other way is using the URL itself. For instance to access ID "1" we can simply use the URL,
#" http://127.0.0.1:8000/get-user/1"

#Now lets see a bit more.
from fastapi import Path
#We can use the Path Library to access more path parameters and define how will our the endpoints work. Lets see an extension to the previosly created endpoint.
@app.get("/get-user8/{student_id}")
def get_student(student_id: int=Path(description="Enter Student Roll",gt=0,lt=100)):
    return(student[student_id])
#lt is less than, gt is greater than, ge is greater than equal to, le is less than equal to and etc. See the difference in docs file for further understanding of how does it actually affects api.

#Now lets just move ahead and see the query parameter. Now when you see the code, the structure of query seems very similar, yet it is different to Path. A very basic difference can be seen in URLs when we try to implement a path or a query.
#In case of Path, we see URL something like this, "google.com/get-data/1"
#In case of Query, we see the URL something like this, "google.com/get-data?1"
#Now lets see how the two differ in implementation.

@app.get("/get-user7")
def get_student(student_id:int):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")

#Now one thing to observe is that whenever these APIs are implemented, if there is a place of query it becomes compulsory for the user to fill the fields. We can make that optional via either setting default value to none or using the optional object. Both are implemented below.

@app.get("/get-user6")
def get_student(student_id:int=None):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")

from typing import Optional
@app.get("/get-user5")
def get_student(student_id:Optional[int]=None):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")

#While using non-compulsory APIs we encounter 1 issue. The issue is encountered in the case where we are using multiple parameters in our function. In that case we need to ensure that our compulsory parameters are mentioned before the not compulsory ones. For instance see the example below,
@app.get("/get-user4")
def get_student(roll:int,student_id:int=None):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")
#The above code is correct. Since non-default(compulsory) parameter comes before compulsory(default) parameter. Though it becomes a problem in the code below,
'''
@app.get("/get-user3")
def get_student(student_id:int=None,roll:int):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")
'''
#A very simple way to tackle this problem is, usage of *. See below.
@app.get("/get-user2")
def get_student(*,student_id:int=None,roll:int):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")
#Now you will get no errors.

#Now in the following code we will se an instance where we are combining the path and query parameters.
@app.get("/get-user1/{student_id}")
def get_student(student_id:int,roll:int,semester:int):
    for i in student:
        if(i==student_id):
            return(student[i])
    return("Data Not found")
#Here we combined the path parameter "student_id" with query parameters roll and sem. Do take a look a docs to understand how the two differ.

#Lets move ahead into a different endpoint method. Lets talk about POST method. POST as metioned already is used to create something new.
#All the operations that we have performed till now have been performed on the student dataset. One common error that the API throws regularly is the one where we try to access a object which is just not thier. One way to solve this is, if in case we do come across such situation, we get a option to create object in the run time. Lets do that below.

from pydantic import BaseModel

class Student(BaseModel):
    Name: str
    Semester: int
    Roll: int

#When we said we want to create an object against a key when its not there, we also need to define the structure under which the data will be created and stored. The class above is for that. The BaseModel library there links the API which the class to create the data point at time of execution.
@app.post("/get-student/{Student_id}")
def get_student(Student_id:int,students:Student):
    if(Student_id in student):
        return("Student already  exists")
    student[Student_id]=students
    return(student[Student_id]) 

#Now lets move onto the next endpoint method that is PUT. PUT as we have already metioned is used to edit the already available data in the dataset or the JSON file. Lets see how do we implement this.

#First we will create a very similar class object as we did in the case of POST. The reason we are not using the PUSH class object in this case is because all its variables are non-default, hence when executing it, its compulsory for us to enter all the 3 feilds which is not required in this case are we are just editing the already available data, so we can maybe just edit 1 or 2 fields. So to provide us this flexibility we edit the class as follows.

class stud(BaseModel):
    Name:Optional[str]=None
    Roll:Optional[int]=None
    Semester:Optional[int]=None

#Lets now try to implement the POST Object.

app.put("/get-student/{Student_id}")
def get_student(Student_id:int, students:stud):
    if(Student_id not in student):
        return("Instance not available.")
    if(students.name!=None):
        student[Student_id].name=students.Name
    if(students.Roll!=None):
        student[Student_id].Roll=students.Roll
    if(students.Semester!=None):
        student[Student_id].Semester=students.Semester
    return(student[Student_id])

#In the above code the updation task is performed only when field is entered. The if states used above are to ensure that. If a similar code was written for PUT as in case of PUSH, it would have generated an error.

#Last but not the last, lets do the DELETE endpoint method.
@app.delete("/get-student/{student_id}")
def delete_student(student_id:int):
    if(student_id not in student):
         return("Cannot delete. Object not found")
    del student[student_id]
    return("Object deleted")