import requests

token = "" # token da sua conta aqui
checkados = 0
validos = 0
invalidos = 0

with open('trimensais.txt', 'r') as file:
    links = file.read().splitlines()

def checker():
    global checkados, validos, invalidos
    for link in links:
        if link.startswith('https://discord.com/billing/promotions/'):
            codigo = link.replace('https://discord.com/billing/promotions/', '')
        elif link.startswith('https://promos.discord.gg/'):
            codigo = link.replace('https://promos.discord.gg/', '')
        else:
            codigo = None
        if codigo == None:
            print("[ERRO] Esse link não é suportado pelo checker!")
        else:
            url = f"https://discord.com/api/v9/entitlements/gift-codes/{codigo}"
            querystring = {"country_code":"BR","with_application":"false","with_subscription_plan":"true"}
            headers = {
                "authorization": token,
            }
            response = requests.get(url=url, params=querystring, headers=headers)
            if response.status_code == 200:
                if response.json().get('redeemed') == False and response.json().get('uses') < 1:
                    with open('input/validos.txt', 'a') as file:
                        file.write(link+'\n')
                    validos += 1
                    print(f'[VALIDO] O link ({link}) é válido')
                else:
                    with open('input/invalidos.txt', 'a') as file:
                        file.write(link+'\n')
                    invalidos += 1
                    print(f'[INVALIDO] O link ({link}) é inválido')
            else:
                with open('input/invalidos.txt', 'a') as file:
                    file.write(link+'\n')
                invalidos += 1
                print(f'[INVALIDO] O link ({link}) é inválido')
            checkados += 1

checker()
print(f'[FINALIZADO] | Validos: {validos} | Invalidos: {invalidos} | Total: {checkados}')