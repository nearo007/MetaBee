import tinytuya
from .models import Printer

DEVICE_IP = '192.168.226.79'
LOCAL_KEY = '96tO3A>2urrqK$#$'

def get_outlet_status(device_id: str, device_ip: str, local_key: str):
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

# def api_get_outlet_status(device_id):
#     try:
#         plug = tinytuya.OutletDevice(device_id, DEVICE_IP, LOCAL_KEY)
#         plug.set_version(3.4)
        
#         status = plug.status()
        
#         if 'dps' not in status:
#             return {'erro': 'Não foi possível obter dados DPS do dispositivo.'}

#         dps = status['dps']
#         corrente_mA = dps.get('18', 0)
#         potencia_dW = dps.get('19', 0)
#         tensao_dV = dps.get('20', 0)

#         dados = {
#             'corrente_A': corrente_mA / 1000.0,
#             'potencia_W': potencia_dW / 10.0,
#             'tensao_V': tensao_dV / 10.0
#         }
#         return dados

#     except Exception as e:
#         return {'erro': f'Falha na conexão: {e}'}

# for testing API
def api_get_outlet_status(device_id):
    return {'corrente_A': 0.2, 'potencia_W': 0.3, 'tensao_V': 0.4}

def get_printers_state_func():
    printers = Printer.objects.all()
    printers_state = {}

    for printer in printers:
        device_id = printer.device_id
        printer_state = get_outlet_status(device_id, DEVICE_IP, LOCAL_KEY)
        printers_state[device_id] = printer_state

    return printers_state

def update_printers_state_in_db(printers_state: dict):
    for device_id, state in printers_state.items():
        if state['corrente_A'] > 0.100:
            Printer.objects.filter(device_id=device_id).update(status=2)
        else:
            Printer.objects.filter(device_id=device_id).update(status=0)


# for device_id, state in printers_state.items():
#     Printer.objects.filter(device_id=device_id).update(
#         corrente_A=state['corrente_A'],
#         potencia_W=state['potencia_W'],
#         tensao_V=state['tensao_V']
#     )

if __name__ == '__main__':
    print(get_outlet_status())