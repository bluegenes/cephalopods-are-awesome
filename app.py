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
    reason, source = reasonSonyaIsAwesome().split('::')
    capability = TwilioCapability(app.config['ACCOUNT_SID'],
        app.config['AUTH_TOKEN'])
    capability.allow_client_outgoing(app.config['SONYA_APP_SID'])
    token = capability.generate()
    return render_template('index.html', token=token, reason=reason, source = source)


@app.route('/voice', methods=['POST'])
def voice():
    r = twiml.Response()
    r.say('Hello.  Here is a reason why cephalopods are awesome.')
    reason = reasonSonyaIsAwesome()
    #reason.replace(':', '.')
    #reason = "This one is from %s" % reason
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
     #   reason.replace(':', '.')
      #  reason = "This one is from %s" % reason
        r.say(reason)
    elif request.form['Digits'] == '2':
        r.say('Bye!')
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
        r.sms("Welcome to the Cephalopods are Awesome Hotline.  Text CEPH " \
                "to get one random reason why cephalopods are awesome.")
    else:
        r.sms(reason)
    return str(r)


def reasonSonyaIsAwesome():
    reasons = [
            'Octopuses have eight arms, and squid and cuttlefish have eight arms and two feeding tentacles ' \
                '(making them decapods). But the nautilus, another type of cephalopod, outnumbers its brethren ' \
                'in terms of appendages: females have around 50 arms while males manage 90 or so. A single nautilus ' \
                'arm is less powerful than other cephalopods, but the arms are so numerous they can easily overpower prey.' \
                ':: http://bit.ly/17grqte',
            'No species of cuttlefish lives on the East Coast of the United States, but there are more than 100 species' \
                ' that inhabit shallow waters in other parts of the world. :: http://bit.ly/17grqte',
            'Some species of squid can swim at speeds up to 25 miles per hour, as fast as some sharks, but only in short spurts.' \
                ':: http://bit.ly/17grqte',
            'The earliest known ancestor of today\'s squid is Kimberella, a tiny mollusk that looked like a jellyfish and lived ' \
                'about 555 million years ago. :: http://bit.ly/17grqte',
            'Neuroscientists in training learn the basics of neurosurgery by practicing on Loligo pealei squid. ' \
                'Their thick axon, thicker than any human nerves, is easier to start with. :: http://bit.ly/17grqte',
            'Vampyroteuthis infernalis has been given the inappropriate nickname of \"Vampire Squid from Hell.\" '
                'Not only is it not a squid (it\'s an octopus), it\'s more coward than predator. When Vampyroteuthis ' \
                'feels threatened, it bites off the end of one of its eight bioluminescent arms, which then floats away, ' \
                'luring a potential enemy with its glowing blue light. :: http://bit.ly/17grqte',
            'Some cephalopod ink contains the chemical dopamine, the neurotransmitter that, in human brains, produces ' \
                'the sensation of euphoria. (Scientists don\'t yet know what role dopamine plays in the squid world, though.)' \
                ':: http://bit.ly/17grqte',
            'The fossils of ammonites---extinct cephalopods that lived 400 to 65 million years ago---were so common on the ' \
                'southern England coast that the town of Whitby had three of them on its town coat of arms. However, the local ' \
                'people thought they were the remains of coiled snakes and added heads to their depictions of the fossils. ' \
                '(The town\'s current coat of arms still has ammonite fossils on it, but the snake heads have been removed.) ' \
                ':: http://bit.ly/17grqte',
            'The tiny deep-sea squid Heteroteuthis dispar is nicknamed the \"fire shooter\" because it shoots out a cloud of ' \
                'light---from bioluminescent photophores---to distract predators. :: http://bit.ly/17grqte',
            'The Hawaiian bobtail squid (Euprymna scolopes) spends its days buried in the sand and hunts only at night. ' \
                'To camouflage itself in shallow, moonlit waters, it takes up luminescent bacteria that help it to blend ' \
                'into its environment. :: http://bit.ly/17grqte',
            'Humboldt squid, the large species now commonly found off the coast of California (and on the plates of ' \
                'California restaurants), can practice cannibalism. :: http://bit.ly/17grqte',
            'Male paper nautiluses, a type of octopus, are about a tenth the size of the females of the species. ' \
                'The male fertilizes the female by breaking off a special arm, which then swims to the female and ' \
                'deposits spermatophores into her. :: http://bit.ly/17grqte',
            'Giant Pacific octopuses can grow up to 400 pounds, though the ones that inhabit aquarium exhibits usually ' \
                'reach only 30 or 40 pounds in size. This species is smart, and aquarium managers are kept busy creating ' \
                'puzzles to challenge the octopuses\' brains. :: http://bit.ly/17grqte',
            'The Humboldt squid can turn itself blood-red. Because this wavelength of light doesn\'t travel far underwater, ' \
                'a dark red squid is effectively invisible. :: http://bit.ly/17grqte'
            'The colossal squid is the world\'s largest invertebrate! :: http://bit.ly/1q7SMEP',
            'Want to celebrate Cephalopods? October 8-12 are \"Cephalopod Awareness Days,\" meant to bring attention to the ' \
                'diversity, conservation and biology of the world\'s cephalopods. :: http://cephalopodday.tumblr.com/about',

            ]
    return choice(reasons)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
