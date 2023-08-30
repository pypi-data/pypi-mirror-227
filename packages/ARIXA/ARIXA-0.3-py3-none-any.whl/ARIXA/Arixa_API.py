import requests
import json

# Define the base URL and headers
base_url = 'http://localhost:3000/api/v1'
#HEADERS = {'Content-Type': 'application/json', 'api-key': 'm1475963m0'}

def set_api_key(api_key):
    global HEADERS
    HEADERS = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }

def init():
    """Initialize the robotic arm."""
    response = requests.post(f'{base_url}/initialize', headers=HEADERS)
    return response.json()

def move_joint_space(j1, j2, j3, j4, j5, j6, speed, acc):
    """Move the robotic arm using joint space coordinates."""
    payload = {
        'j1': j1,
        'j2': j2,
        'j3': j3,
        'j4': j4,
        'j5': j5,
        'j6': j6,
        'speed': speed,
        'acc': acc
    }
    response = requests.post(f'{base_url}/move/joint_space', headers=HEADERS, json=payload)
    return response.json()

def move_cartesian(x, y, z, rx, ry, rz, speed, acc):
    """Move the robotic arm using Cartesian coordinates."""
    payload = {
        'x': x,
        'y': y,
        'z': z,
        'rx': rx,
        'ry': ry,
        'rz': rz,
        'speed': speed,
        'acc': acc
    }
    response = requests.post(f'{base_url}/move/cartesian', headers=HEADERS, json=payload)
    return response.json()

def get_status():
    """Get the status of the robotic arm."""
    response = requests.get(f'{base_url}/status', headers=HEADERS)
    return response.json()

def get_status_joint_space():
    """Get the status of the robotic arm in joint space."""
    response = requests.get(f'{base_url}/status/joint_space', headers=HEADERS)
    data = response.json()
    
    j1 = data.get('j1')
    j2 = data.get('j2')
    j3 = data.get('j3')
    j4 = data.get('j4')
    j5 = data.get('j5')
    j6 = data.get('j6')
    speed = data.get('speed')
    acc = data.get('acc')
    
    return j1, j2, j3, j4, j5, j6, speed, acc

def get_status_cartesian():
    """Get the status of the robotic arm in Cartesian space."""
    response = requests.get(f'{base_url}/status/cartesian', headers=HEADERS)
    data = response.json()
    
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    rx = data.get('rx')
    ry = data.get('ry')
    rz = data.get('rz')
    speed_cart = data.get('speed_cart')
    acc_cart = data.get('acc_cart')
    
    return x, y, z, rx, ry, rz, speed_cart, acc_cart


def emergency_stop():
    """Activate the emergency stop for the robotic arm."""
    response = requests.post(f'{base_url}/emergency_stop', headers=HEADERS)
    return response.json()

def shutdown():
    """Shutdown the robotic arm."""
    response = requests.post(f'{base_url}/shutdown', headers=HEADERS)
    return response.json()

def save_action_joint_space(name):
    """Save the latest action in joint space to a file."""
    #payload = json.dumps(action)
    response = requests.put(f'{base_url}/action/joint_space/{name}', headers=HEADERS)
    return response.text

def save_action_cartesian(name):
    """Save the latest action in Cartesian space to a file."""
   # payload = json.dumps(action)
    response = requests.put(f'{base_url}/action/cartesian/{name}', headers=HEADERS)
    return response.text

#def get_saved_action_joint_space(name):
#    """Retrieve the saved action in joint space from a file."""
#    response = requests.get(f'{base_url}/action/joint_space/{name}', headers=HEADERS)
#    return response.json()
#
#def get_saved_action_cartesian(name):
#    """Retrieve the saved action in Cartesian space from a file."""
#    response = requests.get(f'{base_url}/action/cartesian/{name}', headers=HEADERS)
#    return response.json()

def get_saved_action_joint_space(name):
    """Retrieve the saved action in joint space from a file."""
    response = requests.get(f'{base_url}/action/joint_space/{name}', headers=HEADERS)
    data = response.json()
    
    if 'data' in data:
        actions = data['data']
        
        j1_array = []
        j2_array = []
        j3_array = []
        j4_array = []
        j5_array = []
        j6_array = []
        speed_array = []
        acc_array = []
        
        for entry in actions:
            action = entry['action']
            
            j1_array.append(action['j1'])
            j2_array.append(action['j2'])
            j3_array.append(action['j3'])
            j4_array.append(action['j4'])
            j5_array.append(action['j5'])
            j6_array.append(action['j6'])
            speed_array.append(action['speed'])
            acc_array.append(action['acc'])
            
        return j1_array, j2_array, j3_array, j4_array, j5_array, j6_array, speed_array, acc_array
    else:
        return None


def get_saved_action_cartesian(name):
    """Retrieve the saved action in Cartesian space from a file."""
    response = requests.get(f'{base_url}/action/cartesian/{name}', headers=HEADERS)
    data = response.json()
    
    if 'data' in data:
        actions = data['data']
        
        x_array = []
        y_array = []
        z_array = []
        rx_array = []
        ry_array = []
        rz_array = []
        speed_cart_array = []
        acc_cart_array = []
        
        for entry in actions:
            action = entry['action']
            
            x_array.append(action['x'])
            y_array.append(action['y'])
            z_array.append(action['z'])
            rx_array.append(action['rx'])
            ry_array.append(action['ry'])
            rz_array.append(action['rz'])
            speed_cart_array.append(action['speed'])
            acc_cart_array.append(action['acc'])
            
        return x_array, y_array, z_array, rx_array, ry_array, rz_array, speed_cart_array, acc_cart_array
    else:
        return None

def start_recording_joint_space():
    """Start recording actions in joint space."""
    response = requests.post(f'{base_url}/start_save/joint_space', headers=HEADERS)
    return response.text

def stop_recording_joint_space(name):
    """Stop recording actions in joint space and save to a file."""
    response = requests.post(f'{base_url}/stop_save/joint_space/{name}', headers=HEADERS)
    return response.text

def start_recording_cartesian():
    """Start recording actions in Cartesian space."""
    response = requests.post(f'{base_url}/start_save/cartesian', headers=HEADERS)
    return response.text

def stop_recording_cartesian(name):
    """Stop recording actions in Cartesian space and save to a file."""
    response = requests.post(f'{base_url}/stop_save/cartesian/{name}', headers=HEADERS)
    return response.text

def get_saved_data_joint_space(name):
    """Retrieve all saved data in joint space from a file."""
    response = requests.get(f'{base_url}/saved/joint_space/{name}', headers=HEADERS)
    return response.json()

def get_saved_data_cartesian(name):
    """Retrieve all saved data in Cartesian space from a file."""
    response = requests.get(f'{base_url}/saved/cartesian/{name}', headers=HEADERS)
    return response.json()

def extract_and_assign_joint_space(name):
    """Extract data from a file and assign it for joint space."""
    response = requests.post(f'{base_url}/saved/joint_space/{name}', headers=HEADERS)
    return response.json()

def extract_and_assign_cartesian(name):
    """Extract data from a file and assign it for Cartesian space."""
    response = requests.post(f'{base_url}/saved/cartesian/{name}', headers=HEADERS)
    return response.json()
