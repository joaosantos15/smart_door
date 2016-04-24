#!/usr/bin/env python
import ReadSala2
import authorization
import time
import RPi.GPIO as GPIO

init = 0
continuereading = True
doorlock=True
hash_uid="0"
uid=None
eligible=None
eligible2=[]
badcard = [[-1,-1,-1,-1,-1]]

LED_PIN = 13
DOOR_PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DOOR_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
#security guard tag's UID
master_keys=[[116, 150, 107, 26, 147]]

#default state - locked, for when the system reboots
GPIO.output(DOOR_PIN, 0)

#check for security guards key
def check_for_master_key(uid):
    if uid in master_keys:
        return True
    else:
        return False

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, BAZANDOO."
    continue_reading = False
#loop until finding a card
def look_for_cards():
    card =ReadSala2.keep_reading()
    return card

def get_card_hash(uid):
    digest=ReadSala2.get_digest(uid)
    return digest

def get_authorization_status():
    authorized= authorization.door_get_ellegible()
    return authorized

def reset_reading():
    global uid
    global hash_uid
    global eligible
    uid = "0"
    hash_uid = "0"
    eligible = None
    print("...Voltando a ler cartoes")

def lock_door():
    global doorlock
    global DOOR_PIN
    doorlock=True
    print("Door Locked")
    GPIO.output(DOOR_PIN, doorlock)
    time.sleep(3)

def unlock_door():
    global doorlock
    global DOOR_PIN
    doorlock=False
    print("Door Unlocked")
    GPIO.output(DOOR_PIN, doorlock)
    time.sleep(3)

def change_door_state():
    blink_right()
    if doorlock:
        unlock_door()
        return doorlock
    if not doorlock:
        lock_door()
        return doorlock

def log_entry(name):
    authorization.door_log(name,doorlock,doorlock)

def handle_bad_card():
    print("Bad reading... try again")
    blink_wrong()
    time.sleep(3)

def handle_unauthorized_user():
    print("Ou nao podes, ou nao estas logado, yo")
    blink_wrong()
    time.sleep(3)

def blink_wrong():
    global LED_PIN
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)

def blink_right():
    global LED_PIN
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)

def blink_no_connection():
    global LED_PIN
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)

def standing_by():
    global LED_PIN
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 1)
    time.sleep(0.1)
    GPIO.output(LED_PIN, 0)
    time.sleep(0.1)
#cheks if user is in the cache
"""
def check_if_in_cache(uid):
    global eligible2
    if eligible2 != None:
	print("Checking if in cache...")
        for (name, ist_ID, hash) in eligible2:
            if (str(hash) == uid):
		print("in cache!!")
                change_door_state()
                try:
                    log_entry(name)
                except Exception as e:
                    print "No network... Cache mode"
                    blink_no_connection()
                reset_reading()
"""
def check_if_in_cache(uid):
    global eligible2
    if eligible2 != None:
	print("Checking if in cache...")
        for (name, ist_ID, hash) in eligible2:
            if (str(hash) == uid):
		print("in cache!!")
                return name
        return False




def main():
    global uid
    global eligible,eligible2
    while continuereading:
        uid=look_for_cards()
        if uid != None:
            standing_by()
            #handle a bad reading
            if uid == badcard:
                handle_bad_card()
                continue
            if(check_for_master_key(uid)):
                change_door_state()
                #logs are made in try catch blocks to handle bad network connectivity
                try:
                    log_entry("seguranca")
                except Exception as e:
                    print("No connection do DB, master card")
                reset_reading()
                continue
            hash_uid= get_card_hash(uid)
	    name = check_if_in_cache(hash_uid)
	    print(str(name))
            if( name != False):
                change_door_state()
                #logs are made in try catch blocks to handle bad network connectivity
                try:
                    log_entry(name)
                except Exception as e:
                    print("Cached user")
                reset_reading()
                continue
            hash_uid= get_card_hash(uid)
            #checks if the user is in cache

            #if not in cache, it contacts the database
            try:
                eligible= get_authorization_status()
                eligible2 = []

                i=0
                for (name, ist_ID, hash) in eligible:
                    #copies the query results to the cache copy
                    eligible2.append((name,ist_ID,hash))
                    i=1
                    if (str(hash) == hash_uid):
                        change_door_state()
                        log_entry(name)
                        reset_reading()
                        i=-1
                        break
                if(i==1):
                    blink_wrong()
            except Exception as e:
                print("No connection do DB, regular card")
                blink_no_connection()
                time.sleep(3)
                continue



    time.sleep(1)

main()
