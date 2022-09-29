import random
import os
import torch
import numpy as np
import shutil
import PIL
from PIL import Image
from einops import rearrange, repeat
from torch import autocast
from diffusers import StableDiffusionPipeline
import webbrowser
from deep_translator import GoogleTranslator
from langdetect import detect
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
model_id = "CompVis/stable-diffusion-v1-4"
#device = "cuda"
device = "mps" #torch.device("mps")

white = (255, 255, 255)
green = (0, 255, 0)
darkgreen = (0, 128, 0)
red = (255, 0, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

os.environ["skl"] = "nn"
os.environ["epsilon"] = "0.005"
os.environ["decay"] = "0."
os.environ["ngoptim"] = "DiscreteLenglerOnePlusOne"
os.environ["forcedlatent"] = ""
#os.environ["enforcedlatent"] = ""
os.environ["good"] = "[]"
os.environ["bad"] = "[]"
num_iterations = 50
gs = 7.5



import pyttsx3

noise = pyttsx3.init()
noise.setProperty("rate", 178)
noise.setProperty('voice', 'mb-us1')                                            

#voice = noise.getProperty('voices')
#for v in voice:
#    if v.name == "Kyoko":
#        noise.setProperty('voice', v.id)


all_selected = []
forcedlatents = []



pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token="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")
pipe = pipe.to(device)

prompt = "a photo of an astronaut riding a horse on mars"
prompt = "a photo of a red panda with a hat playing table tennis"
prompt = "a photorealistic portrait of " + random.choice(["Mary Cury", "Scarlett Johansson", "Marilyn Monroe", "Poison Ivy", "Black Widow", "Medusa", "Batman", "Albert Einstein", "Louis XIV", "Tarzan"]) + random.choice([" with glasses", " with a hat", " with a cigarette", "with a scarf"])
prompt = "a photorealistic portrait of " + random.choice(["Nelson Mandela", "Superman", "Superwoman", "Volodymyr Zelenskyy", "Tsai Ing-Wen", "Lzzy Hale", "Meg Myers"]) + random.choice([" with glasses", " with a hat", " with a cigarette", "with a scarf"])
prompt = random.choice(["A woman with three eyes", "Meg Myers", "The rock band Ankor", "Miley Cyrus", "The man named Rahan", "A murder", "Rambo playing table tennis"])
prompt = "Photo of a female Terminator."
prompt = random.choice([
     "Photo of Tarzan as a lawyer with a tie",
     "Photo of Scarlett Johansson as a sumo-tori",
     "Photo of the little mermaid as a young black girl",
     "Photo of Schwarzy with tentacles",
     "Photo of Meg Myers with an Egyptian dress",
     "Photo of Schwarzy as a ballet dancer",
    ])


name = random.choice(["Mark Zuckerbeg", "Zendaya", "Yann LeCun", "Scarlett Johansson", "Superman", "Meg Myers"])
name = "Zendaya"
prompt = f"Photo of {name} as a sumo-tori."

prompt = "Full length portrait of Mark Zuckerberg as a Sumo-Tori."
prompt = "Full length portrait of Scarlett Johansson as a Sumo-Tori."
prompt = "A close up photographic portrait of a young woman with uniformly colored hair."
prompt = "Zombies raising and worshipping a flying human."
prompt = "Zombies trying to kill Meg Myers."
prompt = "Meg Myers with an Egyptian dress killing a vampire with a gun."
prompt = "Meg Myers grabbing a vampire by the scruff of the neck."
prompt = "Mark Zuckerberg chokes a vampire to death."
prompt = "Mark Zuckerberg riding an animal."
prompt = "A giant cute animal worshipped by zombies."


prompt = "Several faces."

prompt = "An armoured Yann LeCun fighting tentacles in the jungle."
prompt = "Tentacles everywhere."
prompt = "A photo of a smiling Medusa."
prompt = "Medusa."
prompt = "Meg Myers in bloody armor fending off tentacles with a sword."
prompt = "A red-haired woman with red hair. Her head is tilted."
prompt = "A bloody heavy-metal zombie with a chainsaw."
prompt = "Tentacles attacking a bloody Meg Myers in Eyptian dress. Meg Myers has a chainsaw."
prompt = "Bizarre art."

prompt = "Beautiful bizarre woman."
prompt = "Yann LeCun as the grim reaper: bizarre art."
prompt = "A star with flashy colors."
prompt = "Un chat en sang et en armure joue de la batterie."
prompt = "Photo of a cyberpunk Mark Zuckerberg killing Cthulhu with a light saber."
prompt = "A ferocious cyborg bear."
prompt = "Photo of Mark Zuckerberg killing Cthulhu with a light saber."
prompt = "A bear with horns and blood and big teeth."
prompt = "A photo of a bear and Yoda, good friends."
prompt = "A photo of Yoda on the left, a blue octopus on the right, an explosion in the center."
prompt = "A bird is on a hippo. They fight a black and red octopus. Jungle in the background."
prompt = "A flying white owl above 4 colored pots with fire. The owl has a hat."
prompt = "A flying white owl above 4 colored pots with fire."
prompt = "An armored Mark Zuckerberg fighting off a monster with bloody tentacles in the jungle with a light saber."
print(f"The prompt is {prompt}")


import pyfiglet
print(pyfiglet.figlet_format("Welcome in Genetic Stable Diffusion !"))
print(pyfiglet.figlet_format("First, let us choose the text :-)!"))



print(f"Francais: Proposez un nouveau texte si vous ne voulez pas dessiner << {prompt} >>.\n")
noise.say("Hey!")
noise.runAndWait()
user_prompt = input(f"English: Enter a new prompt if you prefer something else than << {prompt} >>.\n")
if len(user_prompt) > 2:
    prompt = user_prompt

# On the fly translation.
language = detect(prompt)
english_prompt = GoogleTranslator(source='auto', target='en').translate(prompt)

def to_native(stri):
    return GoogleTranslator(source='en', target=language).translate(stri)

def pretty_print(stri):
    print(pyfiglet.figlet_format(to_native(stri)))

print(f"{to_native('Working on')} {english_prompt}, a.k.a {prompt}.")

def eg(list_of_files):
    pretty_print("Should I convert images below to high resolution ?")
    print(list_of_files)
    noise.say("Hey!")
    noise.runAndWait()
    answer = input(" [y]es / [n]o ?")
    if "y" in answer or "Y" in answer:
        model = RealESRGAN(device, scale=4)
        model.load_weights('weights/RealESRGAN_x4.pth', download=True)
        for f in list_of_files:
            import torch
            from PIL import Image
            import numpy as np
            from RealESRGAN import RealESRGAN
            
            #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            path_to_image = f
            image = Image.open(path_to_image).convert('RGB')
            sr_image = model.predict(image)
            output_filename = "SR" + f
            sr_image.save(output_filename)
            print(to_native(f"Created the super-resolution file {output_filename}")) 

def stop_all(list_of_files):
    print(to_native("Your selected images and the last generation:"))
    print(list_of_files)
    eg(all_selected + onlyfiles)
    pretty_print("Should we create a meme ?")
    answer = input(" [y]es or [n]o ?")
    if "y" in answer or "Y" in answer:
        url = 'https://imgflip.com/memegenerator'
        webbrowser.open(url)
    pretty_print("Good bye!")
    exit()


import os
import pygame
from os import listdir
from os.path import isfile, join
      
sentinel = str(random.randint(0,100000)) + "XX" +  str(random.randint(0,100000))

all_files = []

llambda = 15

assert llambda < 16, "lambda < 16 for convenience in pygame."

bad = []
five_best = []
latent = []
images = []
onlyfiles = []

pretty_print("Now let us choose (if you want) an image as a start.")
image_name = input(to_native("Name of image for starting ? (enter if no start image)"))

# activate the pygame library .
pygame.init()
X = 2000  # > 1500 = buttons
Y = 900  
scrn = pygame.display.set_mode((1700, Y + 100))
font = pygame.font.Font('freesansbold.ttf', 22)
bigfont = pygame.font.Font('freesansbold.ttf', 44)

def load_img(path):
    image = Image.open(path).convert("RGB")
    w, h = image.size
    print(to_native(f"loaded input image of size ({w}, {h}) from {path}"))
    w, h = map(lambda x: x - x % 32, (w, h))  # resize to integer multiple of 32
    image = image.resize((512, 512), resample=PIL.Image.LANCZOS)
    #image = image.resize((w, h), resample=PIL.Image.LANCZOS)
    image = np.array(image).astype(np.float32) / 255.0
    image = image[None].transpose(0, 3, 1, 2)
    image = torch.from_numpy(image)
    return 2.*image - 1.

if len(image_name) > 0:
    pretty_print("Importing an image !")
    import torchvision
    #forced_latent = pipe.get_latent(torchvision.io.read_image(image_name).float())
    model = pipe.vae
    try:
        init_image = load_img(image_name).to(device)
    except:
        pretty_print("Try again!")
        image_name = input(to_native("Name of image for starting ? (enter if no start image)"))
        pretty_print("Loading failed!!")
        
    base_init_image = load_img(image_name).to(device)
    noise.say("Image loaded")
    noise.runAndWait()
    print(base_init_image.shape)
    print(np.max(base_init_image.cpu().detach().numpy().flatten()))
    print(np.min(base_init_image.cpu().detach().numpy().flatten()))
    forcedlatents = []
    divider = 1.5
    for i in range(llambda):
        new_base_init_image = base_init_image
        if (i % 7)  == 1:
            new_base_init_image[0,0,:,:] /= divider
        if (i % 7) == 2:
            new_base_init_image[0,1,:,:] /= divider
        if (i % 7) == 3:
            new_base_init_image[0,2,:,:] /= divider
        if (i % 7) == 4:
            new_base_init_image[0,0,:,:] /= divider
            new_base_init_image[0,1,:,:] /= divider
        if (i % 7) == 5:
            new_base_init_image[0,1,:,:] /= divider
            new_base_init_image[0,2,:,:] /= divider
        if (i % 7) == 6:
            new_base_init_image[0,0,:,:] /= divider
            new_base_init_image[0,2,:,:] /= divider
           
        c = np.exp(np.random.randn() - 2)
        init_image_shape = base_init_image.cpu().numpy().shape
        if i > 0:
            init_image = new_base_init_image + torch.from_numpy(c * np.random.randn(np.prod(init_image_shape))).reshape(init_image_shape).float().to(device)
        else:
            init_image = new_base_init_image
        init_image = repeat(init_image, '1 ... -> b ...', b=1)
        forced_latent = 6. * model.encode(init_image.to(device)).latent_dist.sample()
        new_fl = forced_latent.cpu().detach().numpy().flatten()
        basic_new_fl = new_fl  #np.sqrt(len(new_fl) / sum(new_fl ** 2)) * new_fl
        #new_fl = forced_latent + (1. / 1.1**(llambda-i)) * torch.from_numpy(np.random.randn(1*4*64*64).reshape(1,4,64,64)).float().to(device)
        #forcedlatents += [new_fl.cpu().detach().numpy()]
        if i > 0:
            #epsilon = 0.3 / 1.1**i
            #basic_new_fl = np.sqrt(len(new_fl) / np.sum(new_fl**2)) * basic_new_fl
            epsilon = 1.0 / 2**(2 + i / 6)
            new_fl = epsilon * basic_new_fl + (1 - epsilon) * np.random.randn(1*4*64*64)
        else:
            new_fl = basic_new_fl
        #new_fl = np.sqrt(len(new_fl)) * new_fl / np.sqrt(np.sum(new_fl ** 2))
        forcedlatents += [new_fl] #np.clip(new_fl, -3., 3.)] #np.sqrt(len(new_fl) / sum(new_fl ** 2)) * new_fl]
        #forcedlatents += [np.sqrt(len(new_fl) / sum(new_fl ** 2)) * new_fl]
        #print(f"{i} --> {forcedlatents[i][:10]}")

# We start the big loop!
for iteration in range(30):
    latent = [latent[f] for f in five_best]
    images = [images[f] for f in five_best]
    onlyfiles = [onlyfiles[f] for f in five_best]
    early_stop = []
    noise.say("WAIT!")
    noise.runAndWait()
    for k in range(llambda):
        if len(forcedlatents) > 0 and k < len(forcedlatents):
            os.environ["forcedlatent"] = str(list(forcedlatents[k].flatten()))            
        if k < len(five_best):
            imp = pygame.transform.scale(pygame.image.load(onlyfiles[k]).convert(), (300, 300))
            # Using blit to copy content from one surface to other
            scrn.blit(imp, (300 * (k // 3), 300 * (k % 3)))
            pygame.display.flip()
            continue
        if len(early_stop) > 0:
            break
        pygame.draw.rect(scrn, black, pygame.Rect(0, Y, 1700, Y+100))
        pygame.draw.rect(scrn, black, pygame.Rect(1500, 0, 2000, Y+100))
        text0 = bigfont.render(to_native(f'Please wait !!! {k} / {llambda}'), True, green, blue)
        scrn.blit(text0, ((X*3/4)/2 - X/32, Y/2-Y/4))
        text0 = font.render(to_native(f'Or, if you find one image very cool and want to focus on it only,'), True, green, blue)
        scrn.blit(text0, ((X*3/4)/3 - X/32, Y/2-Y/8))
        text0 = font.render(to_native(f'then click on it AND KEEP THE MOUSE AT THE SAME POINT until I get the click.'), True, green, blue)
        scrn.blit(text0, ((X*3/4)/3 - X/32, Y/2))
        text0 = font.render(to_native(f'Then I''ll work on variants of that specific image.'), True, green, blue)
        scrn.blit(text0, ((X*3/4)/2 - X/32, Y/2+Y/8))

        # Button for early stopping
        text2 = font.render(to_native('Click here for stopping, '), True, green, blue)
        text2 = pygame.transform.rotate(text2, 90)
        scrn.blit(text2, (X*3/4+X/16      - X/32, Y/3))
        text2 = font.render(to_native('and get the effects,'), True, green, blue)
        text2 = pygame.transform.rotate(text2, 90)
        scrn.blit(text2, (X*3/4+X/16+X/64 - X/32, Y/3))
        text2 = font.render(to_native('or for creating a meme.'), True, green, blue)
        text2 = pygame.transform.rotate(text2, 90)
        scrn.blit(text2, (X*3/4+X/16+X/32 - X/32, Y/3))

        pygame.display.flip()
        os.environ["earlystop"] = "False" if k > len(five_best) else "True"
        os.environ["epsilon"] = str(0. if k == len(five_best) else (k - len(five_best)) / llambda)
        os.environ["budget"] = str(np.random.randint(400) if k > len(five_best) else 2)
        os.environ["skl"] = {0: "nn", 1: "tree", 2: "logit"}[k % 3]
        #enforcedlatent = os.environ.get("enforcedlatent", "")
        #if len(enforcedlatent) > 2:
        #    os.environ["forcedlatent"] = enforcedlatent
        #    os.environ["enforcedlatent"] = ""
        with autocast("cuda"):
            image = pipe(english_prompt, guidance_scale=gs, num_inference_steps=num_iterations)["sample"][0]
            images += [image]
        filename = f"SD_{prompt.replace(' ','_')}_image_{sentinel}_{iteration:05d}_{k:05d}.png"  
        image.save(filename)
        onlyfiles += [filename]
        imp = pygame.transform.scale(pygame.image.load(onlyfiles[-1]).convert(), (300, 300))
        # Using blit to copy content from one surface to other
        scrn.blit(imp, (300 * (k // 3), 300 * (k % 3)))
        pygame.display.flip()
        #noise.say("Dong")
        #noise.runAndWait()
        print('\a')
        str_latent = eval((os.environ["latent_sd"]))
        array_latent = eval(f"np.array(str_latent).reshape(4, 64, 64)")
        print(f"Debug info: array_latent sumsq/var {sum(array_latent.flatten() ** 2) / len(array_latent.flatten())}")
        latent += [array_latent]
        with open(f"SD_{prompt.replace(' ','_')}_latent_{sentinel}_{k}.txt", 'w') as f:
            f.write(f"{latent}")
        # In case of early stopping.
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONUP:
                noise.say("Ok I stop")
                noise.runAndWait()
                pos = pygame.mouse.get_pos()
                index = 3 * (pos[0] // 300) + (pos[1] // 300)
                if pos[0] > X and pos[1] > Y /3 and pos[1] < 2*Y/3:
                    stop_all(all_selected)
                    exit()
                if index <= k:
                    pretty_print(("You clicked for requesting an early stopping."))
                    early_stop = [pos]
                    break
                #early_stop = [(k - 1, .5,.5)]
                pretty_print("I do not understand your click.")
                pretty_print("So I assume you want the last image...")
    
    # Stop the forcing from disk!
    #os.environ["enforcedlatent"] = ""
    # importing required library
    
    #mypath = "./"
    #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #onlyfiles = [str(f) for f in onlyfiles if "SD_" in str(f) and ".png" in str(f) and str(f) not in all_files and sentinel in str(f)]
    #print()
     
    # create the display surface object
    # of specific dimension..e(X, Y).
    if len(early_stop) == 0:
        noise.say("Ok I'm ready!")
        noise.runAndWait()
    # Add rectangles
    pygame.draw.rect(scrn, red, pygame.Rect(X*3/4, 0, X*3/4+X/16+X/32, Y/3), 2)
    pygame.draw.rect(scrn, red, pygame.Rect(X*3/4, Y/3, X*3/4+X/16+X/32, 2*Y/3), 2)
    pygame.draw.rect(scrn, red, pygame.Rect(X*3/4, 2*Y/3, X*3/4+X/16+X/32, Y), 2)
    pygame.draw.rect(scrn, red, pygame.Rect(0, Y, X/2, Y+100), 2)

    # Button for loading a starting point
    text1 = font.render('Manually edit an image.', True, green, blue)
    text1 = pygame.transform.rotate(text1, 90)
    #scrn.blit(text1, (X*3/4+X/16 - X/32, 0))
    #text1 = font.render('& latent    ', True, green, blue)
    #text1 = pygame.transform.rotate(text1, 90)
    #scrn.blit(text1, (X*3/4+X/16+X/32 - X/32, 0))

    # Button for creating a meme
    text2 = font.render(to_native('Click <here>,'), True, green, blue)
    text2 = pygame.transform.rotate(text2, 90)
    scrn.blit(text2, (X*3/4+X/16 - X/32, Y/3+10))
    text2 = font.render(to_native('for finishing with effects.'), True, green, blue)
    text2 = pygame.transform.rotate(text2, 90)
    scrn.blit(text2, (X*3/4+X/16+X/32 - X/32, Y/3+10))
    # Button for new generation
    text3 = font.render(to_native(f"I don't want to select images"), True, green, blue)
    text3 = pygame.transform.rotate(text3, 90)
    scrn.blit(text3, (X*3/4+X/16 - X/32, Y*2/3+10))
    text3 = font.render(to_native(f"Just rerun."), True, green, blue)
    text3 = pygame.transform.rotate(text3, 90)
    scrn.blit(text3, (X*3/4+X/16+X/32 - X/32, Y*2/3+10))
    text4 = font.render(to_native(f"Modify parameters or text!"), True, green, blue)
    scrn.blit(text4, (300, Y + 30))
    pygame.display.flip()

    if len(early_stop) == 0:
        for idx in range(llambda):
            # set the pygame window name
            pygame.display.set_caption(prompt)
            imp = pygame.transform.scale(pygame.image.load(onlyfiles[idx]).convert(), (300, 300))
            scrn.blit(imp, (300 * (idx // 3), 300 * (idx % 3)))
     
    # paint screen one time
    pygame.display.flip()
    status = True
    indices = []
    good = []
    five_best = []
    for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONUP:
            print(to_native(".... too early for clicking !!!!"))


    pretty_print("Please click on your favorite elements!")
    print(to_native("You might just click on one image and we will provide variations."))
    print(to_native("Or you can click on the top of an image and the bottom of another one."))
    print(to_native("Click on the << new generation >> when you're done.")) 
    while (status):
     
      # iterate over the list of Event objects
      # that was returned by pygame.event.get() method.
        for i in early_stop + pygame.event.get():
            if hasattr(i, "type") and i.type == pygame.MOUSEBUTTONUP or len(early_stop) > 0:
                pos = early_stop[0] if len(early_stop) > 0 else pygame.mouse.get_pos() 
                pretty_print(f"Detected! Click at {pos}")
                if pos[1] > Y:
                    pretty_print("Let us update parameters!")
                    text4 = font.render(to_native(f"ok, go to text window!"), True, green, blue)
                    scrn.blit(text4, (300, Y + 30))
                    pygame.display.flip()
                    try:
                        num_iterations = int(input(to_native(f"Number of iterations ? (current = {num_iterations})\n")))
                    except:
                        num_iterations = int(input(to_native(f"Number of iterations ? (current = {num_iterations})\n")))
                    gs = float(input(to_native(f"Guidance scale ? (current = {gs})\n")))
                    print(to_native(f"The current text is << {prompt} >>."))
                    print(to_native("Start your answer with a symbol << + >> if this is an edit and not a new text.")) 
                    new_prompt = str(input(to_native(f"Enter a text if you want to change from ") + prompt))
                    if len(new_prompt) > 2:
                        if new_prompt[0] == "+":
                            prompt += new_prompt[1:]
                        else:
                            prompt = new_prompt
                        language = detect(prompt)
                        english_prompt = GoogleTranslator(source='auto', target='en').translate(prompt)
                    pretty_print("Ok! Parameters updated.")
                    pretty_print("==> go back to the window!")
                    text4 = font.render(to_native(f"Ok! parameters changed!"), True, green, blue)
                    scrn.blit(text4, (300, Y + 30))
                    pygame.display.flip()
                elif pos[0] > 1500:  # Not in the images.
                    if pos[1] < Y/3:
                        #filename = input(to_native("Filename (please provide the latent file, of the format SD*latent*.txt) ?\n"))
                        #status = False
                        #with open(filename, 'r') as f:
                        #     latent = f.read()
                        #break
                        pretty_print("Easy! I exit now, you edit the file and you save it.")
                        pretty_print("Then just relaunch me and provide the text and the image.")
                        exit()
                    if pos[1] < 2*Y/3:
                        #onlyfiles = [f for f in listdir(".") if isfile(join(mypath, f))]
                        #onlyfiles = [str(f) for f in onlyfiles if "SD_" in str(f) and ".png" in str(f) and str(f) not in all_files and sentinel in str(f)]
                        stop_all(all_selected + onlyfiles)
                        exit()
                    status = False
                    break
                index = 3 * (pos[0] // 300) + (pos[1] // 300)
                pygame.draw.circle(scrn, red, [pos[0], pos[1]], 3, 0)
                selected_filename = to_native("Selected") + onlyfiles[index]
                shutil.copyfile(onlyfiles[index], selected_filename)
                all_selected += [selected_filename]
                if index not in five_best and len(five_best) < 5:
                    five_best += [index]
                indices += [[index, (pos[0] - (pos[0] // 300) * 300) / 300, (pos[1] - (pos[1] // 300) * 300) / 300]]
                # Update the button for new generation.
                pygame.draw.rect(scrn, black, pygame.Rect(X*3/4, 2*Y/3, X*3/4+X/16+X/32, Y))
                pygame.draw.rect(scrn, red, pygame.Rect(X*3/4, 2*Y/3, X*3/4+X/16+X/32, Y), 2)
                text3 = font.render(to_native(f"  You have chosen {len(indices)} images:"), True, green, blue)
                text3 = pygame.transform.rotate(text3, 90)
                scrn.blit(text3, (X*3/4+X/16 - X/32, Y*2/3))
                text3 = font.render(to_native(f"  Click <here> for new generation!"), True, green, blue)
                text3 = pygame.transform.rotate(text3, 90)
                scrn.blit(text3, (X*3/4+X/16+X/32 - X/32, Y*2/3))
                pygame.display.flip()
                #text3Rect = text3.get_rect()
                #text3Rect.center = (750+750*3/4, 1000)
                good += [list(latent[index].flatten())]
    
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if len(early_stop) > 0 or i.type == pygame.QUIT:
                status = False
     
    # Covering old images with full circles.
    for _ in range(123):
        x = np.random.randint(1500)
        y = np.random.randint(900)
        pygame.draw.circle(scrn, darkgreen,
                           [x, y], 17, 0)
    pygame.display.update()
    if len(indices) == 0:
        print("The user did not like anything! Rerun :-(")
        continue
    print(f"Clicks at {indices}")
    os.environ["mu"] = str(len(indices))
    forcedlatents = []
    bad += [list(latent[u].flatten()) for u in range(len(onlyfiles)) if u not in [i[0] for i in indices]]
    sauron = 0 * latent[0]
    for u in [u for u in range(len(onlyfiles)) if u not in [i[0] for i in indices]]:
        sauron += latent[u]
    sauron = (1 / len([u for u in range(len(onlyfiles)) if u not in [i[0] for i in indices]])) * sauron
    if len(bad) > 300:
        bad = bad[(len(bad) - 300):]
    print(to_native(f"{len(indices)} indices are selected."))
    #print(f"indices = {indices}")
    for a in range(llambda):
        forcedlatent = np.zeros((4, 64, 64))
        os.environ["good"] = str(good)
        os.environ["bad"] = str(bad)
        coefficients = np.zeros(len(indices))
        for i in range(len(indices)):
            coefficients[i] = np.exp(2. * np.random.randn())
        for i in range(64):
            x = i / 63.
            for j in range(64):
                y = j / 63
                mindistances = 10000000000.
                for u in range(len(indices)):
                    #print(a, i, x, j, y, u)
                    #print(indices[u][1])
                    #print(indices[u][2])
                    #print(f"  {coefficients[u]}* np.linalg.norm({np.array((x, y))}-{np.array((indices[u][1], indices[u][2]))}")
                    distance = coefficients[u] * np.linalg.norm( np.array((x, y)) - np.array((indices[u][1], indices[u][2])) )
                    if distance < mindistances:
                        mindistances = distance
                        uu = indices[u][0]
                for k in range(4):
                    assert k < len(forcedlatent), k
                    assert i < len(forcedlatent[k]), i
                    assert j < len(forcedlatent[k][i]), j
                    assert uu < len(latent)
                    assert k < len(latent[uu]), k
                    assert i < len(latent[uu][k]), i
                    assert j < len(latent[uu][k][i]), j
                    forcedlatent[k][i][j] = float(latent[uu][k][i][j])
        #if a % 2 == 0:
        #    forcedlatent -= np.random.rand() * sauron
        basic_new_fl = np.sqrt(len(forcedlatent) / np.sum(forcedlatent**2)) * forcedlatent
        epsilon = (a / (llambda - 1)) ** 3
        forcedlatent = (1. - epsilon) * basic_new_fl.flatten() + epsilon * np.random.randn(4*64*64)
        forcedlatent = np.sqrt(len(forcedlatent) / np.sum(forcedlatent**2)) * forcedlatent
        forcedlatents += [forcedlatent]
    #for uu in range(len(latent)):
    #    print(f"--> latent[{uu}] sum of sq / variable = {np.sum(latent[uu].flatten()**2) / len(latent[uu].flatten())}")
            
pygame.quit()
