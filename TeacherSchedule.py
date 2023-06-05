attachments = []
images = []
img = Image.new('RGB', (len(urls) * 50, 50))
for i in range(len(urls)):
    image = requests.get(urls[i], stream=True)
    images.append(image)
    with open(f'{i}.png', "wb") as f:
        f.write(image.content)
    img1 = Image.open("file1.png")
    img2 = Image.open("file2.png")
    img.paste(img1, (0, 0))
    img.paste(img2, (50, 0))
    img.save("image.png")
    photo = self.upload.photo_messages(photos=image.raw)[0]
    attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
self.vk_session.method('messages.send',
                       {'user_id': u_id,
                        'message': weather_str,
                        'random_id': get_random_id(), 'attachment': ','.join(attachments)})