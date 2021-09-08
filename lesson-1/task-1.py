'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев 
для конкретного пользователя, сохранить JSON-вывод в файле *.json.

'''

import requests
import json

url = 'https://api.github.com'
user = input('Введите имя пользователя Github: ').strip()
params = {'per_page': 200}

request = requests.get(f'{url}/users/{user}/repos', params=params)

json_data = request.json()
print(f'Список репозиториев пользователя {user}: ')
for i in json_data:
    print(i['name'])

with open('repos.json', 'w') as file:
    json.dump(json_data, file)


'''
Ввод и вывод программы (скопировано из терминала):

Введите имя пользователя Github: boygaggoo
Список репозиториев пользователя boygaggoo: 
101-GameDesign-2D-GameDesign-With-Unity
2dboilerplate
2d_platformer_unity
30-days-of-react-native
49erSense
Accelerometer
ACEMusicPlayer
aChat
aDateSwitcher
Adb-Remote-Screen
AdGallery
Advance-Android-Tutorials
AdvancedRecyclerView
advancedtextview
AFBlurSegue
AFViewShaker
AFWeather
AgendaCalendarView
ai2app
AI_Trader
AJCPlayer
Alerter
Algorithm-Implementations
Algorithms
AlmostMaterialDatepicker
AMPAvatarView
AMWaveTransition
andar
android
android-about-page
Android-AdvancedWebView
android-amazing-listview
android-antivirus
Android-App-Data-Usage-Monitor
Android-Application-Template
android-auto-scroll-view-pager
android-BatteryLoadingView
Android-BluetoothSPPLibrary
android-bootstrap
Android-Bootstrap-1
android-Camera2Video
Android-ChatHead
android-child-lock
android-chips
android-classyshark
android-Crop-Image
Android-Crop-Tool
android-downloadable-fonts-example
android-file-explorer
android-google-drive-browser
Android-GoogleDirectionLibrary
android-graphiql
android-guidelines
android-image-magnifier
Android-Interview-Questions
android-keyboard
Android-Kotlin-Commons
android-lecture
Android-MobileLocator
android-money-manager-ex
android-morphing-button
android-mvvm
Android-Network-Info-Boss-Master
Android-NiceTab
Android-Onboarder
android-patternview
android-pdfview
Android-Permission-Check-Library
Android-Phone-Protector
Android-PhotoTaker
android-popup-info
android-private-sms
android-process-button
Android-Projects
android-Required-Interview-Outline
Android-RoundCornerProgressBar
android-sample-clock
android-screenshot-gallery
android-security-awesome
android-shapeLoadingView
android-simple-animation
Android-Simple-Social-Sharing
Android-SimpleLocation
Android-SlidingEmojiKeyboard
Android-Smart-Login
Android-Sms-BackUp-XML
Android-SMSBackup
android-social-signin-helper
android-socialbuttons
Android-Speech-Bubble-LIstView
android-sqlite-asset-helper
android-sumbit-credit-card-flow
android-swipelistview-sample
android-training-course-in-chinese
Android-UltimateGPUImage
android-Ultra-Pull-To-Refresh
Android-UndoBar
Android-VideoThumbnail-Resource
android-volley-file-upload
Android-Vulnerabilities-Overview

'''
