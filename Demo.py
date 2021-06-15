from DB import add_new_user, add_new_donation, add_new_request, RequestStatus
from server.Donation_Creation import list_to_string
from server.Donation_Preview import handle_new_suggested_tag


def build_demo_donors():

    # Donors - Restaurants
    add_new_user(email="agadir@gmail.com", name="Agadir", location="Moshe Beker Street 10, Rishon LeZion",
                 password="12345678", picture="static/profile_pictures/agadir.JPG", status_text="Best Meat!")
    add_new_user(email="delapaix@gmail.com", name="De La Paix", location="Modiin-Maccabim-Reut",
                 password="12345678", picture="static/profile_pictures/delapaix.jpeg", status_text="Tasty Cakes")
    add_new_user(email="giraffe@gmail.com", name="Giraffe", location="Haifa",
                 password="12345678", picture="static/profile_pictures/giraffe.png",
                 status_text="You'll love our sushi!")
    add_new_user(email="golda@gmail.com", name="Golda", location="Herzl Beach, Netanya",
                 password="12345678", picture="static/profile_pictures/golda.png", status_text="Best ice cream!")
    add_new_user(email="goomba@gmail.com", name="Goomba", location="St. George Greek Orthodox Church, Lod",
                 password="12345678", picture="static/profile_pictures/goomba.jpg", status_text="Pasta is love")
    add_new_user(email="halil@gmail.com", name="Halil", location="חומוס חליל",
                 password="12345678", picture="static/profile_pictures/halil.jpg", status_text="Hummus is Halil")
    add_new_user(email="landwer@gmail.com", name="Landwer", location="Bat Yam Mall",
                 password="12345678", picture="static/profile_pictures/landver.png", status_text="Have some coffee!")
    add_new_user(email="lehamim@gmail.com", name="Lehamim", location="קניון שאול המלך",
                 password="12345678", picture="static/profile_pictures/lehamim.png",
                 status_text="Bread, cakes and more!")
    add_new_user(email="mcdonalds@gmail.com", name="Mcdonalds", location="קניון רוטשילד",
                 password="12345678", picture="static/profile_pictures/mcdonald's.png", status_text="I'm lovin it")
    add_new_user(email="miznon@gmail.com", name="Miznon", location="Herzliya",
                 password="12345678", picture="static/profile_pictures/miznon.jpg", status_text="Pita is life")
    add_new_user(email="monica@gmail.com", name="Monica", location="Eli Horowitz 12, Rehovot, Central District",
                 password="12345678", picture="static/profile_pictures/monica.jpg", status_text="I know!")
    add_new_user(email="moses@gmail.com", name="Moses", location="Mall Hayam, HaPalmach 1, Eilat",
                 password="12345678", picture="static/profile_pictures/moses.jpg", status_text="Try our burgers!")
    add_new_user(email="neeman@gmail.com", name="Neeman Bakery", location="נס ציונה",
                 password="12345678", picture="static/profile_pictures/neeman.jpg",
                 status_text="Pastries, sandwiches and more!")
    add_new_user(email="otello@gmail.com", name="Otello Gelato", location="Givatayim",
                 password="12345678", picture="static/profile_pictures/otello.jpg", status_text="Great Gelato!")
    add_new_user(email="soho@gmail.com", name="Soho Sushi",
                 location="Soho Sushi & Bar, 15 Moshe Beker St., Rishon LeZion",
                 password="12345678", picture="static/profile_pictures/soho.png", status_text="The best Sushi!")
    add_new_user(email="zozobra@gmail.com", name="Zozobra",
                 location="Ben Gurion International Airport",
                 password="12345678", picture="static/profile_pictures/zozobra.jpg", status_text="Open 8-19")
    add_new_user(email="aroma@gmail.com", name="Aroma",
                 location="Petah Tikva",
                 password="12345678", picture="static/profile_pictures/ארומה.png", status_text="Open 7-18")
    add_new_user(email="victory@gmail.com", name="Victory",
                 location="טיילת בת-ים, Ben Gurion Rd., בת ים, מחוז תל אביב, ישראל",
                 password="12345678", picture="static/profile_pictures/victory.jpg", status_text="Ice cream, pancakes and crepes")
    add_new_user(email="tzachi@gmail.com", name="Tzhib",
                 location="צחי בשרים",
                 password="12345678", picture="static/profile_pictures/tzachi.png", status_text="The best meat in Bat Yam")
    add_new_user(email="segev@gmail.com", name="Segev",
                 location="שגב, 16 Shenkar St., הרצליה, מחוז תל אביב, ישראל",
                 password="12345678", picture="static/profile_pictures/segev_l.jpg", status_text="All kinds of food in one Place")
    add_new_user(email="adhaezem@gmail.com", name="Ad Hazem",
                 location="מרכז שוסטר",
                 password="12345678", picture="static/profile_pictures/adhaezem_l.png", status_text="Ad Hazem Express")
    # Donors - private persons
    add_new_user(email="savata@gmail.com", name="Rachel Maimon",
                 location="קניון קרית אונו, 37 Shlomo Hamelech St., קריית אונו, מחוז תל אביב, ישראל",
                 password="12345678", picture="static/profile_pictures/grandmother.jpg", status_text="You're Welcome!")
    add_new_user(email="china@gmail.com", name="Lee",
                 location="קרית ההגנה, רחובות, מחוז המרכז, ישראל",
                 password="12345678", picture="static/profile_pictures/china_l.jpg", status_text="有胃口")
    add_new_user(email="mikiepl@gmail.com", name="Miki",
                 location="אשדוד רובע י״ב, אשדוד, מחוז הדרום, ישראל",
                 password="12345678", picture="static/profile_pictures/italian_p.jpg", status_text="")
    add_new_user(email="NotABotForSure@gmail.com", name="Not A Bot", location="Tel Aviv",
                 password="12345678", picture="static/profile_pictures/NotABot.jpg", status_text="I'm not a Bot!")
    # Admin
    add_new_user(email="taumanyforone@gmail.com", name="Admin", location="Israel",
                 password="12345678", picture="static/profile_pictures/admin.jpg", status_text="I am here for you")

def build_demo_donations():
    # donations
    #1
    add_new_donation(user_email="agadir@gmail.com", recipients_amount=50, is_predictable=False,
                     description="", picture=list_to_string(
            ["../static/donations_pictures/4_burgers.jpg", "../static/profile_pictures/agadir.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=False, is_vegan=False, is_meat=True, is_dairy=False, is_gluten_free=False)
    #2
    add_new_donation(user_email="delapaix@gmail.com", recipients_amount=32, is_predictable=False,
                     description="YUMMY!", picture=list_to_string(
            ["../static/donations_pictures/cakes.jpeg", "../static/donations_pictures/cakes2.jpg","../static/profile_pictures/delapaix.jpeg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=True, is_gluten_free=False)
    #3
    add_new_donation(user_email="giraffe@gmail.com", recipients_amount=12, is_predictable=False,
                     description="sushi!", picture=list_to_string(
            ["../static/donations_pictures/sushi1.jpg", "../static/profile_pictures/giraffe.png"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=False, is_vegan=True, is_meat=False, is_dairy=False, is_gluten_free=True)
    #4
    add_new_donation(user_email="golda@gmail.com", recipients_amount=15, is_predictable=False,
                     description="", picture=list_to_string(
            ["../static/donations_pictures/icecream1.jpg","../static/donations_pictures/icecream2.jpg", "../static/profile_pictures/golda.png"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=True, is_gluten_free=True)
    #5
    add_new_donation(user_email="goomba@gmail.com", recipients_amount=43, is_predictable=False,
                     description="", picture=list_to_string(
            ["../static/donations_pictures/3_pizza.jpg", "../static/profile_pictures/goomba.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=True, is_gluten_free=False)
    #6
    add_new_donation(user_email="halil@gmail.com", recipients_amount=8, is_predictable=False,
                     description="", picture=list_to_string(
            ["../static/donations_pictures/hummus1.jpg", "../static/donations_pictures/hummus2.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=False, is_vegan=True, is_meat=False, is_dairy=False, is_gluten_free=False)
    #7
    add_new_donation(user_email="landwer@gmail.com", recipients_amount=13, is_predictable=False,
                     description="sandwiches", picture=list_to_string(
            ["../static/donations_pictures/sandwiches2.jpg", "../static/profile_pictures/landver.png"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=True, is_gluten_free=False)
    #8
    add_new_donation(user_email="lehamim@gmail.com", recipients_amount=None, is_predictable=True,
                     description="some sandwiches", picture=list_to_string(
            ["../static/donations_pictures/sandwiches3.jpg", "../static/profile_pictures/lehamim.png"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=True, is_dairy=False, is_gluten_free=False)
    #9
    add_new_donation(user_email="victory@gmail.com", recipients_amount=17, is_predictable=False,
                     description="Pancakes, Ice-Cream", picture=list_to_string(
            ["../static/donations_pictures/icecream_v.jpg", "../static/donations_pictures/pancake_v.jpg","../static/profile_pictures/victory.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=False, is_vegan=False, is_meat=False, is_dairy=True, is_gluten_free=False)
    #10
    add_new_donation(user_email="tzachi@gmail.com", recipients_amount=None, is_predictable=True,
                     description="Shawarma, kebab", picture=list_to_string(
            ["../static/donations_pictures/tzahi_k.jpg", "../static/donations_pictures/tzahi_s.jpg","../static/profile_pictures/tzachi.png"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=True, is_dairy=False, is_gluten_free=False)
    #11
    add_new_donation(user_email="segev@gmail.com", recipients_amount=12, is_predictable=False,
                     description="pizza, hamburger and more", picture=list_to_string(
            [ "../static/donations_pictures/segev_f.jpg","../static/profile_pictures/segev_l.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=False, is_gluten_free=False)
    #12
    add_new_donation(user_email="adhaezem@gmail.com", recipients_amount=43, is_predictable=False,
                     description="Hamburger, Chips", picture=list_to_string(
            [ "../static/donations_pictures/adhaezem_f.jpg","../static/profile_pictures/adhaezem_l.png"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=False, is_gluten_free=False)


    #Person Donations
    #13
    add_new_donation(user_email="savata@gmail.com", recipients_amount=None, is_predictable=True,
                     description="", picture=list_to_string(
            [ "../static/donations_pictures/home-food.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=True, is_vegan=False, is_meat=False, is_dairy=False, is_gluten_free=False)
    #14
    add_new_donation(user_email="china@gmail.com", recipients_amount=None, is_predictable=True,
                     description="", picture=list_to_string(
            [ "../static/donations_pictures/chniese_f.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=False, is_vegan=False, is_meat=False, is_dairy=False, is_gluten_free=True)
    #15
    add_new_donation(user_email="mikiepl@gmail.com", recipients_amount=None, is_predictable=True,
                     description="", picture=list_to_string(
            [ "../static/donations_pictures/italian_f.jpg"]), start_time=None,
                     end_time=None, is_open=True, is_in_process=False,
                     is_kosher=False, is_vegan=True, is_meat=False, is_dairy=False, is_gluten_free=False)


# donation = add_new_donation(user_email="email1", description='test', is_gluten_free=True, recipients_amount=4)
    # add_new_user(email="test@gmail.com", name="Test", location="Moshe Beker Street 10, Rishon LeZion",password="12345678",picture="static/profile_pictures/joe.JPG")
    # add_new_user(email=Email, name=username, location=location, password=Password, picture=img_path)
def build_demo_tags():
        handle_new_suggested_tag(donation_id=1,new_tag="chips",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="chips",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="chips",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="chips",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="chips",user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="burger",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="burger",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="burger",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="burger",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="burger",user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="cheese",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="cheese",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="cheese",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="cheese",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=1,new_tag="cheese",user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=2,new_tag="cake",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="cake",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="cake",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="cake",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="cake",user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="chocolate",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="chocolate",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="chocolate",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="chocolate",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="chocolate",user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="meringue",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="meringue",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="meringue",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="meringue",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=2,new_tag="meringue",user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=3, new_tag="sushi", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="sushi", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="sushi", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="sushi", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="sushi", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="avocado", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="avocado", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="avocado", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="avocado", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=3, new_tag="avocado", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=4, new_tag="ice cream", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="ice cream", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="ice cream", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="ice cream", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="ice cream", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="frozen", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="frozen", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="frozen", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="frozen", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="frozen", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="yogurt", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="yogurt", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="yogurt", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="yogurt", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=4, new_tag="yogurt", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=5, new_tag="pizza", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="pizza", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="pizza", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="pizza", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="pizza", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="italian", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="italian", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="italian", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="italian", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=5, new_tag="italian", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=6, new_tag="hummus", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="hummus", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="hummus", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="hummus", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="hummus", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="falafel", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="falafel", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="falafel", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="falafel", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=6, new_tag="falafel", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=7, new_tag="omelet", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="omelet", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="omelet", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="omelet", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="omelet", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="breakfast", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="breakfast", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="breakfast", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="breakfast", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=7, new_tag="breakfast", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=8, new_tag="tuna", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="tuna", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="tuna", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="tuna", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="tuna", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="sabih", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="sabih", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="sabih", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="sabih", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=8, new_tag="sabih", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=9, new_tag="ice cream", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="ice cream", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="ice cream", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="ice cream", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="ice cream", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="frozen", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="frozen", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="frozen", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="frozen", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="frozen", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="yogurt", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="yogurt", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="yogurt", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="yogurt", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="yogurt", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="pancake", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="pancake", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="pancake", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="pancake", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=9, new_tag="pancake", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=10, new_tag="shawarma", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="shawarma", user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="shawarma", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="shawarma", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="shawarma", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="shawarma", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="chicken", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="chicken", user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="chicken", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="chicken", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="chicken", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=10, new_tag="chicken", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=11, new_tag="pizza", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="pizza", user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="pizza", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="pizza", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="pizza", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="pizza", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="italian", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="italian", user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="italian", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="italian", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="italian", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="italian", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="shakshuka", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="shakshuka", user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="shakshuka", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="shakshuka", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="shakshuka", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="shakshuka", user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="burger", user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="burger", user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="burger", user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="burger", user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="burger", user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=11, new_tag="burger", user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=12,new_tag="burger",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=12,new_tag="burger",user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=12,new_tag="burger",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=12,new_tag="burger",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=12,new_tag="burger",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=12,new_tag="burger",user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=13,new_tag="soup",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="soup",user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="soup",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="soup",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="soup",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="soup",user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="couscous",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="couscous",user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="couscous",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="couscous",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="couscous",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=13,new_tag="couscous",user_email="tzachi@gmail.com")

        handle_new_suggested_tag(donation_id=14,new_tag="noodles",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="noodles",user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="noodles",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="noodles",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="noodles",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="noodles",user_email="tzachi@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="eggroll",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="eggroll",user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="eggroll",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="eggroll",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="eggroll",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=14,new_tag="eggroll",user_email="tzachi@gmail.com")


        handle_new_suggested_tag(donation_id=15,new_tag="italian",user_email="savata@gmail.com")
        handle_new_suggested_tag(donation_id=15,new_tag="italian",user_email="mikiepl@gmail.com")
        handle_new_suggested_tag(donation_id=15,new_tag="italian",user_email="china@gmail.com")
        handle_new_suggested_tag(donation_id=15,new_tag="italian",user_email="golda@gmail.com")
        handle_new_suggested_tag(donation_id=15,new_tag="italian",user_email="segev@gmail.com")
        handle_new_suggested_tag(donation_id=15,new_tag="italian",user_email="tzachi@gmail.com")

def build_demo_requests():
    # delivery
    add_new_request(recipient="monica@gmail.com", donation="1", recipients_amount=int(3),
                    donor="agadir@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="1", recipients_amount=int(1),
                    donor="agadir@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="1", recipients_amount=int(2),
                    donor="agadir@gmail.com", status=RequestStatus.By_volunteer.value)

    add_new_request(recipient="monica@gmail.com", donation="2", recipients_amount=int(3),
                    donor="delapaix@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="2", recipients_amount=int(1),
                    donor="delapaix@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="2", recipients_amount=int(2),
                    donor="delapaix@gmail.com", status=RequestStatus.By_volunteer.value)

    add_new_request(recipient="monica@gmail.com", donation="3", recipients_amount=int(3),
                    donor="giraffe@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="3", recipients_amount=int(1),
                    donor="giraffe@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="3", recipients_amount=int(2),
                    donor="giraffe@gmail.com", status=RequestStatus.By_volunteer.value)


    add_new_request(recipient="monica@gmail.com", donation="4", recipients_amount=int(3),
                    donor="golda@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="4", recipients_amount=int(1),
                    donor="golda@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="4", recipients_amount=int(2),
                    donor="golda@gmail.com", status=RequestStatus.By_volunteer.value)

    add_new_request(recipient="monica@gmail.com", donation="5", recipients_amount=int(3),
                    donor="goomba@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="5", recipients_amount=int(1),
                    donor="goomba@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="5", recipients_amount=int(2),
                    donor="goomba@gmail.com", status=RequestStatus.By_volunteer.value)

    add_new_request(recipient="monica@gmail.com", donation="6", recipients_amount=int(3),
                    donor="halil@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="6", recipients_amount=int(1),
                    donor="halil@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="6", recipients_amount=int(2),
                    donor="halil@gmail.com", status=RequestStatus.By_volunteer.value)

    add_new_request(recipient="monica@gmail.com", donation="9", recipients_amount=int(3),
                    donor="victory@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="9", recipients_amount=int(1),
                    donor="victory@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="9", recipients_amount=int(2),
                    donor="victory@gmail.com", status=RequestStatus.By_volunteer.value)

    #Take Away :
    add_new_request(recipient="mikiepl@gmail.com", donation="12", recipients_amount=int(1),
                    donor="adhaezem@gmail.com")
    add_new_request(recipient="soho@gmail.com", donation="12", recipients_amount=int(1),
                    donor="adhaezem@gmail.com")
    add_new_request(recipient="soho@gmail.com", donation="10", recipients_amount=int(1),
                    donor="tzachi@gmail.com")
    add_new_request(recipient="soho@gmail.com", donation="11", recipients_amount=int(1),
                    donor="segev@gmail.com")
    add_new_request(recipient="soho@gmail.com", donation="1", recipients_amount=int(2),
                    donor="agadir@gmail.com")

def build_demo_requests_for_movie():
    # delivery
    add_new_request(recipient="monica@gmail.com", donation="11", recipients_amount=int(3),
                    donor="segev@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="11", recipients_amount=int(1),
                    donor="segev@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="11", recipients_amount=int(2),
                    donor="segev@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="mikiepl@gmail.com", donation="11", recipients_amount=int(1),
                    donor="segev@gmail.com")

    add_new_request(recipient="monica@gmail.com", donation="2", recipients_amount=int(3),
                    donor="delapaix@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="2", recipients_amount=int(1),
                    donor="delapaix@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="2", recipients_amount=int(2),
                    donor="delapaix@gmail.com", status=RequestStatus.By_volunteer.value)



    add_new_request(recipient="monica@gmail.com", donation="5", recipients_amount=int(3),
                    donor="goomba@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="5", recipients_amount=int(1),
                    donor="goomba@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="5", recipients_amount=int(2),
                    donor="goomba@gmail.com", status=RequestStatus.By_volunteer.value)

    add_new_request(recipient="monica@gmail.com", donation="13", recipients_amount=int(3),
                    donor="landwer@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="otello@gmail.com", donation="13", recipients_amount=int(1),
                    donor="landwer@gmail.com", status=RequestStatus.By_volunteer.value)
    add_new_request(recipient="neeman@gmail.com", donation="13", recipients_amount=int(2),
                    donor="landwer@gmail.com", status=RequestStatus.By_volunteer.value)











