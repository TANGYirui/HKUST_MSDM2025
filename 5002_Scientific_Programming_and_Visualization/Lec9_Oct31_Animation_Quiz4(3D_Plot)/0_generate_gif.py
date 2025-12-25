import imageio 

def create_gif(image_list, gif_name, dura):
    # Save them as frames into a gif  
    all_images = []    
    for image_name in image_list:        
        all_images.append(imageio.imread(image_name))      
        imageio.mimsave(gif_name, all_images, 'GIF', duration = dura)     
    return 

image_list=[]
image_list=['first.png']
for ni in range(40):
    image_list.append(str(ni)+'.png')

image_list.append('last.png')

gif_name = 'plot_circle.gif'    

create_gif(image_list, gif_name,0.5)


