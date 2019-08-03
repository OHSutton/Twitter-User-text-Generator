from numpy.random import randint

class MarkovModel:
    def __init__(self, transition_dict=None, starting_words=None):
        """
        Instantiates the Markov chain class

        Parameters:
            all_tweets (List(String)): A list of the tweets
        """   
        # In transition dict, keys are unique words in a dict and values are all words that ever follow
        # the unique word        
        self._transition_dict = {} if transition_dict == None else transition_dict
        self._starting_words = [] if starting_words == None else starting_words

    def create_transition_dict(self, all_tweets):
        """
        Creates a dictionary where each unique word in the tweets is a state, and
        the words that immediately succeed it are the states that can be 'reached'.

        Parameters:
            all_tweets: (List(String)) A list of tweets
        """
        for tweet in all_tweets:
            words = tweet.split(" ")
            last_word_index = len(words) - 1
            self._starting_words.append(words[0])

            for index, word in enumerate(words):
                if index == last_word_index:
                    break
                    
                next_word_index = index + 1
                if word in self._transition_dict.keys():
                    self._transition_dict[word].append(words[next_word_index])
                else:
                    self._transition_dict[word] = [words[next_word_index]]

    @classmethod
    def load_model(cls, user_id):
        """
        Loads a pre-existing transition dictionary and starting words list into this model.

        Parameters:
            user_id: The name of the user for this transition dictionary.

        Precondition:
            Ensure user_id is valid
        """
        transition_dict = {}
        starting_words = []
        # Reads in the transition dictionary
        with open(user_id + "_transition_dict.txt", encoding='utf-8') as file:
            for line in file.readlines():
                line = line.strip().split(" ")
                unique_word = line[0]
                next_words = line[1:]
                transition_dict[unique_word] = next_words

        # Reads in the starting words
        with open(user_id + "_starting_words.txt", encoding='utf-8') as file2:
            for line in file2.readlines():
                starting_words.append(line.strip())

        return cls(transition_dict, starting_words)

    def generate_text(self, max_length=20):
        """
        Randomly generates text for a given twitter user.

        Parameters:
            max_length (int): The desired length of the text
        Returns:
            The generated text
        """
        tweet_ended = False  # True if text generation finished naturally (i.e. len < max_length)
        word_count = 1

        next_word_index = randint(0, len(self._starting_words))
        current_word = self._starting_words[next_word_index]
        text = current_word

        while word_count <= max_length and not tweet_ended:
            
            # Generates the next word based off of the current word
            if current_word in self._transition_dict.keys() and self._transition_dict[current_word]:
                next_words = self._transition_dict[current_word]
                next_word_index = randint(0, len(next_words))
                current_word = next_words[next_word_index]
                text += " " + str(current_word)
            else:
                tweet_ended = True

            word_count += 1
        return text + "\n"

    def save_model(self, user_id):
        """
        Writes both the transition dictionary and starting words list to file

        Parameters:
            user_id (String): The name of the user the transition dict is for.

        Precondition:
            Ensure user_id is valid
        """
        # Write transition dictionary to file
        with open(user_id + "_transition_dict.txt", 'w', encoding='utf-8') as file:
            # Writes in format: word nextword nextword ... nextword
            for key, value in self._transition_dict.items():
                line = str(key) + " "
                for word in value:
                    line += str(word) + " "
                file.write(line[:-1] + "\n")
        # Write the starting words to file
        with open(user_id + "_starting_words.txt", 'w', encoding='utf-8') as file2:
            for word in self._starting_words:
                file2.write(str(word) + "\n")