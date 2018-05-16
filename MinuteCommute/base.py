from nav import nav
import dominate
from dominate.tags import img

branding = img(src='static/img/logo.png')

nav.register_element('frontend_top', Navbar(
    branding,
    View('Home', '.index'),
    View('Github', 'https://github.com/pzeng123/MinuteCommute'),
    View('Google Slides', 'https://www.google.com'),
    View('About', '.about'),
    Text("Don't waste time commuting")
))