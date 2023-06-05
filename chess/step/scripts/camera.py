from hikvisionapi import Client

def get_img(ip, user, password, debug=False):
    cam = Client(f'http://{ip}', user, password)
    response = cam.Streaming.channels[102].picture(method='get', type='opaque_data')

    # if debug: 
    #     print(response)
    
    return response.iter_content(chunk_size=1024)
    
