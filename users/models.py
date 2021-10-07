from django.db import models
from django.contrib.auth.models import User
from PIL import Image

def crop_center(pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))
                             
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.gif', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            img_thumb = crop_max_square(img).resize((300, 300), Image.LANCZOS)
            img = img_thumb
            img.save(self.image.path)
        
    # bio = 
    # school = 
    # work = 
    # phone = 
    
    