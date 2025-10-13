import tinytuya

DEVICE_IP = '192.168.0.111'
LOCAL_KEY = 'B1iC3Q<mUgndi8k0'

def obter_status_tomada(device_id: str, device_ip: str, local_key: str):
    """
    Retorna o status atual de uma tomada Tuya (corrente, potência, tensão).

    Parâmetros:
        device_id (str): ID do dispositivo.
        device_ip (str): Endereço IP local do dispositivo.
        local_key (str): Chave local (LocalKey) do dispositivo.

    Retorna:
        dict: {'corrente_A': float, 'potencia_W': float, 'tensao_V': float}
              ou {'erro': str} se algo falhar.
    """
    try:
        plug = tinytuya.OutletDevice(device_id, device_ip, local_key)
        plug.set_version(3.4)
        
        status = plug.status()
        
        if 'dps' not in status:
            return {'erro': 'Não foi possível obter dados DPS do dispositivo.'}

        dps = status['dps']
        corrente_mA = dps.get('18', 0)
        potencia_dW = dps.get('19', 0)
        tensao_dV = dps.get('20', 0)

        dados = {
            'corrente_A': corrente_mA / 1000.0,
            'potencia_W': potencia_dW / 10.0,
            'tensao_V': tensao_dV / 10.0
        }
        return dados

    except Exception as e:
        return {'erro': f'Falha na conexão: {e}'}

if __name__ == '__main__':
    obter_status_tomada()