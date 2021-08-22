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

    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    
    
    browser = webdriver.Chrome(options=options)

    browser.get("https://www.tradingview.com/chart/?symbol=BITSTAMP%3ABTCUSD")

    browser.maximize_window()

    sleep(5)
    period = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[2]')
    period.click()
    
    
    period = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[16]')
    period.click()
    ad = browser.find_element_by_xpath('/html/body/div[6]/div/span/div[1]/div/div/div[3]/div[2]/div/div/span[2]/span')
    ad.click()
    sleep(5)

    link = pyperclip.paste()

    print(link)
    browser.quit()

    embed_slp = discord.Embed(
        title= 'Preço SLP',
        description= f'Atualmente: R$ {result}',
        colour = discord.Colour.green()
    )
    
    

    embed_slp.set_author(name='SLP', icon_url='')

    embed_slp.set_image(
        url=f'{link}'
    )
    
    embed_slp.set_footer(text="feito por Csehz#0527")
    sleep(5)
    await preco_slp.send(embed=embed_slp)
    
    sleep(5)



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