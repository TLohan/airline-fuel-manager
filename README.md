# airline-fuel-manager

This is a tool for use by an airline to plan where a plane should refuel along its route. A user selects the plane, base airport and several destination airports. The program will then calculate the amount of fuel required to fly each leg of the route and how much fuel should be bought at each airport. The plane’s performance attributes can be altered to reflect different conditions. 

## Design
The application was designed to adhere to the SOLID design principles as much as possible. Care was taken to make sure all classes' were loosely coupled with all major dependencies being injected rather than declared in the initialiser. For example the app gets its currency data from a local CSV file, were this to be upgraded to a system that took live currency data from some currency API, the parts of the app that need access to this live currency data would not have to be altered. 

I used python's built-in unittest library throughout the development of the project to test each class as I developed it. 

## Running the application
To run the application extract the files and activate the virtualenv.

``` shell session
$ ~/venv/Scripts > activate
```

Next, execute the \_\_main_\_.py file:

``` shell script
$  > python __main.__.py
```

