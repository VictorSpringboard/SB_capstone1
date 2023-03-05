<<<<<<< HEAD
from models import db, connect_db, User, Favorite, Grocery
from app import app
import datetime

=======
from models import db, connect_db, User, Favorite, Match
from app import app
import datetime
import requests
from secrets import API_KEY
from sqlalchemy.exc import IntegrityError
>>>>>>> messages

connect_db(app)
app.app_context().push()

<<<<<<< HEAD
db.drop_all()
db.create_all()
=======
def drop_create():
    db.drop_all()
    db.create_all()
>>>>>>> messages



users = [
    {
<<<<<<< HEAD
        'id': 0,
        'username': 'test',
        'password': 'test',
        'email': 'test@test.com'
    },
    {
        'id': 1,
        'username': 'HankHill',
        'password': 'propane',
        'email': 'hank@strickland.com'
    },
    {
        'id': 2,
        'username': 'PeggyHill',
        'password': 'boggle',
        'email': 'peggy@boggle.com'
    },
    {
        'id': 3,
        'username': 'BobbyHill',
        'password': 'comedy',
        'email': 'bobby@thatsmypurse.com'
    },
    {
        'id': 4,
        'username': 'Boomhauer',
        'password': 'dang',
        'email': 'dangole@talkinbout.com'
    },
]

for user in users:
    new = User.register_user(id=user['id'],
                username=user['username'],
                pwd=user['password'],
                email=user['email'])
    db.session.add(new)
    db.session.commit()


recipes = [
    {
        'user_id':1,
        'recipe_id': 52885,
        'title': 'Bubble & Squeak',
        'instructions': "Melt the fat in a non-stick pan, allow it to get nice and hot, then add the bacon. As it begins to brown, add the onion and garlic. Next, add the sliced sprouts or cabbage and let it colour slightly. All this will take 5-6 mins.\r\nNext, add the potato. Work everything together in the pan and push it down so that the mixture covers the base of the pan – allow the mixture to catch slightly on the base of the pan before turning it over and doing the same again. It’s the bits of potato that catch in the pan that define the term ‘bubble and squeak’, so be brave and let the mixture colour. Cut into wedges and serve.",
        'ingredients': 'Butter | Bacon | Onion | Garlic Clove | Brussels Sprouts | Potatoes', 
        'measurements': '1 tbs | 4 | 1 finely sliced | 1 chopped | 20 | 400g',
        'category': 'Pork',
        'area': 'British',
        'original': 'https://www.bbcgoodfood.com/recipes/164622/bubble-and-squeak'
},
    {
        'user_id':1,
        'recipe_id': 52893,
        'title': 'Apple & Blackberry Crumble',
        'instructions': "Heat oven to 190C/170C fan/gas 5. Tip the flour and sugar into a large bowl. Add the butter, then rub into the flour using your fingertips to make a light breadcrumb texture. Do not overwork it or the crumble will become heavy. Sprinkle the mixture evenly over a baking sheet and bake for 15 mins or until lightly coloured.\r\nMeanwhile, for the compote, peel, core and cut the apples into 2cm dice. Put the butter and sugar in a medium saucepan and melt together over a medium heat. Cook for 3 mins until the mixture turns to a light caramel. Stir in the apples and cook for 3 mins. Add the blackberries and cinnamon, and cook for 3 mins more. Cover, remove from the heat, then leave for 2-3 mins to continue cooking in the warmth of the pan.\r\nTo serve, spoon the warm fruit into an ovenproof gratin dish, top with the crumble mix, then reheat in the oven for 5-10 mins. Serve with vanilla ice cream.",
        'ingredients': 'Plain Flour | Caster Sugar | Butter | Braeburn Apples | Butter | Demerara Sugar | Blackberrys | Cinnamon | Ice Cream', 
        'measurements': '120g | 60g | 30g | 300g | 30g | 120g | ¼ teaspoon | to serve',
        'category': 'Dessert',
        'area': 'British',
        'original': 'https://www.bbcgoodfood.com/recipes/778642/apple-and-blackberry-crumble'
},
    {
        'user_id':2,
        'recipe_id': 52939,
        'title': 'Callaloo Jamaican Style',
        'instructions': "'Cut leaves and soft stems from the kale branches, them soak in a bowl of cold water for about 5-10 minutes or until finish with prep.\r\nProceed to slicing the onions, mincing the garlic and dicing the tomatoes. Set aside\r\nRemove kale from water cut in chunks.\r\nPlace bacon on saucepan and cook until crispy. Then add onions, garlic, thyme, stir for about a minute or more\r\nAdd tomatoes; scotch bonnet pepper, smoked paprika. Sauté for about 2-3 more minutes.\r\nFinally add vegetable, salt, mix well, and steamed for about 6-8 minutes or until leaves are tender. Add a tiny bit of water as needed. Adjust seasonings and turn off the heat.\r\nUsing a sharp knife cut both ends off the plantain. This will make it easy to grab the skin of the plantains. Slit a shallow line down the long seam of the plantain; peel only as deep as the peel. Remove plantain peel by pulling it back.\r\nSlice the plantain into medium size lengthwise slices and set aside.\r\nCoat a large frying pan with cooking oil spray. Spray the tops of the plantains with a generous layer of oil spray and sprinkle with salt, freshly ground pepper.\r\nLet the plantains fry on medium heat, shaking the frying pan to redistribute them every few minutes.\r\nAs the plantains brown, continue to add more cooking oil spray, salt and pepper (if needed) until they have reached the desired color and texture.\r\nRemove and serve with kale",
        'ingredients': 'Kale | Bacon | Garlic | Onion | Paprika | Thyme | Tomato | Red Pepper | Banana | Vegetable Oil', 
        'measurements': '1  bunch | 2 strips | 3 cloves Chopped | 1 medium | 1/2 tsp | 1 Sprig | 1 | 1 | 4 | Splash',
        'category': 'Miscellaneous',
        'area': 'Jamaican',
        'original': 'https://www.africanbites.com/callaloo-jamaican-style/',
        },
    {
        'user_id':2,
        'recipe_id': 52807,
        'title': 'Baingan Bharta',
        'instructions': "Rinse the baingan (eggplant or aubergine) in water. Pat dry with a kitchen napkin. Apply some oil all over and\r\nkeep it for roasting on an open flame. You can also grill the baingan or roast in the oven. But then you won't get\r\nthe smoky flavor of the baingan. Keep the eggplant turning after a 2 to 3 minutes on the flame, so that its evenly\r\ncooked. You could also embed some garlic cloves in the baingan and then roast it.\r\n2. Roast the aubergine till its completely cooked and tender. With a knife check the doneness. The knife should slid\r\neasily in aubergines without any resistance. Remove the baingan and immerse in a bowl of water till it cools\r\ndown.\r\n3. You can also do the dhungar technique of infusing charcoal smoky flavor in the baingan. This is an optional step.\r\nUse natural charcoal for this method. Heat a small piece of charcoal on flame till it becomes smoking hot and red.\r\n4. Make small cuts on the baingan with a knife. Place the red hot charcoal in the same plate where the roasted\r\naubergine is kept. Add a few drops of oil on the charcoal. The charcoal would begin to smoke.\r\n5. As soon as smoke begins to release from the charcoal, cover the entire plate tightly with a large bowl. Allow the\r\ncharcoal smoke to get infused for 1 to 2 minutes. The more you do, the more smoky the baingan bharta will\r\nbecome. I just keep for a minute. Alternatively, you can also do this dhungar method once the baingan bharta is\r\ncooked, just like the way we do for Dal Tadka.\r\n6. Peel the skin from the roasted and smoked eggplant.\r\n7. Chop the cooked eggplant finely or you can even mash it.\r\n8. In a kadai or pan, heat oil. Then add finely chopped onions and garlic.\r\n9. Saute the onions till translucent. Don't brown them.\r\n10. Add chopped green chilies and saute for a minute.\r\n11. Add the chopped tomatoes and mix it well.\r\n12. Bhuno (saute) the tomatoes till the oil starts separating from the mixture.\r\n13. Now add the red chili powder. Stir and mix well.\r\n14. Add the chopped cooked baingan.\r\n15. Stir and mix the chopped baingan very well with the onion\xadtomato masala mixture.\r\n16. Season with salt. Stir and saute for some more 4 to 5 minutes more.\r\n17. Finally stir in the coriander leaves with the baingan bharta or garnish it with them. Serve Baingan Bharta with\r\nphulkas, rotis or chapatis. It goes well even with bread, toasted or grilled bread and plain rice or jeera rice.",
        'ingredients': 'Aubergine | Onion | Tomatoes | Garlic | Green Chili | Red Chili Powder | Oil | Coriander Leaves | salt', 
        'measurements': '1 large | ½ cup  | 1 cup | 6 cloves | 1 | ¼ teaspoon | 1.5 tablespoon | 1 tablespoon chopped | as required',
        'category': 'Vegetarian',
        'area': 'Indian',
        'original': 'http://www.vegrecipesofindia.com/baingan-bharta-recipe-punjabi-baingan-bharta-recipe/',
        },
    {
        'user_id':2,
        'recipe_id': 52952,
        'title': 'Beef Lo Mein',
        'instructions': "STEP 1 - MARINATING THE BEEF\r\nIn a bowl, add the beef, salt, 1 pinch white pepper, 1 Teaspoon sesame seed oil, 1/2 egg, corn starch,1 Tablespoon of oil and mix together.\r\nSTEP 2 - BOILING THE THE NOODLES\r\nIn a 6 qt pot add your noodles to boiling water until the noodles are submerged and boil on high heat for 10 seconds. After your noodles is done boiling strain and cool with cold water.\r\nSTEP 3 - STIR FRY\r\nAdd 2 Tablespoons of oil, beef and cook on high heat untill beef is medium cooked.\r\nSet the cooked beef aside\r\nIn a wok add 2 Tablespoon of oil, onions, minced garlic, minced ginger, bean sprouts, mushrooms, peapods and 1.5 cups of water or until the vegetables are submerged in water.\r\nAdd the noodles to wok\r\nTo make the sauce, add oyster sauce, 1 pinch white pepper, 1 teaspoon sesame seed oil, sugar, and 1 Teaspoon of soy sauce.\r\nNext add the beef to wok and stir-fry",
        'ingredients': 'Beef | Salt | Pepper | Sesame Seed Oil | Egg | Starch | Oil | Noodles | Onion | Minced Garlic | Ginger | Bean Sprouts | Mushrooms | Water | Oyster Sauce | Sugar | Soy Sauc', 
        'measurements': '1/2 lb | pinch | pinch | 2 tsp | 1/2  | 3 tbs | 5 tbs | 1/4 lb | 1/2 cup  | 1 tsp  | 1 tsp  | 1 cup  | 1 cup  | 1 cup  | 1 tbs | 1 tsp  | 1 tsp ',
        'category': 'Beef',
        'area': 'Chinese',
        'original': 'https://sueandgambo.com/pages/beef-lo-mein',
        },

]

for recipe in recipes:
    new = Favorite(user_id=recipe['user_id'], 
                    recipe_id=recipe['recipe_id'], 
                    title=recipe['title'],
                    ingredients=recipe['ingredients'],
                    measurements=recipe['measurements'],
                    instructions=recipe['instructions'],
                    category=recipe['category'],
                    area=recipe['area'],
                    original=recipe['original'])
    db.session.add(new)
    db.session.commit()
=======
        'id': 151,
        'username': 'test',
        'password': 'test',
        'email': 'test@test.com',
        'bio': 'I am a test user. I love to test things. Testing is fun',
        'img': 'https://thumbs.dreamstime.com/b/student-trying-to-cheat-test-male-class-34669006.jpg'
    },
    {
        'id': 152,
        'username': 'HankHill',
        'password': 'propane',
        'email': 'hank@strickland.com',
        'bio': 'I sell propane and propane accessories. I love mowing lawns and using WD-40',
        'img': 'https://play-lh.googleusercontent.com/iQaRYz9z_TsVyyzjtpaJ73ms9RPiT4e_UB5DOndoPmxIQ10LU5jGubR1X7hVI1U-_wM'
    },
    {
        'id': 153,
        'username': 'PeggyHill',
        'password': 'boggle',
        'email': 'peggy@boggle.com',
        'bio': 'I am a substitute spanish teacher at Tom Landry Middle School. I love boggle and playing softball',
        'img': 'https://static.tvtropes.org/pmwiki/pub/images/char_6989_4107.jpg'
    },
    {
        'id': 154,
        'username': 'BobbyHill',
        'password': 'comedy',
        'email': 'bobby@thatsmypurse.com',
        'bio': 'I am an amateur comedian and I like to hang out with my friends Connie and Joseph',
        'img': 'https://imgix.ranker.com/list_img_v2/14514/2754514/original/bobby-hill-feminist-hero'
    },
    {
        'id':155,
        'username': 'Boomhauer',
        'password': 'dang',
        'email': 'dangole@talkinbout.com',
        'bio': "Dang ole, tawmbout. Dang ole...biography",
        'img': 'https://upload.wikimedia.org/wikipedia/en/b/be/Jeff_Boomhauer.png'
    },
]

def set_users():

    for user in users:
        new = User.register_user(
                    id=user['id'],
                    username=user['username'],
                    pwd=user['password'],
                    email=user['email'],
                    bio=user['bio'],
                    img=user['img'])
        db.session.add(new)
        db.session.commit()




def get_meal_data():
    res = requests.get(f'https://www.themealdb.com/api/json/v2/{API_KEY}/randomselection.php')
    res_json = res.json()

    res_dict = res_json['meals']


    # breakpoint()
    return res_dict




def set_favs():
    for i in range(1, 156):
        example = get_meal_data()
        for recipe in example:
            new = Favorite(user_id=i, 
                        recipe_id=recipe['idMeal'], 
                        title=recipe['strMeal'],
                        ingredients='example of ingredients',
                        measurements='example of measurements',
                        instructions=recipe['strInstructions'],
                        category=recipe['strCategory'],
                        area=recipe['strArea'],
                        original='example',
                        )
            db.session.add(new)
            db.session.commit()

matches = [
    (151, 152),
    (151, 45),
    (152, 154),
    (152, 67),
    (152, 33),
    (153, 152),
    (153, 56),
    (154, 153),
    (154, 1),
    (155, 154),
    (155, 30)
]

def set_matches():
    for user, match in matches:
        new = Match(user_id=user, match_id=match)
        db.session.add(new)
        db.session.commit()

def clear_matches():
    for user, match in matches:
        new = Match(user_id='', match_id='')
        db.session.add(new)
        db.session.commit()



# drop_create()

# set_users()
# set_favs()                                                    
# set_matches()
# clear_matches()
>>>>>>> messages
