import os
import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
from time import sleep
import pyperclip
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


load_dotenv(os.path.join(os.getcwd(), '.env'))
SECRET_KEY = os.getenv("TOKEN")

cg = CoinGeckoAPI()
cliente = commands.Bot(command_prefix="!", case_insensitive=True)


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


@cliente.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = f'**Comando em cooldown** por favor, espere {int(error.retry_after)} segundos antes de digitar novamente.'
        await ctx.send(msg)


@cliente.command()
async def ola(ola):
    await ola.send(f'Olá, {ola.author}!')


@cliente.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def preco_slp(preco_slp):
    result = float(slp_price['smooth-love-potion']['brl'])

    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("disable-infobars")

    browser = webdriver.Chrome(options=options)
    browser.get("https://www.tradingview.com/chart/?symbol=BITSTAMP%3ABTCUSD")
    sleep(1)
    window_before = browser.window_handles[0]

    webdriver.ActionChains(browser).key_down(Keys.ALT).send_keys("s").perform()

    sleep(2)

    link = pyperclip.paste()

    browser.execute_script("window.open('{link}')")  # Abre segunda guia

    # Chama a segunda guia de "windows_after"
    window_after = browser.window_handles[1]
    browser.switch_to.window(window_after)  # Troca para a segunda guia
    browser.get(link)  # Acessa o link na segunda guia

    html = browser.page_source

    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img')
    endereco_imagem = img.get('src')

    print(f"ESSE E O ENDERECO : {endereco_imagem}")

    embed_slp = discord.Embed(
        title='Preço SLP',
        description=f'Atualmente: R$ {result}',
        colour=discord.Colour.green()
    )

    embed_slp.set_author(name='SLP', icon_url='')

    embed_slp.set_image(
        url=endereco_imagem
    )

    embed_slp.set_footer(text="feito por Csehz#0527")
    await preco_slp.send(embed=embed_slp)

    browser.quit()


@cliente.command()
async def preco_pvu(preco_pvu):
    result = float(pvu_price['plant-vs-undead-token']['brl'])
    
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("disable-infobars")

    browser = webdriver.Chrome(options=options)
    browser.get("https://poocoin.app/tokens/0x31471e0791fcdbe82fbf4c44943255e923f1b794")
    sleep(1)
    window_before = browser.window_handles[0]

    webdriver.ActionChains(browser).key_down(Keys.ALT).send_keys("s").perform()
    sleep(2)
    webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys("c").perform()
    sleep(2)
    link = pyperclip.paste()

    browser.execute_script("window.open('{link}')")  # Abre segunda guia

    # Chama a segunda guia de "windows_after"
    window_after = browser.window_handles[1]
    browser.switch_to.window(window_after)  # Troca para a segunda guia
    browser.get(link)  # Acessa o link na segunda guia

    html = browser.page_source

    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img')
    endereco_imagem = img.get('src')

    print(f"ESSE E O ENDERECO : {endereco_imagem}")
    
    embed = discord.Embed(
        title='Preço PVU',
        description=f'Atualmente: R$ {result}',
        colour=discord.Colour.red()
    )

    embed.set_author(
        name='PVU', icon_url='https://pbs.twimg.com/profile_images/1409847793355657219/LQQ989bP.jpg')

    embed.set_image(
        url=endereco_imagem
    )

    embed.set_footer(text="feito por Csehz#0527")

    await preco_pvu.send(embed=embed)

print(f"OLHA O QUE IMPRIMIU: {SECRET_KEY}")
cliente.run(SECRET_KEY)
