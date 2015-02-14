from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from twilio import twiml
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient
import os
from random import choice
from local_settings import *


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config['ACCOUNT_SID'] = ACCOUNT_SID
app.config['AUTH_TOKEN'] = AUTH_TOKEN
app.config['SONYA_APP_SID'] = SONYA_APP_SID
app.config['SONYA_CALLER_ID'] = SONYA_CALLER_ID


@app.route('/')
def index():
    reason = reasonSonyaIsAwesome()
    capability = TwilioCapability(app.config['ACCOUNT_SID'],
        app.config['AUTH_TOKEN'])
    capability.allow_client_outgoing(app.config['SONYA_APP_SID'])
    token = capability.generate()
    return render_template('index.html', token=token, reason=reason)


@app.route('/voice', methods=['POST'])
def voice():
    r = twiml.Response()
    r.say('Hello Danielle.  Here is a reason why you are awesome.')
    reason = reasonSonyaIsAwesome()
    reason.replace(':', '.')
    reason = "This one is from %s" % reason
    r.say(reason)
    with r.gather(action='/gather', numDigits='1') as g:
        g.say('Press 1 if you would like to hear another reason.  Press 2 or ' \
        'hangup if you are finished.')
    r.pause()
    r.redirect('/voice')
    return str(r)


@app.route('/gather', methods=['POST'])
def repeat():
    r = twiml.Response()
    if request.form['Digits'] == '1':
        reason = reasonSonyaIsAwesome()
        reason.replace(':', '.')
        reason = "This one is from %s" % reason
        r.say(reason)
    elif request.form['Digits'] == '2':
        r.say('Bye Danielle!')
        r.hangup()
    else:
        r.say('I did not understand your input.')
    with r.gather(action='/gather', numDigits='1') as g:
        g.say('Press 1 if you would like to hear another reason.  Press 2 or ' \
        'hangup if you are finished.')
    r.pause()
    r.redirect('/voice')
    return str(r)


@app.route('/sms', methods=['POST'])
def sms():
    r = twiml.Response()
    reason = reasonSonyaIsAwesome()
    if request.form['Body'].upper() == "HELP":
        r.sms("Welcome to the Reasons Danielle Is Awesome Hotline.  Text GIMME " \
                "to get one random reason Danielle is awesome.")
    else:
        r.sms(reason)
    return str(r)


def reasonSonyaIsAwesome():
    reasons = [
            'Tessa: You are the kindest, most considerate shit I know.',
            'Tessa: You don\'t always wear glasses, but when you do, they have real lenses.',
            'Tessa: You are the Shit.',
            'Tessa: WE ARE THE SHITS.',
            'Tessa: You are a business MASTER!',
            'Tessa: Because, SAME BRAIN.',
            'Tessa: Your ability to consume chicken wings is unparalleled.',
            'Tessa: o_O',
            'Tessa: lalalalalalallalalaalalala.',
            'Tessa: Because AGHHHHHHHHHIAWJFEOIJWAFOIEWA!',
            'Tessa: Because the NSA must be both concerned and impressed by our level of correspondence.',
            'Tessa: Because I\'m so lucky we get to walk through life alone together!',
            'Tessa: \"DUDE THIS GIRL MEANS BUSINESS. CUZ SHE\'S A BUSINESS WOMAN.\"',
            'Tessa: SLUUUUUUUUURRRRRP',
            'Tessa: Uhh, Danielle\'s ok, I guess.',
            'Tessa: Aaaahhhh! Youths!',
            'Tessa: Because unbridled, hilarious ranting solves everything.',
            'Tessa: TADDAT. Shuffling together in the right general direction since 1997.',
            'AA:    It is a little known fact that the refrain \'sweetheart your heart my hot\' in \'I\'m So Hot\' by 183 Club is a reference to Danielle,' \
                     ' because she is so, so hot.  The part about the \'coh, coh heart\' refers to someone else.',
            'AA:  The \'abs and glutes\' teacher at Arrillaga still plays Danielle\'s Asian pop CD as pump-up music.',
            'AA:  Danielle is so talented at multitasking, she can hold an entire conversation with you while she\'s asleep.',
            'AA:  In her spare time, she teaches sushi noobs how to eat an entire piece of sushi in one bite.' \
                  ' NO MATTER HOW BIG.  You CAN do it; you WILL do it; and you will LIKE IT.',
            'AA:  Your ability to consume chicken feet is unparalleled.  ;)',
            'AA:  Danielle holds the Facebook record for world\'s longest duration of a profile picture.',
            'AA:   ASES built a shrine in her honor.  As part of their hazing ritual, new members are required to polish it daily ' \
                    'and spend two hours meditating on how to be more like her.',
            'AA:  Danielle on a sugar high is THE BEST Danielle.',
            'AA:  Danielle once broke into a church in the middle of the night, climbed onto its roof through a crazy maze of ceiling-tunnels,' \
                  'and screamed \"I\'m the king of the world!\" when she got to the top.  Two parts of that story are true.',
            'AA: Danielle is the best partner-in-crime ever.  She made college so much fun; always game for an adventure. ' \
                'And she was always there for a hug if I had a bad day.  We solved all of the world\'s problems '\
                '(because in college, world = boys) during late-night conversations in bed when we both couldn\'t sleep.' \
                'She is hilarious and goofy and sweet and supportive, and I always felt like I was home no matter where ' \
                'I was if I was with her!  Love you and miss you, best roomie ever!!! ',
            'Miko: Dr. Dong\'s vagini coefficient is 0.99, which is 69 standard deviations above the mean.',
            'Miko: You can pull off talking about economics and stroking a breast and not be Dominic Strauss Kahn.',
            'Miko: You are the most generous and loyal friend anyone could ever wish for. For reals.  We love you more than you could know.',
            'Miko: I would go into a knife fight with chopsticks for you.',
            'Miko: You\'re an honorary blonde when it comes to both beauty and sense of direction (says fellow directionless blonde).',
            'Miko: The Dr. Dong Cocktail: 2 parts wit, 3 parts heart, 4 parts dead sexy.',
            'Miko: Cave spelunking eels are nothing compared to your Ravenclaw wand.',
            'Mui Mui: Thanks for being the best sister ever! You are always so supportive, generous, and caring. ' \
                   'Thank you for being my role model and best friend. I love you so much! And remember, keep both hands on the steering wheel!',
            'Jimmy: You are is the world\'s best (inappropriate) haiku writer!',
            'Jimmy: You boast better baking, basting, and battering skills than Bourdain!',
            'Jimmy: You paint primroses prettier than Picasso.',
            'Jimmy: \"10 o\'clock and 2 o\'clock, 10 o\'clock and 2 o\'clock!\" (As an alternate or reinforcing statement for Jacquelyn\'s frequent comment).',
            'Alan Neo: You\'re a wonderful pengyou to all that know you!',
            'Jeff: You is the best roommate ever who would never set the microwave on fire.',
            'Casey: You is the best kind of roommate. And by that, I mean never around, but when she is, she brings food.',
            'Alexis: Cold hands, warm heart! ',
            'Alexis: You are a shining example of unconditional love for rabbits!',
            'Christie: You are incredible. You are vibrant, classic and daring. You are a loyal, adventurous friend, '\
                       'ready for anything and everything. I love and admire you.',
            'Kevin: The most beautiful Daniel I ever knew.',
            'Kevin: Demand-driven. Actionable. Next-generation. Interactive. Ecosystemic. Leveraged. Lateral. EATER.',
            'Kevin: One woman tiger team.',
            'Kevin: MARZIPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN!',
            'Kevin: The motivation with whom to break fast, the procrastination with whom to lunch, and the inspiration with whom to dream and dine.',
            'Kevin: Mulier fortis; quasi aurora consurgens.',
            'Michael: Danielle you are amazing because...        You are a phenomenal dancer             When you speak,  people listen, '\
                      'You are fantastic at concensus building,             You make it okay to feel vulnerable and uncertain '\
                      '            You are able to persevere and that inspires us             Your smile radiates feelings of spring time breeze '\
                      'and summer time warmth.            When you sleep it is funny.',
            'Brian: Danielle is super caring, kind and loving! Happy Birthday Danielle - You are the best cousin and friend I could ever ask for.',
            'Judy: Happy Birthday, Daniel(le)!!!',
            'Judy: Because we put the \"HA\" in White Plaza',
            'Judy: Two words: ZENG LAOSHI',
            'Kat: Because she actually liked studying at Meyer.',
            'Kat: Chinese teachers call her Daniel because they can\'t pronounce Danielle, and she smiles graciously despite it all.',
            'Kat: She is awesome because she will roll goats with you.',
            'Kat: Danielle will hug you when she is sick.',
            'Kat: Danielle\'s wardrobe puts Zooey Deschanel to shame.',
            'Baba: Danielle is a thoughtful and loving person. She enjoys and values her friendships greatly. '\
                   'She is a friend to many, definitely a people person. She has many interests and she loves to '\
                   'explore and learn: the arts, cooking, music, sports, a quick study. Above all, she loves her family!',
            'Mama: Danielle is a gift from God. She is kind-hearted, thoughtful and always put others before herself. '\
                   'She is loving, beautiful, gracious, and so much fun to be with. She is also artistic to no end and my '\
                   'go-to art consultant. I wish our dearest darling Danielle the happiest birthday ever, and may all your '\
                   'wishes come true! Love you with all my heart!'
            ]
    return choice(reasons)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
