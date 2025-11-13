import tinytuya
import time

# --- CONFIGURAÇÃO --
# Cole as informações que você obteve
DEVICE_ID    = "eb6ef7c3036ef24c8aw7ul"  # Cole o ID do arquivo json
DEVICE_IP    = "192.168.0.111"            # Cole o IP que você encontrou
LOCAL_KEY    = "B1iC3Q<mUgndi8k0"         # Cole a KEY do arquivo json
INTERVALO_SEGUNDOS = 5

print(">>> Iniciando o script de monitoramento...")
print(f">>> Tentando conectar na tomada com IP: {DEVICE_IP}...")

try:
    # Conexão com o dispositivo
    plug = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
    plug.set_version(3.4)
    
    # Linha de teste para ver o status inicial
    print(">>> Conexão inicial estabelecida. Tentando obter status...")
    status_inicial = plug.status()
    print(f">>> Status inicial recebido: {status_inicial}")
    
    print("-" * 50)
    print(">>> Monitoramento iniciado com sucesso! Pressione CTRL+C para parar.")
    print("-" * 50)

    while True:
        # Pede o status completo do dispositivo
        status = plug.status()

        if 'dps' in status:
            dps = status['dps']
            
            corrente_mA = dps.get('18', 0)
            potencia_dW = dps.get('19', 0)
            tensao_dV = dps.get('20', 0)
            
            corrente_A = corrente_mA / 1000.0
            potencia_W = potencia_dW / 10.0
            tensao_V = tensao_dV / 10.0

            print(f"Corrente: {corrente_A:.3f} A | Potência: {potencia_W:.2f} W | Tensão: {tensao_V:.1f} V")
        else:
            print(">>> Não foi possível ler os dados de energia (DPS). Resposta recebida:")
            print(status)

        time.sleep(INTERVALO_SEGUNDOS)

except KeyboardInterrupt:
    print("\n>>> Monitoramento encerrado pelo usuário.")
except Exception as e:
    # Esta parte é a mais importante para o diagnóstico
    print("\n" + "="*20 + " OCORREU UM ERRO " + "="*20)
    print(f"NÃO FOI POSSÍVEL CONECTAR OU MANTER A CONEXÃO.")
    print(f"MOTIVO: {e}")
    print("="*58)
    print("\nVerifique se o IP está correto e se o Firewall do Windows está desativado.")
