from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

cv = f"""
{Fore.GREEN}Hello world!{Style.RESET_ALL} 👋🏻️ 🌎

My name is Fede Calendino, I'm an Argentinian 🇦🇷  living in the UK 🇬🇧.

I'm a passionate software engineer with a focus on backend development. 
I enjoy scripting, code generation, automation, and web scraping. 
Always happy to help, eager to travel, and excited to learn new things.

Currently working as a Software Engineer at Microsoft.

✉️\tfede@calendino.com
💻\tgithub.com/fedecalendino
👤\tlinkedin.com/in/fedecalendino
"""


print(cv)
