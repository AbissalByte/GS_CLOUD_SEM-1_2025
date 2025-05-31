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

if __name__ == "__main__":
    print("\n🔎 Verificação de senha:")
    senha = getpass.getpass("Digite a senha a verificar (não será exibida): ")
    resultado = check_password(senha)
    print(resultado)