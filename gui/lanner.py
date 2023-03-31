from msgbx import showMessageBox,message_box


mess='''In this example, we pass the title string as an argument to the MyWindow constructor. Inside the constructor, we use the len() function to get the length of the title string and multiply it by 10 to get an approximate width in pixels. We add 50 pixels to this value to make sure that the width is always 50 pixels wider than the title string.

We then set both the minimum and maximum width of the window to this calculated value using the setMinimumWidth() and setMaximumWidth() methods.'''
# msgboxw=showMessageBox("hey howa \nre yoou    \n        ","from ")
# msgboxw=showMessageBox(mess,"from 10.10.1.010.10 djcndkc ks")
# msgboxw=msgbox("from 10.10.1.010.10 djcndkc ks","hey howa re yoou ")
# print(msgboxw)

country_names = ["Argentina", "Brazil", "Canada", "Denmark", "Egypt", "France", "Germany", "Honduras", "India", "Japan", "Kenya", "Liberia", "Mexico", "Nigeria", "Oman", "Peru", "Qatar", "Russia", "Spain", "Thailand", "United States", "Vietnam", "Yemen", "Zimbabwe"]

# b,a=message_box(country_names,"Send Message" )
b,a,d,c=message_box(country_names,"Send Message" )
print(a,b,c,d)
msg,filu,folu=showMessageBox(b,f'message From xxxxxxxxxxx to {a}')
# msg=showMessageBox(msg,"from self")
print(msg,filu,folu)