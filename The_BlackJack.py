import random
import time

suits=["Hearts","Diamonds","Spades","Clubs"]
ranks=["Ace","two","three","four","five","six","seven","eight","nine","ten","Jack","Queen","King"]
values={"Ace":[1,11],"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"Jack":10,"Queen":10,"King":10}

class Card:
    
    def __init__(self,suit,rank):
        self.rank=rank
        self.suit=suit
        self.value=values[rank]

    def set_value(self,new_value):
        self.value=new_value

    def __str__(self):   #Prints the name of the card
        return f"{self.suit} of {self.rank}"
    
class Deck:

    def __init__(self):
        self.all_cards=[]

        for suit in suits:   #Creates the 52 cards
            for rank in ranks:
                created_card=Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle(self):   #Shuffles the deck
        random.shuffle(self.all_cards)
                
class Player():

    def __init__(self,name,budget) -> None:  
        self.name=name
        self.budget=int(budget)
        

    def __str__(self):    #Prints the Player's name and budget.
        return f"{self.name} has {self.budget} USD."
    
    def GetPaid(self,bet):
        self.budget+=int(bet)
        print(f"+{bet} USD")

    def LoseTheBet(self,bet):
        self.budget-=int(bet)
        print(f"-{bet} USD")

class InsufficientError(Exception):
    def __init__(self,message):
        super().__init__(message)


def Introduction():
    print("Welcome to BlackJack")
    print("You will create your player by giving its name and its budget(the money which has)")
    print("You will choose whether you will get a card or stay by saying 'Hit' or 'Stay' " )
    print("\n")

def Create_A_Player():  
    global New_Player
    name=input("Write your name:")
    while True:
        try:
            budget=int(input("Give yourself a budget"))
            if budget<0:
                raise ValueError
            New_Player=Player(name,budget)
            break  
        except ValueError:
            print("Please give a proper number ")

def Create_The_Hands():
    global Hand_of_Dealer
    global Hand_of_Player
    Hand_of_Dealer=[]
    Hand_of_Player=[]

def Print_The_Deck(flag):
    if flag=="Start":  
        str_hand_of_dealer= ", ".join(map(str,Hand_of_Dealer[1:])) 
        print(f"The Dealer's hand is X and {str_hand_of_dealer}") #The Dealer's one of card is faced down.
        str_hand_of_player= ", ".join(map(str,Hand_of_Player))
        print(f"The Player's hand is {str_hand_of_player}")
        
    elif flag=="End":  
        str_hand_of_dealer= ", ".join(map(str,Hand_of_Dealer)) 
        print(f"The Dealer's hand is {str_hand_of_dealer} ")  #The Dealer's shows his card which was face down.
        str_hand_of_player= ", ".join(map(str,Hand_of_Player))
        print(f"The Player's hand is {str_hand_of_player}")

    print("\n")

def BlackJack(): #To ensure raising NameError
    pass

Card_Flag=False
import sys
def Deal_A_Card(whose_turn): 
    try:
        if whose_turn=="Player's":
            Player_picked=New_deck.all_cards.pop()
            Hand_of_Player.append(Player_picked)
            print(f"{New_Player.name} got {Player_picked}")
        elif whose_turn=="Dealer's":
            Dealer_picked=New_deck.all_cards.pop()
            Hand_of_Dealer.append(Dealer_picked)
            if Card_Flag==True:
                print(f"The Dealer got {Dealer_picked}")
                Print_The_Deck("Start")
            else:
                pass
        
        else:
            pass  #There is only two player.
    except IndexError:
        print("There is no more card left to play with")
        print("That's why, the game is going to be resetted.")
        time.sleep(2)
        BlackJack()

def StartRound():
    global Dealer_Stay
    global Player_Stay
    global Card_Flag
    Dealer_Stay=False
    Player_Stay=False
    Create_The_Hands() 
    for i in range(2):
        Deal_A_Card("Player's")
        Deal_A_Card("Dealer's")
    Card_Flag=True
    Print_The_Deck("Start")

def Wanna_Continue():
    while True:
        try:
            answer=input("Would you like to continue?(y,q):").upper()
            if answer not in ["Y","Q"]:
                raise ValueError
            elif answer=="Y":
                print("Next Round starts")
                break

            elif answer=="Q":
                print("See you next time")
                sys.exit(0)
        except ValueError:
            print("Give a proper answer")

def Place_A_Bet():
    global bet
    while True:
        try:
            bet= int(input("Place a bet:"))
            if bet<0:
                raise ValueError
            
            elif bet>New_Player.budget:
                raise InsufficientError("Insufficient budget,try again")
                
            
            print(f"{New_Player.name} bet {bet} USD")
            break  

        except ValueError:
                print("Please give a proper number ")
        
        except InsufficientError:
            pass            


def Round_END(result): 
    global Game_on
    global situation
    
    if result=="BlackJack":
        print(f"{New_Player.name} hitted BlackJack.")
        New_Player.GetPaid((3/2)*bet)
        
    elif result=="Win":
        print(f"{New_Player.name} won this round and got paid {bet} USD")
        New_Player.GetPaid(bet)
    
    elif result=="Lose":
        print("Dealer's hand is closer to 21 than Player's hand")
        print(f"{New_Player.name} lost this round and lost {bet} USD")
        New_Player.LoseTheBet(bet)
    
    elif result=="Bust":
        Game_on=True
        print(f"{New_Player.name} busted this round and lost {bet} USD")
        New_Player.LoseTheBet(bet)
    
    elif result=="Push":
        print(f"This round is PUSH,so {New_Player.name} has not won nor lost the bet")
    
    Game_on=False
    situation=False
    Print_The_Deck("End")

def BlackJackCheck():
    global sum_Player
    sum_Player=[]
    sum_Player=sum([max(card.value) if isinstance(card.value,list) else card.value for card in Hand_of_Player])
    if sum_Player==21:
        Round_END("BlackJack")
    else: 
        pass
        
        
def ScoreCount(turn):  #Sums the cards' values
    global sum_Player
    global sum_Dealer
    if turn=="Player":
        aces=[]
        for card in Hand_of_Player:
           if card.rank=="Ace":
              aces.append(card)

        for ace in aces:
           while True:
                try:
                    print("You have an Ace in your hand.")
                    ace_value=int(input("Choose the value of an Ace in your hand(1,11): "))
                    if ace_value in values["Ace"]:
                        ace.set_value(ace_value)
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter 1 or 11.")
        
        sum_Player=[]
        sum_Player=sum([card.value for card in Hand_of_Player])

    elif turn=="Dealer":
        
        aces=[]
        for card in Hand_of_Dealer:
                if card.rank=="Ace":
                    aces.append(card)
        
        for ace in aces:
            ace_value=random.choice(values["Ace"])
            ace.set_value(ace_value)

        if Dealer_Stay==True:
            sum_Dealer=[]
            sum_Dealer=sum([card.value for card in Hand_of_Dealer])
        elif Dealer_Stay==False:
            sum_Dealer=[]
            sum_Dealer=sum([card.value for card in Hand_of_Dealer[1:]])


def GameCheck(name):
    
    if name=="Player":
        ScoreCount("Player")
        if sum_Player>21:
            Round_END("Bust")
        else:
            pass
        
    elif name=="Dealer":
        global smallflag
        ScoreCount("Dealer")
        
        if sum_Dealer>21:
            
            smallflag=True
            print("The Dealer busted.")
            Round_END("Win")
        
        else:
            smallflag=False

def Dealer_AI():
    global Dealer_Stay
    if situation==True:
        if Dealer_Stay!=True:
            ScoreCount("Dealer")
            max_rank = max(max(card.value) if isinstance(card.value, list) else card.value for card in New_deck.all_cards)
            min_rank = min(min(card.value) if isinstance(card.value, list) else card.value for card in New_deck.all_cards)
            
            green_flag=0 
            for value in range(min_rank,max_rank+1):
                New_Score=sum_Dealer+value
                if New_Score<21:
                    green_flag+=1
                else:
                    pass
            
            success_rate=(green_flag/(max_rank-min_rank+1))*100
            if success_rate>40:
                Deal_A_Card("Dealer's")
                GameCheck("Dealer")
            else:
                Dealer_Stay=True
                print("Dealer chose to Stay.")
            
        else:
            print("The Dealer is staying")
        
    else:
        pass

def Decision():
    global Player_Stay

    while True:
        if Player_Stay!=True:
            choice=input("What is your choice(Stay,Hit):").capitalize()
            try:
                if choice=="Stay":
                    Player_Stay=True
                    print(f"{New_Player.name} decided to stay")

                elif choice=="Hit":
                    Deal_A_Card("Player's")
                    break

                else:
                    raise ValueError
            except ValueError:
                print("Write your choice correctly(Stay,Hit):")
                continue
            finally:
                Print_The_Deck("Start")
                GameCheck("Player")
            
        else: 
            print(f"{New_Player.name} is staying")
            Print_The_Deck("Start")
            GameCheck("Player")
            break


def Stay_Check():
    
    if Dealer_Stay==True and Player_Stay==True:
        ScoreCount("Dealer")
        ScoreCount("Player")
        GameCheck("Dealer")
        if smallflag==False:
            if sum_Dealer>sum_Player:

                Round_END("Lose")
            elif sum_Dealer==sum_Player:
                Round_END("Push")
            else:
                print("Player's hand is closer to 21 than Dealer's hand.")
                Round_END("Win")
        else:
            pass
        

def BlackJack():
    global New_deck
    global situation
    Introduction()
    time.sleep(3)
    Create_A_Player()
    print(New_Player)
    New_deck=Deck()
    New_deck.shuffle()
    Game_on=True
    while Game_on:
        situation=True
        Place_A_Bet()
        StartRound()
        BlackJackCheck()
        while situation:
            Game_on=True
            time.sleep(1)
            Decision()
            time.sleep(1)
            Dealer_AI()
            time.sleep(1)
            Stay_Check()
        print("Round is over \n")
        print(New_Player)
        time.sleep(2)
        Wanna_Continue()

BlackJack()