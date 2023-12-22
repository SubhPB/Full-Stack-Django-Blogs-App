from users.models import NewUser as User
from blog.models import Category, Post

chat_gpt_json = [
    {
        "title": "Exploring the World of Coffee: From Bean to Cup",
        "category": {
            "id": 45,
            "name": "food"
        },
        "excerpt": "Dive into the journey of coffee, understanding its origins, roasting processes, and brewing techniques.",
        "image_url": "https://example.com/coffee.jpg",
        "content": "This article explores the fascinating world of coffee, tracing its journey from bean to cup. It covers the history of coffee cultivation, different bean varieties, roasting techniques, and brewing methods, providing a comprehensive guide for coffee enthusiasts.",
        "status": "published",
        "image": "http://localhost/media/images/coffee.jpg",
        "author": "Emily Durant",
        "email": "emily.durant@example.com"
    },
    {
        "title": "Yoga for Mental Well-being: A Holistic Approach",
        "category": {
            "id": 12,
            "name": "health"
        },
        "excerpt": "Discover the benefits of yoga on mental health and how it can be a tool for stress relief and mindfulness.",
        "image_url": "https://example.com/yoga.jpg",
        "content": "This article highlights the importance of yoga for mental well-being. It discusses various yoga poses and techniques that can aid in stress relief, mindfulness, and emotional balance, making yoga a holistic approach to mental health.",
        "status": "published",
        "image": "http://localhost/media/images/yoga.jpg",
        "author": "Alex Johnson",
        "email": "alex.johnson@example.com"
    },
    {
        "title": "Urban Gardening: Cultivating Green Spaces in the City",
        "category": {
            "id": 21,
            "name": "lifestyle"
        },
        "excerpt": "Learn how to create and maintain a thriving garden in urban settings, making the most of limited space.",
        "image_url": "https://example.com/urban-gardening.jpg",
        "content": "This article focuses on urban gardening, offering practical advice for creating green spaces in city environments. It covers techniques for container gardening, vertical gardens, and using small spaces effectively, providing city dwellers with a guide to cultivating their own urban oasis.",
        "status": "published",
        "image": "http://localhost/media/images/urban-gardening.jpg",
        "author": "Laura Green",
        "email": "laura.green@example.com"
    },
    {
        "title": "The Marvels of Modern Architecture: An Exploration",
        "category": {
            "id": 34,
            "name": "technology"
        },
        "excerpt": "Discover the innovations in modern architecture, exploring groundbreaking designs and sustainable building practices.",
        "image_url": "https://example.com/modern-architecture.jpg",
        "content": "This article delves into the marvels of modern architecture, showcasing innovative designs and sustainable building practices. It highlights key architects, famous buildings, and the integration of technology in contemporary architectural projects.",
        "status": "published",
        "image": "http://localhost/media/images/modern-architecture.jpg",
        "author": "Mark Thompson",
        "email": "mark.thompson@example.com"
    },
    {
        "title": "The Art of Mindfulness: Techniques for Everyday Life",
        "category": {
            "id": 12,
            "name": "health"
        },
        "excerpt": "Learn about the practice of mindfulness and its benefits for mental health, stress reduction, and overall well-being.",
        "image_url": "https://example.com/mindfulness.jpg",
        "content": "This article explores the art of mindfulness, offering techniques and exercises to incorporate mindfulness into everyday life. It discusses the benefits of mindful living for mental health, stress reduction, and enhancing the quality of daily experiences.",
        "status": "published",
        "image": "http://localhost/media/images/mindfulness.jpg",
        "author": "Sarah Lee",
        "email": "sarah.lee@example.com"
    },
    {
        "title": "Sustainable Fashion: The Future of Clothing",
        "category": {
            "id": 63,
            "name": "environment"
        },
        "excerpt": "Explore the concept of sustainable fashion, understanding its impact on the environment and how to make ethical choices.",
        "image_url": "https://example.com/sustainable-fashion.jpg",
        "content": "This article discusses the rising trend of sustainable fashion. It covers the environmental impact of the fashion industry and how consumers can make more ethical and sustainable choices in their clothing.",
                "status": "published",
        "image": "http://localhost/media/images/mindfulness.jpg",
        "author": "Sarah Lee",
        "email": "sarah.lee@example.com"
    }
]    




imgs = [
    'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/235922/pexels-photo-235922.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/173301/pexels-photo-173301.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2526491/pexels-photo-2526491.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/810775/pexels-photo-810775.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1328545/pexels-photo-1328545.jpeg?auto=compress&cs=tinysrgb&w=400'
]
# imgs_by_pexels = [ {k,v} if not (k == '') for index,item in enumerate(chat_gpt_json) for k,v in item.items()]
def generate(pexel_images,json_data):
    imgs_by_pexels = [{}] * len(json_data)

    try:

        for ind,item in enumerate(json_data):

            for key,value in item.items():
                
                if key == 'category':
                    del value['id']

                elif key == 'image_url':
                    item[key] = pexel_images[ind]

                elif key == 'image':
                    continue

                
            imgs_by_pexels[ind] = item

        return imgs_by_pexels

    except:
        raise Exception


# refined_data = generate(pexel_images=imgs,json_data=chat_gpt_json)


# def create_data(refined_data):

#     for item in refined_data:
#         ...

def get_or_create():
    json_data = generate(pexel_images=imgs,json_data=chat_gpt_json)

    

    try:

        for data in json_data:
            
            user, user_created = User.objects.get_or_create(email=data['email'],defaults={
                'user_name': data['author'],
                'first_name': data['author'].split()[0],
                'last_name': data['author'].split()[1] if len(data['author'].split()) > 1 else None,
            })
            if user_created:
                user.set_password(data['author'].split()[0] + '123')
                user.save()
                print("A new user has been created in sysytem")

            else:
                print(f"{user.user_name} exists in the system")   


            category , category_created = Category.objects.get_or_create(name=data['category']['name'])  

            if category_created:
                print(" A new category {0} was created".format(category.name))  
        
            blog = Post.objects.create(
                category = category,
                title = data['title'],
                excerpt= data['excerpt'],
                content= data['content'],
                author=user,
                status=data['status'],
                image_url= data['image_url']
            )

            print(" blog has been saved {0}".format(blog.title))
        
    except:
        print('Something went wrong')
        raise Exception
    