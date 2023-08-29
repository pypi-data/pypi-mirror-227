import redis

class Calbi():

    # It could be dangerous that the recharging_credits get bugged, but the process is getting restart there are not problem :)
    # The best it would be wake up another process to recharge the api. In the case there are not process slept, it would work 
    def acquire_credits(self):
        recharge = False
        # In an atomic way, the process query how many credits there are available
        with self.redis_client.lock("mutex_credits", blocking_timeout=1):
            credits = self.redis_client.llen(self.bot_name+"_credit")
            print(f"Credits available: {credits}")
            if(credits > 0):
                # Pop a credit
                self.redis_client.lpop(self.bot_name + "_credit")
            else:
                # Start the process to recharge the queue
                recharge = True
                first = self.redis_client.setnx(self.bot_name + "_recharging_credits", 1)
        
            # If it is needed to recharge the credits
            if (recharge):
                    print(f"It's needed to recharge: First?: {first}")
                    # Just the first arrived will re-charge it
                    if(first):
                        try:
                            while [ True ]:
                                new_credits = self.api_credits.get_credits()
                                print("First")
                                if (new_credits > 0):
                                    # Delete the key to the next round
                                    self.redis_client.delete(self.bot_name + "_recharging_credits")
                                    break
                            print(f"new_credits: {new_credits}")
                            # It is -1 because this bot have to consume one credit    
                            for i in range(new_credits-1):
                                self.redis_client.lpush(self.bot_name + "_credit","new_credit")
                        finally:
                            self.redis_client.delete(self.bot_name + "_recharging_credits")
                    else:
                        # If it is not the first it will sleep until there are credits.
                        self.redis_client.blpop(self.bot_name + "_credit",timeout=None)

            
    # This works perfectly :)
    def __init__(self,redis_host, redis_port, bot_name, max_bots, api_credits=None):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.bot_name = bot_name
        if self.redis_client.setnx(self.bot_name + "_initialized", 1):
            for _ in range(max_bots):
                self.redis_client.lpush(self.bot_name + "_notification", "init")
        if (api_credits):
            self.api_credits = api_credits

    def acquire(self):
       self.redis_client.blpop(self.bot_name + "_notification", timeout=None)

    def release(self):
      self.redis_client.lpush(self.bot_name + "_notification", "released")


