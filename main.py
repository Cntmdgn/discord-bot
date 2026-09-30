import os
import random
import discord
from discord.ext import commands
from discord import app_commands

# 봇 기본 설정
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 봇이 준비되었을 때 슬래시 명령어 동기화
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f'성공적으로 로그인했습니다: {bot.user.name}')
        print(f'슬래시 명령어 {len(synced)}개가 동기화되었습니다!')
    except Exception as e:
        print(f'동기화 중 오류 발생: {e}')


# ==================== 1. 기본 & 대화 슬래시 명령어 ====================

@bot.tree.command(name="안녕", description="봇이 인사합니다.")
async def 안녕(interaction: discord.Interaction):
    await interaction.response.send_message(f'안녕하세요, {interaction.user.mention}님!')

@bot.tree.command(name="이공", description="이공이라고 말해줍니다.")
async def 이공(interaction: discord.Interaction):
    await interaction.response.send_message('졸귀')

@bot.tree.command(name="멍멍", description="멍멍! 하고 짖습니다.")
async def 멍멍(interaction: discord.Interaction):
    await interaction.response.send_message('멍멍!')

@bot.tree.command(name="야옹", description="야옹~ 하고 울어줍니다.")
async def 야옹(interaction: discord.Interaction):
    await interaction.response.send_message('야옹~ 🐾')

@bot.tree.command(name="바보", description="장난을 칩니다.")
async def 바보(interaction: discord.Interaction):
    await interaction.response.send_message('반사~! 😜')


# ==================== 2. 미니게임 & 운세 ====================

@bot.tree.command(name="주사위", description="1부터 6까지 주사위를 던집니다.")
async def 주사위(interaction: discord.Interaction):
    number = random.randint(1, 6)
    await interaction.response.send_message(f'🎲 주사위를 던져서 **[{number}]**가 나왔습니다!')

@bot.tree.command(name="동전", description="동전을 던져 앞면/뒷면을 맞춥니다.")
async def 동전(interaction: discord.Interaction):
    result = random.choice(['앞면 🪙', '뒷면 🪙'])
    await interaction.response.send_message(f'동전을 던진 결과: **{result}**!')

@bot.tree.command(name="가위바위보", description="봇과 가위바위보 게임을 합니다.")
@app_commands.choices(선택=[
    app_commands.Choice(name="가위 ✌️", value="가위"),
    app_commands.Choice(name="바위 ✊", value="바위"),
    app_commands.Choice(name="보 🖐️", value="보")
])
async def 가위바위보(interaction: discord.Interaction, 선택: app_commands.Choice[str]):
    user_choice = 선택.value
    bot_choice = random.choice(['가위', '바위', '보'])
    
    if user_choice == bot_choice:
        outcome = "비겼습니다! 🤝"
    elif (user_choice == '가위' and bot_choice == '보') or \
         (user_choice == '바위' and bot_choice == '가위') or \
         (user_choice == '보' and bot_choice == '바위'):
        outcome = "당신이 이겼습니다! 🎉"
    else:
        outcome = "제가 이겼습니다! 🤖"
        
    await interaction.response.send_message(f'당신: **{user_choice}** vs 봇: **{bot_choice}**\n👉 **{outcome}**')

@bot.tree.command(name="운세", description="오늘의 운세를 확인합니다.")
async def 운세(interaction: discord.Interaction):
    fortunes = [
        '✨ 오늘은 뭘 해도 되는 최고 대박의 날입니다!',
        '🍀 뜻밖의 소소한 행운이 찾아올 거예요.',
        '☕ 평범하지만 무난하고 평화로운 하루입니다.',
        '⚠️ 뜻밖의 지출이 발생할 수 있으니 조심하세요!',
        '🔥 당신의 능력을 마음껏 발휘할 기회가 올 것입니다.'
    ]
    await interaction.response.send_message(f'🔮 {interaction.user.mention}님의 오늘 운세: **{random.choice(fortunes)}**')


# ==================== 3. 결정장애 해결 & 추천 ====================

@bot.tree.command(name="점심추천", description="오늘 점심 메뉴를 추천해 드립니다.")
async def 점심추천(interaction: discord.Interaction):
    menus = ['제육볶음', '돈까스', '김치찌개', '짜장면', '햄버거', '초밥', '마라탕', '국밥', '치킨', '떡볶이']
    await interaction.response.send_message(f'🍱 오늘 점심은 **[{random.choice(menus)}]** 어떠세요?')

@bot.tree.command(name="야식추천", description="오늘 야식 메뉴를 추천해 드립니다.")
async def 야식추천(interaction: discord.Interaction):
    snack = ['뿌링클 치킨', '족발/보쌈', '불닭볶음면', '야채곱창', '피자', '타코야끼', '빙수']
    await interaction.response.send_message(f'🌙 오늘 야식은 **[{random.choice(snack)}]** 결정!')

@bot.tree.command(name="제비뽑기", description="띄어쓰기로 여러 항목을 입력하면 무작위로 하나를 뽑습니다.")
async def 제비뽑기(interaction: discord.Interaction, 항목들: str):
    items = 항목들.split()
    if not items:
        await interaction.response.send_message('항목을 하나 이상 입력해 주세요!')
        return
    await interaction.response.send_message(f'🎉 뽑힌 항목은 바로 **[{random.choice(items)}]** 입니다!')


# ==================== 4. 유틸리티 & 편의 기능 ====================

@bot.tree.command(name="아바타", description="유저의 아바타 프로필 사진을 가져옵니다.")
async def 아바타(interaction: discord.Interaction, 대상: discord.Member = None):
    member = 대상 or interaction.user
    await interaction.response.send_message(f'📸 {member.mention}님의 프로필 사진입니다:\n{member.display_avatar.url}')

@bot.tree.command(name="핑", description="봇의 응답 속도를 측정합니다.")
async def 핑(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'🏓 퐁! 현재 봇의 응답 속도는 **{latency}ms** 입니다.')


# ==================== 5. 메뉴 및 도움말 ====================

@bot.tree.command(name="메뉴", description="전체 슬래시 명령어 목록을 확인합니다.")
async def 메뉴(interaction: discord.Interaction):
    embed = discord.Embed(title="📜 봇 전체 메뉴 및 명령어", description="사용할 수 있는 슬래시(/) 명령어 목록입니다.", color=0x3498db)
    embed.add_field(name="💬 기본 대화", value="`/안녕`, `/이공`, `/멍멍`, `/야옹`, `/바보`", inline=False)
    embed.add_field(name="🎮 게임 & 운세", value="`/주사위`, `/동전`, `/가위바위보`, `/운세`", inline=False)
    embed.add_field(name="🍕 결정 장애 해결", value="`/점심추천`, `/야식추천`, `/제비뽑기 [항목들]`", inline=False)
    embed.add_field(name="⚙️ 유틸리티", value="`/아바타`, `/핑`", inline=False)
    embed.set_footer(text="채팅창에 / 를 입력하면 목록에서 쉽게 찾아 선택할 수 있습니다!")
    await interaction.response.send_message(embed=embed)

token = os.environ.get("DISCORD_TOKEN")
bot.run(token)