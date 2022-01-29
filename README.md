# PyIFTTT
If This Than That - The python version to drive your own IOT and Automation Projects. 

If you are familiar with the website IFTTT (https://ifttt.com/),  this is the python version. IFTTT is awesome, but it a drag and drop tool of pre-approved app's that they have verified. This means it doesn't do complex logic and you can't add your own apps or functionality to exist apps - just use what's there and working. Again it's awesome but as a developer it's frustrating not to be able to close the gaps.

It you are not familiar with it its a automation and workflow engine that people use with IOT and other automation projects. The basic principle is you add some conditions and an action to do if those conditions are meet. It's a simple but powerfull tool have a play.


## What extra does PyIFTTT do?
* Multiple conditions
* Multiple actions
* Add an Else for actions where the condition is not met
* Unsupported apps - where there are backdoors, screen scraping etc you can add the app
* Add your own conditions and actions


## Sugggested Usage
If you are not adding new functionality the you can set these up without changing any python code, just setting up the Yaml config files to do what you want.

Github has actions we are really useful to run things periodically. So I'd suggest
1. Clone this repo to your own private repo in GitHub (so any app credentials are private
2. Configure as many workflows yml files you need.
3. Configure your auth.yml file with any creditials for each app
4. Run each config localy to make sure it works ok. "pyifttt.py -c configfile"
5. Push all your changes.
6. Set a GitHub Action for each config file to run on a cadence that works for your flow. (If they are un-offical perhaps not too often so you don't get blocked by them)) 


## Current Apps
### Growatt (Solar and Batteries)
Uses https://github.com/indykoning/ 's library - thank you!
Auth required [Username, Password]
* is_battery_full - if the state charge of the battery is 97-100% full
* is_input_above(kilowatt) - if the current power from the solar pannels is above a number of kilowatts
* is_input_below(kilowatt) - if the current power from the solar pannels is below a number of kilowatts


### Meross (Home IOT devices)
Uses https://github.com/albertogeniola/ 's library - thank you!
Auth required [Username, Password]
* is_on - is a switch on at the moment
* is_off - is a switch off at the moment
* action_on - turn a switch on
* action_off - turn a switch off


### Open Weather
Auth required [app_id, location]
* is_nighttime
* is_before_nighttime(minutes)
* is_after_nighttime(minutes)
* is_daytime
* is_before_daytime(minutes)
* is_after_daytime(minutes)
* is_clear(percentage)
* is_overcast(percentage)



## Example Use Case
It started for me with wanting to be able turn on a heater in winter, if my household battery is full and the pannels are still drawing power. Yes it sell the power but it's cheaper to use it to warm the house ratehr than turn the heater on at night and buy power.

### auth.yml
```
Growatt:
  username: <username>
  password: <password>
OpenWeather:
  app_id: <app_id for api access>
  location: Sydney, AU-NSW, AU
Meross:
  username: <username>
  password: <password>
```
  
### use_it_or_lose_it.yml
```
name: If battery full and spare power turn on switch
if:
  - app: Growatt
    condition: is_battery_full
  - app: Growatt
    condition: is_input_above
    args:
      kw: 3000
  - app: OpenWeather
    condition: is_before_nighttime
    args:
      minutes: 120
  - app: OpenWeather
    condition: is_average_temperature_below_c
    args:
      celsius: 15
  - app: Meross
    condition: is_on
    args:
      device_uuid: '<hidden>'
then:
  - app: Meross
    action: action_on
    args:
      device_uuid: '<hidden>'
else:
  - app: Meross
    action: action_off
    args:
      device_uuid: '<hidden>'
```

## Want some help?
If you are having trouble setting this up or need some help with a some extra functions, reach out and I may be able to help.

## Contribute
If you are adding devices/apps or functions we'd ove you to add it to this repo too so other can benefit. Suggestions to core code or anything else is welcome! Create a branch off master and create a PR to master for me to review.

## Support me/this project
If you're using this project I'd love atributution of whatever your favorite coin is - https://commerce.coinbase.com/checkout/3c82da1c-5945-490f-8c57-a8fe8cf9abb6
