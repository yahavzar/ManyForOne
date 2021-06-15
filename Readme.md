# Many For One
A website for food donations. 
<br> The purpose of the website is to help those in need of food and to reduce food waste.
<br>The website creates easy connections between food donors, the people who wish to receive it and volunteers 
that help with transferring the food.
<br> The matches are based on food types and locations. 


## DB & Tables
Main libraries sqlite & flask_sqlalchemy.

Each file Includes the table class and related function to retrieve, store & perform logic on the table fields.
<br> User - [DB/users.py](DB/users.py)
<br> Donation - [DB/donations.py](DB/donations.py)
<br> Tag & Tags- [DB/tagging.py](DB/tagging.py)
<br> Request - [DB/requests.py](DB/requests.py)
<br> Frequency - [DB/frequency.py](DB/frequency.py)
<br> Suspicious - [DB/Suspicious.py](DB/Suspicious.py)
<br> Blacklist - [DB/blacklist.py](DB/blacklist.py)
<br><br> SQL Relationships:
One-to-Many: User -> Donations ; Many-to-Many: Donations <-> Tags


# Main Features & Algorithms

### Matching Recipient\Volunteer-Donor: Based On Location 
* Users input their address location in register
* Upon login the map updates to show a range from their location to closest open donations
* The pins of the closest donations inside the radius are colored differently
* The User can input a different address from the one in the profile and a different distance for the radius to update the map accordingly.

>path : [server/home_page.py](server/home_page.py) [server/Register.py](server/Register.py)

### Reliable Tagging
Purpose: Keep reliable tags for donations, avoid false/incorrect tags.
* Each user has a “Tagging Score” which saves how many “good tags” he added to the system. 
* Tags by a user with a high “Tagging Score” can be more trusted.
  * A new donation with empty tags suggestions list `[ { tag : sum, user_ids } ]` 
  * User 1 enters an new tag
  * The system offers him similar existing tags (*described later) to choose from
  * User 1 selects a new/existing tag
  * The tag is inserted to the suggestions list : `{tag: sum=User 1’s “Tagging score”, user_ids=[1]}`
  * When user 2 inserts the same tag the tag’s sum is updated `{tag: sum + user 2’s “Tagging score”, user_ids=[1,2]}`
  * After an insert, if sum >= reliable bar (5):
    * The tag is removed from the suggestions list and added as a label to the donation to search by
    * Every user in user_ids gets a `+1` for his Tagging score 
   
>path: [server/Donation_Preview.py](server/Donation_Preview.py)

### Similar Tags
Purpose: Keeping the tags general to optimize the search and avoiding typos and redundancy.
* Compare new suggested tag to the existing tags:
  * Check if an existing tag is a substring of the new tag
  * Radcliff/Obershelp algorithm - difflib.SequenceMatcher 
  * Levenshtein algorithm - fuzzywuzzy
* take 3 most common suggestions
* Show the most similar results for the user to choose from

>path: [server/Donation_Preview.py](server/Donation_Preview.py)

### Recommendations System
- Collaborative filtering - based on users' activity: “Users who took donations from this place, also took donations from these places… ”
- The number of times a user took a donation from a specific donor can indicate how much the place is a good match for him.
- Recommend a user a new donor place based on the user’s previous donations.
- Based on KNN algorithm. Each Donor has a “frequency vector”, 
the counters of donations taken from this donor by the different users.
- The model will take a donor and return the donors with the closest “frequency vector”.
- If the recommended donors has open donations they will appear on the map.

> path: [Recommendations/collaborative_filtering.py](Recommendations/collaborative_filtering.py) [DB/donations.py](DB/donations.py)

### Taggers View
Purpose: 
- Help the users find the donations that are missing tags.
- Find the minimum number of tags in the open donations
    * Change the pins’ color of the donations with the minimum number of tags 

>path: [server/home_page.py](server/home_page.py) [DB/donations.py](DB/donations.py) [server/Donation_Preview.py](server/Donation_Preview.py)

### Volunteer View
Purpose: 
- Show the donations that have open requests on the map for a volunteer to review
- Each request is shown with the distance between the donor and the recipient

>path: [server/home_page.py](server/home_page.py) [DB/donations.py](DB/donations.py) [server/Donation_Preview.py](server/Donation_Preview.py)

### Quantity Prediction
Purpose: 
- Predict quantity of a donation in case the donor didn’t specify it
- Don’t allow user to divert the quantity too much - one vote & median
  * A new donation with no quantity is added and defaulted to 1
  * The donation is marked as open to predictions with predictions list [] and predictors []
  * A user can enter his prediction if he is not already in the predictors list.
  * After every prediction the value is updated to the median of the predictions (less sensitive to extreme scores).

>path: [server/Donation_Preview.py](server/Donation_Preview.py)

### Blacklisting
Purpose: remove unreliable users. 
Unreliable donors and volunteers:
* The recipient reports in his log if the donation is received or not and gives 
  a rating score for the donor and/or the volunteer. 
* If a donation is reported as missing the score is decreased. 
* After each score update, check if the score is below the “reliability bar”
* Unreliable users are marked as suspicious 

>path: [server/log.py](server/log.py) [DB/users.py](DB/users.py)

### Moving to Blacklist
* Suspicious users are informed by mail and are given the chance to to appeal if they believe there's a mistake.
* Admin can review the suspicious users in his admin page and decide if to move them to the blacklist.
* Once blacklisted the user is removed from the website.
* If the user tries to register again with the same email he will see a "blacklisted" notification and will not be able 
  to do so.
>path: [DB/blacklist.py](DB/blacklist.py) [DB/Suspicious.py](DB/Suspicious.py) [server/AdminView.py](server/AdminView.py)

### Unreliable recipients (potential Bots):
* In order to prevent bots from taking new donations that were just being added, every 24 hours, 
  we scans all users and looks for users that requested a donation in a very short period of time since it was added.
* If it detects a user took an unusual amount of requests for 3 days (an unusual amount is more than the average of requests per that day)
  the user is added to a suspicious list
* The admin can then go to "Admin view" in his profile tab and move the user to the blacklist

>path: [DB/blacklist.py](DB/blacklist.py) [DB/Suspicious.py](DB/Suspicious.py) [server/AdminView.py](server/AdminView.py) [app.py](app.py)

### Top Contributors
Purpose: motivating users to take part in the donation process.
  
* each user will have a “contribution rank” calculated daily by the formula that takes into account all of the helping methods.
* contribution score = number_of_past_donations * 2 + number_of_past_deliveries  * 2 + tagging_score +   rating_score_as_donor + rating_score_as_volunteer
* The top 5 users with the highest contribution score will be presented on the main page for a day along with their details.

>path: [DB/users.py](DB/users.py) [app.py](app.py)

### Notifications
Purpose: keeping our users up to date and reminding them of their activity and donations.

The users recieves an email notification in the following cases:
* Registration
* Donation status update
* One of the top 5 contributors
* Suspicious behavior 
>path [server/utils.py](server/utils.py)


# User Guide
( Received by mail after registration )

Welcome!

We greatly appreciate your registration!
In this site you can find food donations, add donations of your own or volunteer to deliver donations to users who can't pick them up themselves.

Don't have donations? you can still help! Tag the donations and suggest quantities where needed to help users find the donations easily.
Any contribution to the website is appreciated. Each day the top 5 contributors are published in the main page!
You can find a guide below, please contact us if you have any questions!

###  Finding A Donation 
The map in the home page will show you the currently open donation.
Donations in a radius of 5000 meters from your location will appear in red.

Are you in a different location? enter your current address into the 'Update location' filed.
Interested in other radius? enter the desire distance in the meters into the 'Radius search' field.

You can also filter the map with the buttons above it. In addition, you can filter it by choosing from the list of tags (hold Ctrl to choose more than one).
Click 'Update Map' to see the donations that match your filters.

If you took a donation before, try the 'Show Recommendations' as well to see donations that you might like based on the donations you took before.

Found a donation you like? Great!
In the donation window choose 'Take it'.
If you intend to take the donation yourself, pick 'Take Away' and enter the quantity you are going to collect. (You might need to suggest a quantity if there isn't one already).
If you can't take the donation yourself, pick 'Delivery' and a volunteer might pick it up for you.

Got the donation? please confirm & rate in the log page through your profile. If the donation is missing, please report it in the log page to help us keep a reliable process.

### Adding A Donation 
Do you have food to donate? That's great!
Please click on the 'Add Donation' button above the map.
You can add photos, description and tags to help users find your donation.
Thank you for your contribution!

### Volunteering
Can you deliver a donation from the donor? that's a great help!
Pick 'Volunteer view' above the map and set the distance filters if needed, then click 'update map'.
In the donation window, you can see all the requests to this donation.
If you find a request you can take, choose 'Take delivery' under the 'Take it' column.
Thank you for your contribution!

### Tagging 
Can you add Tags and quantities to donations? that's a great help!
Pick 'Tagger view' above the map, then click 'update map'.
In the donation window you can see photos or description. If you have a new label to add that can describe the food, click 'Add Lable'.
Before adding your label, you can check if there are already similar tags you can add.
Existing tags are always preferable, but don't hesitate to add a new one where needed!

You added a label but don't see it in the donation window yet? that's ok!
After a few more users will add this label too it will show up.
The more good tags you add, the more weight your future tags will have! Like a rank in a game, we trust our pro-taggers :)

You went through all the donations under tagger view? you're awesome! 
Feel free to switch back to the default view and tag the other ones as well, the more tags the merrier!

One more way to help is by predicting the numbers of users that can enjoy the donation.
If you see the 'suggest quantity' button that means we need your help to predict the number of recipients.
Can you suggest a quantity based on the photos? please click the button and enter your suggestion.
Thank you for your contribution!


## Install


Deployment instructions:

1) Login to nova

2)  Go to delta-tomcat-vm
    ```sh 
    ssh delta-tomcat-vm
    ```

3) Go to your directory with 
    ```sh 
   cd specific/scratch/<userName>/django 
    ```
4) Download ManyForOne
    ```sh 
    git clone https://github.com/yahavzar/ManyForOne.git (or move ManyForOne from nova with
        $scp -r ManyForOne delta-tomcat-vm:/specific/scratch/<userName>) 
     cd ManyForOne
    ```    
5) Make the virtual environment
    ```sh 
    wget repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
    bash Anaconda3-2020.11-Linux-x86_64.sh
   Press 'Enter'
    yes
    specific/scratch/<userName>/django/ManyForOne
    yes
    ```    
6) Activate the virtual environment
    ```sh 
    bash
    export LD_LIBRARY_PATH=/usr/local/lib/openssl-1.1.1a/lib:$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=/usr/local/lib/openssl-1.1.1a/lib
    source activate3 specific/scratch/<userName>/django/ManyForOne
    ```    
7) Install requirements
    ```sh 
     pip install flask_mail
     pip install mapbox
     pip install flask_sqlalchemy
     pip install fuzzywuzzy
     pip install haversine
     pip install apscheduler
    ```    
8) Run app.py
    ```sh 
     python3 app.py
    ```    
## Support

* Adi Tzadkani adic10904@gmail.com 
* Or Harush orharush24@gmail.com
* Shirly Rabin shirlyrl@gmail.com  
* Yahav Zarfati yahavzar171@gmail.com 
