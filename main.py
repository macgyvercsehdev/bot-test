import os
import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
from time import sleep
import pyperclip
from selenium import webdriver




load_dotenv(os.path.join(os.getcwd(), '.env'))
SECRET_KEY = os.getenv("TOKEN")

cg = CoinGeckoAPI()
cliente = commands.Bot(command_prefix = "!", case_insensitive = True)


pvu_price = cg.get_price(ids='plant-vs-undead-token', vs_currencies='brl')
slp_price = cg.get_price(ids='smooth-love-potion', vs_currencies='brl')

@cliente.event
async def on_ready():
    await cliente.change_presence(
        activity=discord.Game(
        name=f"PVU: R$ {float(pvu_price['plant-vs-undead-token']['brl'])}", 
        url="https://www.coingecko.com/pt/moedas/plant-vs-undead-token"
      )
    )
    print(f'Estou pronto! {cliente.user}')

@cliente.event
async def on_connect():
    print(f'Olá, estou conectado!')

@cliente.event
async def on_disconnect(sair):
    await sair.send(f'Saindo, já volto!')


@cliente.command()
async def ola(ola):
    await ola.send(f'Olá, {ola.author}!')

@cliente.command()
async def preco_slp(preco_slp):
    result = float(slp_price['smooth-love-potion']['brl'])

    embed_slp = discord.Embed(
        title= 'Preço SLP',
        description= f'Atualmente: R$ {result}',
        colour = discord.Colour.green()
    )
    
    

    embed_slp.set_author(name='SLP', icon_url='')

    embed_slp.set_image(
        url='https://s3.tradingview.com/snapshots/g/GTO7nBy7.png'
    )
    
    embed_slp.set_footer(text="feito por Csehz#0527")

    await preco_slp.send(embed=embed_slp)


@cliente.command()
async def graf_pvu_5(graf_pvu_5):
    
    
    useragent = "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"

    #Firefox
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent)
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument('--headless')
    
    
    browser = webdriver.Firefox(firefox_profile=profile, options=options, executable_path='/usr/local/bin/geckodriver', firefox_binary='/usr/bin/firefox')

    browser.get("https://www.tradingview.com/chart/?symbol=BITSTAMP%3ABTCUSD")

    browser.maximize_window()

    sleep(5)

    period = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[2]')
    period.click()
    
    
    period = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[16]')
    period.click()
    sleep(2)
    ad = browser.find_element_by_xpath('/html/body/div[6]/div/span/div[1]/div/div/div[3]/div[2]/div/div/span[2]/span')
    ad.click()

    sleep(2)
    
    link = pyperclip.paste()

    embed_char_slp = discord.Embed(
        title= 'Gráfico SLP: 5 dias',
        description= link,
        colour = discord.Colour.green()
    )
    embed_char_slp.set_footer(text="feito por Csehz#0527")

    sleep(2)
    await graf_pvu_5.send(embed=embed_char_slp)

    print(link)
    print('Screenshots taken')




@cliente.command()
async def preco_pvu(preco_pvu):
    result = float(pvu_price['plant-vs-undead-token']['brl'])

    embed = discord.Embed(
        title= 'Preço PVU',
        description= f'Atualmente: R$ {result}',
        colour = discord.Colour.red()
    )
 
    embed.set_author(name='PVU', icon_url='https://pbs.twimg.com/profile_images/1409847793355657219/LQQ989bP.jpg')

    embed.set_image(
        url='https://s3.tradingview.com/snapshots/g/GTO7nBy7.png'
    )
    
    embed.set_footer(text="feito por Csehz#0527")

    await preco_pvu.send(embed=embed)

print(f"OLHA O QUE IMPRIMIU: {SECRET_KEY}")
cliente.run(SECRET_KEY)