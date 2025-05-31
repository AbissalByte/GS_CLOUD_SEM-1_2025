import hashlib
import requests
import getpass

# ============================
# 🔐 VERIFICAÇÃO DE SENHA - HIBP
# ============================

def check_password(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"❌ Erro ao conectar com o serviço de senhas vazadas: {e}"

    hashes = (line.split(":") for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return f"⚠️ Senha encontrada {count} vezes em vazamentos!"
    return "✅ Senha não encontrada em vazamentos."

# ============================
# 📧 VERIFICAÇÃO DE E-MAIL - MOZILLA MONITOR
# ============================

def try_mozilla_monitor(email):
    """
    Simula o acesso à página do Mozilla Monitor com o e-mail fornecido.
    Interpreta a resposta HTML para identificar vazamentos.
    """
    url = f"https://monitor.mozilla.org/?email={email}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code == 200:
            content = res.text.lower()

            if "we found your email" in content or "data breaches" in content:
                print(f"\n⚠️ Vazamentos encontrados para {email} no Mozilla Monitor.")
            elif "has not been found" in content or "no known data breaches" in content:
                print(f"\n✅ Nenhum vazamento encontrado para {email} no Mozilla Monitor.")
            else:
                print(f"\nℹ️ Resposta ambígua para {email}. Verifique manualmente.")
        else:
            print(f"⚠️ HTTP {res.status_code} recebido ao consultar o Mozilla Monitor.")
    except Exception as e:
        print(f"❌ Erro ao consultar Mozilla Monitor: {e}")


# ============================
# 🚀 EXECUÇÃO PRINCIPAL
# ============================

if __name__ == "__main__":
    print("\n🔎 Verificação de senha:")
    senha = getpass.getpass("Digite a senha a verificar (não será exibida): ")
    resultado = check_password(senha)
    print(resultado)

    print("\n🔎 Verificação de e-mail no Mozilla Monitor:")
    email = input("Digite o e-mail a verificar: ").strip()
    try_mozilla_monitor(email)
